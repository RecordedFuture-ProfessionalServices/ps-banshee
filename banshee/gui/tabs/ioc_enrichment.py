#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

from tkinter import messagebox, ttk

from ..theme.base_tab import BaseTab
from ..theme.ui_elements import action_bar, card, combo_row, multiline, primary_btn

SUB_COMMAND_HINTS = {
    'lookup': 'One API call per IOC — rich detail, slower for large batches.',
    'bulk-lookup': 'Batched (up to 1000 IOCs/call) — risk score and triggered rules only.',
}


class IocTab(BaseTab):
    """Render the tab for enriching a singular IOC."""

    NAV_NAME = 'IOC Enrichment'
    NAV_GROUP = 'Investigate'
    NAV_TIP = "Lookup IOC's against Recorded Future Data"

    ENTITY_TYPES = ['ip', 'domain', 'url', 'hash', 'vulnerability']
    SUB_COMMANDS = ['lookup', 'bulk-lookup']

    def __init__(self, parent):
        super().__init__(parent)
        c = card(self.body, 'IOC Enrichment')
        c.pack(fill='x')

        self.sub_command = combo_row(c, 'Sub-command', self.SUB_COMMANDS, 'lookup')
        self.sub_command.bind('<<ComboboxSelected>>', self._on_sub_cmd)
        self.entity_type = combo_row(c, 'Entity type', self.ENTITY_TYPES, 'ip')

        self.hint_label = ttk.Label(c, text=SUB_COMMAND_HINTS['lookup'], style='Muted.TLabel')
        self.hint_label.pack(fill='x', pady=(0, 4))

        frame = ttk.Frame(c, style='Card.TFrame')
        frame.pack(fill='x', pady=4)
        ttk.Label(
            frame, text='IOC(s) — one per line', width=20, anchor='nw', style='FieldLabel.TLabel'
        ).pack(side='left', anchor='n')
        self.ioc_text = multiline(frame, height=4)
        self.ioc_text.pack(side='left', fill='x', expand=True)

        bar = action_bar(c)
        primary_btn(bar, 'Run', self._run)

        self._build_console()

    def _on_sub_cmd(self, _event=None):
        self.hint_label.configure(text=SUB_COMMAND_HINTS[self.sub_command.get()])

    def _run(self):
        iocs = self.ioc_text.get('1.0', 'end').split()
        if not iocs:
            messagebox.showinfo('IOC Enrichment', 'Enter at least one IOC to look up.')
            return

        args = ['ioc', self.sub_command.get(), self.entity_type.get(), *iocs]
        self.command_runner_async(args)
