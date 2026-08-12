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

Adding a language: add an entry to ``LANGUAGE_NAMES`` below and to
``docs/mkdocs.yml`` ``extra.alternate``, then run ``translate --lang <code> --all``.
"""

from __future__ import annotations

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

LANGUAGE_NAMES: dict[str, str] = {
    'en': 'English',
    'ja': '日本語',
    'ko': '한국어',
}
SUPPORTED_LANGS: tuple[str, ...] = tuple(LANGUAGE_NAMES)
NON_EN_LANGS: tuple[str, ...] = tuple(c for c in SUPPORTED_LANGS if c != 'en')

app = typer.Typer(help='Build and translation orchestration for PS Banshee docs.')


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

    return config


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
            return

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
            langs = self._classify(event.src_path)
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


def _detect_drift(lang: str) -> Drift:
    lang_root = _lang_dir(lang)

    en_files = {
        p.relative_to(EN_ROOT): p
        for p in EN_ROOT.rglob('*.md')
        if not any(part.startswith('_') for part in p.relative_to(EN_ROOT).parts[:-1])
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

    return Drift(lang=lang, missing=missing, outdated=outdated, orphaned=orphaned)


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
        if not (d.missing or d.outdated or d.orphaned):
            typer.echo('  clean')
            continue
        for kind in ('missing', 'outdated', 'orphaned'):
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


@app.command()
def translate(
    lang: str = typer.Option(..., '--lang'),
    path: Path | None = typer.Option(None, '--path', help='Translate a single en file.'),
    all_: bool = typer.Option(False, '--all', help='Translate every missing or outdated file.'),
    model: str = typer.Option('anthropic:claude-sonnet-4-6', '--model'),
) -> None:
    """Translate en docs to <lang> using a pydantic-ai agent.

    Pass either ``--path <en-file>`` for a single file or ``--all`` to
    translate everything drifted (missing + outdated).
    """
    if lang not in SUPPORTED_LANGS or lang == 'en':
        raise typer.BadParameter(f'Cannot translate to {lang!r}')
    if not path and not all_:
        raise typer.BadParameter('Pass --path <en-file> or --all')

    lang_root = _lang_dir(lang)
    lang_root.mkdir(parents=True, exist_ok=True)

    if path:
        targets = [path.resolve().relative_to(EN_ROOT)]
    else:
        drift = _detect_drift(lang)
        targets = [Path(t) for t in sorted(set(drift.missing + drift.outdated))]

    if not targets:
        typer.echo('Nothing to translate.')
        return

    base = (SHARED / 'translation-prompt.md').read_text(encoding='utf-8')
    system_prompt = base.replace('{{target_language_name}}', LANGUAGE_NAMES.get(lang, lang))

    for rel in targets:
        src_path = EN_ROOT / rel
        tgt_path = lang_root / rel
        source = src_path.read_text(encoding='utf-8')
        existing = tgt_path.read_text(encoding='utf-8') if tgt_path.exists() else None
        typer.echo(f'[{lang}] translating {rel}')
        try:
            out = _run_translation(model, system_prompt, source, existing)
        except Exception as exc:  # noqa: BLE001 — surface any translator failure
            typer.echo(f'  FAILED: {exc}', err=True)
            raise typer.Exit(1) from exc
        tgt_path.parent.mkdir(parents=True, exist_ok=True)
        tgt_path.write_text(out, encoding='utf-8')
        typer.echo(f'  wrote {tgt_path.relative_to(REPO_ROOT)}')


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    app()
