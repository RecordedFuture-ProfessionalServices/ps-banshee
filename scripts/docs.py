"""Docs build orchestration for PS Banshee.

Layout inspired by fastapi/scripts/docs.py (MIT). One authoritative
``docs/mkdocs.yml`` (pointing at ``docs/en/``); translated languages own
only their translated markdown files. Non-en builds are staged with the
en tree as a base, translated files overlaid on top, and a
missing-translation banner prepended to anything that hasn't been
translated yet. All builds are stitched into a single ``site/`` tree.

Commands:
  build-all           — build every language into ``site/`` (used by CI).
  dev                 — prod-like local preview: rebuilds on save.
  check-translations  — report drift; CI-blocking for every non-en language.
  translate           — LLM-powered translator (dev-machine only).

Adding a language: add an entry to ``scripts/languages.json`` and to
``docs/mkdocs.yml`` ``extra.alternate``, then run ``translate --lang <code> --all``.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import typer
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / 'docs'
DOCS_CONFIG = DOCS_ROOT / 'mkdocs.yml'
STAGE_ROOT = REPO_ROOT / '.docs_stage'
SITE_ROOT = REPO_ROOT / 'site'
SHARED = DOCS_ROOT / '_shared'
EN_ROOT = DOCS_ROOT / 'en'
LANGUAGES_CONFIG = Path(__file__).resolve().parent / 'languages.json'

LANGUAGE_NAMES: dict[str, str] = json.loads(LANGUAGES_CONFIG.read_text(encoding='utf-8'))
SUPPORTED_LANGS: tuple[str, ...] = tuple(LANGUAGE_NAMES)
NON_EN_LANGS: tuple[str, ...] = tuple(c for c in SUPPORTED_LANGS if c != 'en')

# Underscore-prefixed path segments are treated as build-time metadata (e.g.
# ``_nav.yml``) and excluded from the translation/overlay flow. These directories
# are the exceptions: content deliberately hidden from the nav via ``_`` that
# still needs to be translated per-language.
TRANSLATED_UNDERSCORE_DIRS: frozenset[str] = frozenset({'_includes'})

app = typer.Typer(help='Build and translation orchestration for PS Banshee docs.')


def _is_metadata(parts) -> bool:
    """Return True if ``parts`` sit under an untranslated metadata segment."""
    return any(part.startswith('_') and part not in TRANSLATED_UNDERSCORE_DIRS for part in parts)


def _lang_dir(lang: str) -> Path:
    return DOCS_ROOT / lang


def _env_tag_constructor(loader: yaml.Loader, node: yaml.Node):
    """Resolve mkdocs' ``!ENV`` tag against the current environment.

    Supports ``!ENV VAR`` and ``!ENV [VAR, default]``.
    """
    if isinstance(node, yaml.ScalarNode):
        return os.environ.get(loader.construct_scalar(node), '')
    if isinstance(node, yaml.SequenceNode):
        var_name, default = loader.construct_sequence(node, deep=True)
        return os.environ.get(var_name, default)
    return None


yaml.UnsafeLoader.add_constructor('!ENV', _env_tag_constructor)


def _load_yaml(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as fh:
        return yaml.load(fh, Loader=yaml.UnsafeLoader)


# The URL path prefix from ``site_url`` (e.g. ``ps-banshee`` for a GitHub Pages
# project deploy). Everything builds into ``site/<SITE_MOUNT>/`` so local URLs
# match prod URLs by construction
SITE_MOUNT = urlparse(_load_yaml(DOCS_CONFIG).get('site_url', '')).path.strip('/')
SITE_OUT = SITE_ROOT / SITE_MOUNT


def _git_last_committed(path: Path) -> int:
    try:
        out = subprocess.run(
            ['git', 'log', '-1', '--format=%ct', '--', str(path)],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return 0
    if not out:
        return 0
    return int(out)


def _stage_lang_docs(lang: str) -> Path:
    """Stage a non-en build tree and return the path to its mkdocs.yml.

    Layout: ``.docs_stage/<lang>/mkdocs.yml`` + ``.docs_stage/<lang>/content/``.
    """
    stage = STAGE_ROOT / lang
    if stage.exists():
        shutil.rmtree(stage)
    content = stage / 'content'
    content.mkdir(parents=True)

    shutil.copytree(EN_ROOT, content, dirs_exist_ok=True)
    _overlay_lang(lang, content)

    config = _patch_config_for_lang(_load_yaml(DOCS_CONFIG), lang)
    staged_config = stage / 'mkdocs.yml'
    with staged_config.open('w', encoding='utf-8') as fh:
        yaml.dump(config, fh, allow_unicode=True, sort_keys=False)
    return staged_config


def _overlay_lang(lang: str, content: Path) -> None:
    """Overlay translated files on top of the staged English copy; prepend a
    missing-translation banner to every English file that was not overridden."""
    src = _lang_dir(lang)
    notice_path = SHARED / 'missing-translation.md'
    notice = notice_path.read_text(encoding='utf-8') if notice_path.exists() else ''

    translated: set[Path] = set()
    if src.exists():
        for path in src.rglob('*'):
            if path.is_dir():
                continue
            if path.name == '.gitkeep':
                continue
            rel = path.relative_to(src)
            if _is_metadata(rel.parts):
                continue
            dest = content / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            translated.add(rel)

    if not notice:
        return

    for md in content.rglob('*.md'):
        rel = md.relative_to(content)
        if rel in translated or any(part.startswith('_') for part in rel.parts[:-1]):
            continue
        md.write_text(f'{notice}\n{md.read_text(encoding="utf-8")}', encoding='utf-8')


def _patch_config_for_lang(config: dict, lang: str) -> dict:
    """Patch the shared config for a non-en staged build."""
    base = config.get('site_url', '').rstrip('/')
    if base:
        config['site_url'] = f'{base}/{lang}/'

    config['docs_dir'] = 'content'

    stage_content = STAGE_ROOT / lang / 'content'
    for ext in config.get('markdown_extensions') or []:
        if isinstance(ext, dict) and 'pymdownx.snippets' in ext:
            ext['pymdownx.snippets']['base_path'] = [str(stage_content)]

    config['plugins'] = [
        entry
        for entry in config.get('plugins') or []
        if not (isinstance(entry, dict) and 'llmstxt' in entry)
    ]

    theme = config.get('theme') or {}
    if theme.get('language') == 'en':
        theme['language'] = lang
    config['theme'] = theme

    mapping = _load_nav_translations(lang)
    if mapping and config.get('nav') is not None:
        config['nav'] = _apply_nav_translations(config['nav'], mapping)

    return config


# ---------------------------------------------------------------------------
# Nav-label translation
# ---------------------------------------------------------------------------


def _nav_translations_path(lang: str) -> Path:
    return _lang_dir(lang) / '_nav.yml'


def _extract_nav_labels(nav) -> list[str]:
    """Collect every human-readable label in the nav tree, in first-seen order.

    A label is any dict key encountered while walking the tree. String leaves
    are file paths, not labels.
    """
    seen: set[str] = set()
    labels: list[str] = []

    def walk(node) -> None:
        if isinstance(node, dict):
            for key, val in node.items():
                if isinstance(key, str) and key not in seen:
                    seen.add(key)
                    labels.append(key)
                walk(val)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(nav)
    return labels


def _apply_nav_translations(nav, mapping: dict[str, str]):
    if isinstance(nav, dict):
        return {mapping.get(k, k): _apply_nav_translations(v, mapping) for k, v in nav.items()}
    if isinstance(nav, list):
        return [_apply_nav_translations(x, mapping) for x in nav]
    return nav


def _load_nav_translations(lang: str) -> dict[str, str]:
    path = _nav_translations_path(lang)
    if not path.exists():
        return {}
    with path.open('r', encoding='utf-8') as fh:
        data = yaml.safe_load(fh) or {}
    return {str(k): str(v) for k, v in data.items()}


def _save_nav_translations(lang: str, mapping: dict[str, str]) -> Path:
    path = _nav_translations_path(lang)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as fh:
        yaml.safe_dump(mapping, fh, allow_unicode=True, sort_keys=False)
    return path


# ---------------------------------------------------------------------------
# Build commands
# ---------------------------------------------------------------------------


def _mkdocs_build(config_path: Path, out_dir: Path) -> None:
    out_dir = out_dir.resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    subprocess.run(
        [
            'mkdocs',
            'build',
            '-f',
            str(config_path.resolve()),
            '-d',
            str(out_dir),
            '--clean',
        ],
        check=True,
        cwd=REPO_ROOT,
    )


def _build_lang(lang: str) -> None:
    if lang == 'en':
        config_path = DOCS_CONFIG
        out = SITE_OUT
    else:
        config_path = _stage_lang_docs(lang)
        out = SITE_OUT / lang
    _mkdocs_build(config_path, out)
    typer.echo(f'Built {lang} -> {out.relative_to(REPO_ROOT)}')


@app.command('build-all')
def build_all() -> None:
    """Build every supported language into a single site/ tree."""
    if SITE_ROOT.exists():
        shutil.rmtree(SITE_ROOT)
    _build_lang('en')
    for lang in NON_EN_LANGS:
        _build_lang(lang)


@app.command()
def dev(
    host: str = typer.Option('127.0.0.1'),
    port: int = typer.Option(8000),
    debounce_ms: int = typer.Option(500, help='Coalesce file events within this window.'),
) -> None:
    """Prod-like local preview: static server + rebuild-on-save for every language.

    Runs ``build-all`` once, then serves ``site/`` and watches ``docs/`` for
    changes. Edits under ``docs/en/`` or ``docs/mkdocs.yml`` rebuild every
    language; edits under ``docs/<lang>/`` rebuild only that language. Refresh
    the browser manually to see changes.
    """
    import http.server
    import socketserver
    import threading
    import time

    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    build_all()

    class _Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw) -> None:
            super().__init__(*a, directory=str(SITE_ROOT), **kw)

        def log_message(self, format: str, *args) -> None:  # noqa: A002, ARG002
            del format, args

    class _RebuildHandler(FileSystemEventHandler):
        def __init__(self) -> None:
            self.pending: set[str] = set()
            self.lock = threading.Lock()
            self.last_event = 0.0

        def _classify(self, path: str) -> set[str]:
            try:
                rel = Path(path).resolve().relative_to(DOCS_ROOT)
            except ValueError:
                return set()
            if rel == Path('mkdocs.yml'):
                return set(SUPPORTED_LANGS)
            top = rel.parts[0]
            if top == 'en':
                return set(SUPPORTED_LANGS)
            if top in SUPPORTED_LANGS:
                return {top}
            if top == '_shared':
                return set(NON_EN_LANGS)
            return set()

        def on_any_event(self, event) -> None:
            if event.is_directory:
                return
            src = event.src_path
            if isinstance(src, bytes):
                src = src.decode()
            langs = self._classify(src)
            if not langs:
                return
            with self.lock:
                self.pending.update(langs)
                self.last_event = time.monotonic()

        def drain(self) -> set[str]:
            with self.lock:
                langs = self.pending
                self.pending = set()
                return langs

    handler = _RebuildHandler()
    observer = Observer()
    observer.schedule(handler, str(DOCS_ROOT), recursive=True)
    observer.start()

    def _rebuild_loop() -> None:
        while True:
            time.sleep(debounce_ms / 1000)
            with handler.lock:
                idle = (time.monotonic() - handler.last_event) * 1000 >= debounce_ms
            if not idle:
                continue
            langs = handler.drain()
            if not langs:
                continue
            ordered = [c for c in SUPPORTED_LANGS if c in langs]
            typer.echo(f'[dev] rebuilding: {", ".join(ordered)}')
            for code in ordered:
                try:
                    _build_lang(code)
                except subprocess.CalledProcessError as exc:
                    typer.echo(f'[dev] build {code} failed: {exc}', err=True)

    threading.Thread(target=_rebuild_loop, daemon=True).start()

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    socketserver.ThreadingTCPServer.daemon_threads = True
    prefix = f'/{SITE_MOUNT}/' if SITE_MOUNT else '/'
    typer.echo(f'Serving {SITE_ROOT} at http://{host}:{port}{prefix} (watching docs/)')
    try:
        with socketserver.ThreadingTCPServer((host, port), _Handler) as srv:
            srv.serve_forever()
    except KeyboardInterrupt:
        typer.echo('\nStopping...')
    finally:
        observer.stop()
        observer.join()


# ---------------------------------------------------------------------------
# Translation-drift check
# ---------------------------------------------------------------------------


@dataclass
class Drift:
    lang: str
    missing: list[str]
    outdated: list[str]
    orphaned: list[str]
    missing_nav: list[str]
    orphaned_nav: list[str]


def _detect_drift(lang: str) -> Drift:
    lang_root = _lang_dir(lang)

    en_files = {
        p.relative_to(EN_ROOT): p
        for p in EN_ROOT.rglob('*.md')
        if not _is_metadata(p.relative_to(EN_ROOT).parts[:-1])
    }

    missing: list[str] = []
    outdated: list[str] = []
    for rel, en_path in en_files.items():
        tgt = lang_root / rel
        if not tgt.exists():
            missing.append(str(rel))
            continue
        en_ts, tgt_ts = _git_last_committed(en_path), _git_last_committed(tgt)
        if en_ts > tgt_ts:
            outdated.append(str(rel))

    orphaned: list[str] = []
    if lang_root.exists():
        for p in lang_root.rglob('*.md'):
            rel = p.relative_to(lang_root)
            if rel not in en_files:
                orphaned.append(str(rel))

    nav = _load_yaml(DOCS_CONFIG).get('nav')
    nav_labels = _extract_nav_labels(nav) if nav else []
    nav_translations = _load_nav_translations(lang)
    missing_nav = [lbl for lbl in nav_labels if lbl not in nav_translations]
    orphaned_nav = [lbl for lbl in nav_translations if lbl not in nav_labels]

    return Drift(
        lang=lang,
        missing=missing,
        outdated=outdated,
        orphaned=orphaned,
        missing_nav=missing_nav,
        orphaned_nav=orphaned_nav,
    )


@app.command('check-translations')
def check_translations(
    lang: str | None = typer.Option(None, '--lang'),
    all_langs: bool = typer.Option(False, '--all'),
) -> None:
    """Report translation drift. Exits non-zero when drift blocks merge."""
    if all_langs:
        langs = list(NON_EN_LANGS)
    elif lang:
        langs = [lang]
    else:
        raise typer.BadParameter('Pass --lang <code> or --all')

    drifts = [_detect_drift(code) for code in langs]
    exit_code = 0
    for d in drifts:
        typer.echo(f'[{d.lang}]')
        if not (d.missing or d.outdated or d.orphaned or d.missing_nav or d.orphaned_nav):
            typer.echo('  clean')
            continue
        for kind in ('missing', 'outdated', 'orphaned', 'missing_nav', 'orphaned_nav'):
            items = getattr(d, kind)
            if items:
                typer.echo(f'  {kind}:')
                for it in items:
                    typer.echo(f'    - {it}')
        exit_code = 1

    raise typer.Exit(exit_code)


# ---------------------------------------------------------------------------
# LLM translator
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r'^#{1,6}\s', re.MULTILINE)
_FENCE_RE = re.compile(r'^```', re.MULTILINE)
_SNIPPET_RE = re.compile(r'^--8<--\s+.*$', re.MULTILINE)


def _validate_translation(src: str, out: str) -> str | None:
    src_h, out_h = len(_HEADING_RE.findall(src)), len(_HEADING_RE.findall(out))
    if src_h != out_h:
        return f'heading count mismatch: source has {src_h}, output has {out_h}'
    src_f, out_f = len(_FENCE_RE.findall(src)), len(_FENCE_RE.findall(out))
    if src_f != out_f:
        return f'fenced code block count mismatch: source has {src_f}, output has {out_f}'
    src_snips = set(_SNIPPET_RE.findall(src))
    out_snips = set(_SNIPPET_RE.findall(out))
    if src_snips != out_snips:
        return f'snippet include mismatch: missing {src_snips - out_snips!r}'
    return None


def _run_translation(model_spec: str, system_prompt: str, source: str, existing: str | None) -> str:
    try:
        from pydantic_ai import Agent
        from pydantic_ai.settings import ModelSettings
    except ImportError as exc:
        raise typer.BadParameter(
            'pydantic-ai is not installed. Run: uv sync --group translations'
        ) from exc

    user = f'Translate the following Markdown document.\n\n---\n\n{source}'
    if existing:
        user += (
            '\n\n---\n\nExisting translation (use as reference for terminology; '
            f'may be outdated):\n\n{existing}'
        )

    settings = ModelSettings(max_tokens=64000)
    last_err: str | None = None
    for _ in range(3):
        prompt = (
            system_prompt
            if not last_err
            else (f'{system_prompt}\n\nPrevious attempt failed validation: {last_err}. Fix it.')
        )
        agent = Agent(model_spec, system_prompt=prompt, model_settings=settings)
        result = agent.run_sync(user)
        text = getattr(result, 'data', None) or getattr(result, 'output', None) or str(result)
        err = _validate_translation(source, text)
        if err is None:
            return text
        last_err = err
    raise RuntimeError(f'Translation failed validation after 3 attempts: {last_err}')


def _translate_nav(labels: list[str], model_spec: str, lang_name: str) -> dict[str, str]:
    """Translate a list of short nav labels via LLM. Returns {english: translated}."""
    try:
        from pydantic import BaseModel
        from pydantic_ai import Agent
        from pydantic_ai.settings import ModelSettings
    except ImportError as exc:
        raise typer.BadParameter(
            'pydantic-ai is not installed. Run: uv sync --group translations'
        ) from exc

    class NavOut(BaseModel):
        translations: dict[str, str]

    system = (
        f'You are translating short sidebar labels for the PS Banshee CLI documentation '
        f'from English into {lang_name}. Return a JSON object with a single key '
        f'"translations" mapping every English label (exactly as given) to its translated '
        f'form.\n\n'
        f'Rules:\n'
        f'- Every English label in the input MUST appear as a key in the output.\n'
        f'- Keep the translations concise — these render as sidebar navigation.\n'
        f'- Use the formal register standard for technical vendor documentation in '
        f'{lang_name} (e.g. です・ます in Japanese, 합니다체 in Korean).\n'
        f'- Preserve brand and product names as-is: Recorded Future, PS Banshee, '
        f'Playbook Alert, Classic Alert, IOC, PCAP.\n'
        f'- If a term is a well-established technical English term with no natural '
        f'equivalent, keep the English term.'
    )
    user = 'Translate these labels:\n' + '\n'.join(f'- {lbl}' for lbl in labels)
    settings = ModelSettings(max_tokens=4000)

    missing: list[str] = list(labels)
    for _ in range(3):
        agent = Agent(model_spec, system_prompt=system, model_settings=settings, output_type=NavOut)
        result = agent.run_sync(user)
        out = getattr(result, 'output', None) or getattr(result, 'data', None)
        if out is None:
            continue
        mapping = dict(out.translations)
        missing = [lbl for lbl in labels if lbl not in mapping]
        if not missing:
            return mapping
    raise RuntimeError(f'Nav translation missing labels after 3 attempts: {missing}')


def _sync_nav_translations(lang: str, model_spec: str, lang_name: str) -> tuple[Path, int]:
    """Translate any nav labels not yet in ``docs/<lang>/_nav.yml``. Merges with existing."""
    nav = _load_yaml(DOCS_CONFIG).get('nav')
    labels = _extract_nav_labels(nav) if nav else []
    existing = _load_nav_translations(lang)

    stale = [k for k in existing if k not in labels]
    for k in stale:
        existing.pop(k, None)

    todo = [lbl for lbl in labels if lbl not in existing]
    if not todo and not stale:
        return _nav_translations_path(lang), 0

    if todo:
        translated = _translate_nav(todo, model_spec, lang_name)
        existing.update(translated)

    merged = {lbl: existing[lbl] for lbl in labels if lbl in existing}
    path = _save_nav_translations(lang, merged)
    return path, len(todo)


_ALTERNATE_BLOCK_RE = re.compile(
    r'(\n {2}alternate:\n(?: {4}- name: .+\n {6}link: .+\n {6}lang: [\w-]+\n)+)'
)


def _register_language(code: str, name: str) -> tuple[bool, bool]:
    """Add ``code`` to ``languages.json`` and ``mkdocs.yml`` if missing.

    Returns ``(json_added, mkdocs_added)``. Idempotent — no-op when the code
    already appears. Reference:
    https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/
    """
    json_added = False
    if code not in LANGUAGE_NAMES:
        data = json.loads(LANGUAGES_CONFIG.read_text(encoding='utf-8'))
        data[code] = name
        LANGUAGES_CONFIG.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        LANGUAGE_NAMES[code] = name
        global SUPPORTED_LANGS, NON_EN_LANGS  # noqa: PLW0603
        SUPPORTED_LANGS = tuple(LANGUAGE_NAMES)
        NON_EN_LANGS = tuple(c for c in SUPPORTED_LANGS if c != 'en')
        json_added = True

    text = DOCS_CONFIG.read_text(encoding='utf-8')
    if re.search(rf'^ {{6}}lang: {re.escape(code)}\s*$', text, re.MULTILINE):
        return json_added, False

    match = _ALTERNATE_BLOCK_RE.search(text)
    if not match:
        raise RuntimeError(
            'Could not locate the extra.alternate block in docs/mkdocs.yml; add the entry manually.'
        )
    link = f'/{SITE_MOUNT}/{code}/' if SITE_MOUNT else f'/{code}/'
    entry = f'    - name: {name}\n      link: {link}\n      lang: {code}\n'
    DOCS_CONFIG.write_text(text[: match.end()] + entry + text[match.end() :], encoding='utf-8')
    return json_added, True


def _translate_one(
    lang: str,
    rel: Path,
    model: str,
    system_prompt: str,
) -> Path:
    src_path = EN_ROOT / rel
    tgt_path = _lang_dir(lang) / rel
    source = src_path.read_text(encoding='utf-8')
    existing = tgt_path.read_text(encoding='utf-8') if tgt_path.exists() else None
    out = _run_translation(model, system_prompt, source, existing)
    tgt_path.parent.mkdir(parents=True, exist_ok=True)
    tgt_path.write_text(out, encoding='utf-8')
    return tgt_path


@app.command()
def translate(
    lang: str = typer.Option(..., '--lang'),
    name: str | None = typer.Option(
        None,
        '--name',
        help=(
            'Native name of the language (e.g. "Français"). Required only when '
            'first registering a new --lang; ignored if the code is already known. '
            'The --lang code must match a locale supported by mkdocs-material — '
            'see https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/'
        ),
    ),
    path: Path | None = typer.Option(None, '--path', help='Translate a single en file.'),
    all_: bool = typer.Option(False, '--all', help='Translate every missing or outdated file.'),
    model: str = typer.Option('anthropic:claude-sonnet-4-6', '--model'),
    concurrency: int = typer.Option(5, '--concurrency', help='Parallel translations.'),
) -> None:
    """Translate en docs to <lang> using a pydantic-ai agent.

    Pass either ``--path <en-file>`` for a single file or ``--all`` to
    translate everything drifted (missing + outdated). Files are translated
    in parallel; failures are reported at the end so one bad file doesn't
    stop the rest.

    First time onboarding a language: also pass ``--name`` so the tool can
    register the code in ``scripts/languages.json`` and add an
    ``extra.alternate`` entry to ``docs/mkdocs.yml``.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    from rich.console import Console
    from rich.progress import (
        BarColumn,
        MofNCompleteColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeElapsedColumn,
    )

    if lang == 'en':
        raise typer.BadParameter(f'Cannot translate to {lang!r}')
    if lang not in SUPPORTED_LANGS:
        if not name:
            raise typer.BadParameter(
                f'Language {lang!r} is not registered. Pass --name "<Native Name>" '
                f'to add it to scripts/languages.json and docs/mkdocs.yml, or add '
                f'it manually.'
            )
        json_added, mkdocs_added = _register_language(lang, name)
        if json_added:
            typer.echo(f'Registered {lang!r} → {name!r} in {LANGUAGES_CONFIG.name}')
        if mkdocs_added:
            typer.echo(f'Added {lang!r} to extra.alternate in {DOCS_CONFIG.name}')
    elif name and name != LANGUAGE_NAMES.get(lang):
        typer.echo(
            f'--name {name!r} ignored; {lang!r} is already registered as {LANGUAGE_NAMES[lang]!r}.'
        )
    if not path and not all_:
        raise typer.BadParameter('Pass --path <en-file> or --all')

    lang_root = _lang_dir(lang)
    lang_root.mkdir(parents=True, exist_ok=True)

    if path:
        targets = [path.resolve().relative_to(EN_ROOT)]
    else:
        drift = _detect_drift(lang)
        targets = [Path(t) for t in sorted(set(drift.missing + drift.outdated))]

    lang_name = LANGUAGE_NAMES.get(lang, lang)
    if all_:
        try:
            nav_path, added = _sync_nav_translations(lang, model, lang_name)
            if added:
                typer.echo(
                    f'Nav: translated {added} new label(s) → {nav_path.relative_to(REPO_ROOT)}'
                )
            else:
                typer.echo('Nav: up to date.')
        except Exception as exc:  # noqa: BLE001 — surface any translator failure
            typer.echo(f'Nav translation failed: {exc}', err=True)

    if not targets:
        typer.echo('Nothing to translate.')
        return

    base = (SHARED / 'translation-prompt.md').read_text(encoding='utf-8')
    system_prompt = base.replace('{{target_language_name}}', LANGUAGE_NAMES.get(lang, lang))

    console = Console()
    failures: list[tuple[Path, str]] = []
    successes: list[Path] = []

    with Progress(
        SpinnerColumn(),
        TextColumn('[bold blue][{task.fields[lang]}][/]'),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn('{task.description}'),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task_id = progress.add_task('translating…', total=len(targets), lang=lang)
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = {
                pool.submit(_translate_one, lang, rel, model, system_prompt): rel for rel in targets
            }
            for fut in as_completed(futures):
                rel = futures[fut]
                try:
                    tgt = fut.result()
                    successes.append(rel)
                    progress.console.log(f'[green]✓[/] {rel} → {tgt.relative_to(REPO_ROOT)}')
                except Exception as exc:  # noqa: BLE001 — surface any translator failure
                    failures.append((rel, str(exc)))
                    progress.console.log(f'[red]✗[/] {rel}: {exc}')
                progress.advance(task_id)

    console.rule(f'[bold]translated {len(successes)}/{len(targets)} — {len(failures)} failed')
    if failures:
        for rel, err in failures:
            console.print(f'  [red]{rel}[/]: {err}')
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    app()
