"""Gate mkdocs-llmstxt-md to the default (en) locale build only.

The plugin runs its full lifecycle once per i18n locale. During the ja pass it
matches en/ section paths in `on_files` but never captures markdown or
`dest_uri` in `on_page_markdown` (only ja pages fire there), so its
`on_post_build` overwrites `site/llms.txt` and `site/llms-full.txt` with hollow
output.

The i18n plugin swaps the per-locale config between `on_config` and
`on_pre_build`, so we detect the locale in `on_pre_build` and flip the
plugin's write flags off for the ja pass.
"""


def on_pre_build(*, config):
    if config.theme['language'] == 'en':
        return
    plugin = config.plugins.get('llmstxt-md')
    if plugin is None:
        return
    plugin.config.enable_llms_txt = False
    plugin.config.enable_llms_full = False
    plugin.config.enable_markdown_urls = False
