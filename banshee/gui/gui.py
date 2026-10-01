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

"""Banshee GUI - a Tkinter built GUI to for ps-banshee."""

import contextlib
import tkinter as tk
from tkinter import ttk

from banshee.gui import constants
from banshee.gui.helpers import theme
from banshee.gui.helpers.generic_helpers import load_image, test_api_token
from banshee.gui.helpers.widgets import ToolTip

TAB_CLASSES = []

NAV_GROUPS = []

for _cls in TAB_CLASSES:
    if not NAV_GROUPS or NAV_GROUPS[-1][0] != _cls.NAV_GROUP:
        NAV_GROUPS.append((_cls.NAV_GROUP, []))
    NAV_GROUPS[-1][1].append(_cls.NAV_NAME)

NAV_TIPS = {_cls.NAV_NAME: _cls.NAV_TIP for _cls in TAB_CLASSES}


def _build_header(root: tk.Tk):
    """Build the header of the GUI, contains the Title, logo and status on the API key."""
    header = ttk.Frame(root, style='Header.TFrame', padding=(20, 14))
    header.pack(fill='x')

    left = ttk.Frame(header, style='Header.TFrame')
    left.pack(side='left')
    ttk.Label(left, text='BANSHEE', style='H1.TLabel').pack(anchor='w')

    rf_header = load_image('favicon.png', max_height=44, max_width=260)
    if rf_header:
        root._logo_refs.append(rf_header)
        tk.Label(header, image=rf_header, background=theme.Palette.NAVY, bd=0).place(
            relx=0.5, rely=0.5, anchor='center'
        )

    token_label = ttk.Label(header, style='StatusOk.TLabel')
    token_label.pack(side='right')
    token_label.configure(
        text=('RF_TOKEN active' if test_api_token() else 'RF_TOKEN missing - see Settings'),
        style='StatusOk.TLabel' if test_api_token() else 'StatusBad.TLabel',
    )
    stripe = tk.Frame(root, height=3, bg=theme.Palette.ELECTRIC_BLUE)
    stripe.pack(fill='x')


def _build_footer(root: tk.Tk):
    status_bar = ttk.Frame(root, height=3, padding=(14, 5))
    status_bar.pack(fill='x', side='bottom')
    ttk.Label(status_bar, text='ps-banshee CLI  ·  GUI front-end', style='StatusBar.TLabel').pack(
        side='left'
    )
    ttk.Label(
        status_bar,
        text='Brought to you by the Cyber Security Engineers at Recorded Future',
        style='StatusBar.TLabel',
    ).pack(side='right')


def _build_side_bar(body: ttk.Frame):
    sidebar = ttk.Frame(body, style='Nav.TFrame', width=190)
    sidebar.pack(side='left', fill='y')
    sidebar.pack_propagate(False)
    ttk.Separator(body, orient='vertical').pack(side='left', fill='y')

    return sidebar


class _Navigation:
    """A class for the funtions needed for the navigation bar."""

    def __init__(self, factories: dict):
        self.factories = factories
        self.pages: dict[str, ttk.Frame] = {}
        self.nav_buttons: dict[str, ttk.Button] = {}

    def show(self, name: str):
        page = self.pages.get(name)
        if page is None:
            page = self.pages[name] = self.factories[name]()
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
        page.tkraise()
        for n, btn in self.nav_buttons.items():
            btn.configure(style='NavActive.TButton' if n == name else 'Nav.TButton')

    def add_nav_button(self, name: str, parent: ttk.Frame, **pack_kw) -> ttk.Button:
        b = ttk.Button(parent, text=name, style='Nav.TButton', command=lambda n=name: self.show(n))
        b.pack(fill='x', **pack_kw)
        self.nav_buttons[name] = b
        if name in NAV_TIPS:
            ToolTip(b, NAV_TIPS[name])
        return b


def _build_navigation(sidebar: ttk.Frame, content: ttk.Frame):
    factories = {cls.NAV_NAME: (lambda cls=cls: cls(content)) for cls in TAB_CLASSES}
    nav = _Navigation(factories)

    for header_text, items in NAV_GROUPS:
        ttk.Label(sidebar, text=header_text, style='NavHeader.TLabel').pack(
            anchor='w', padx=16, pady=(12, 2)
        )
        for name in items:
            nav.add_nav_button(name, sidebar)

    return nav.show


def gui():
    root = tk.Tk()
    root.title('Banshee - Recorded Future Intelligence')
    root.geometry('1060x900')
    root.minsize(880, 640)
    with contextlib.suppress(tk.TclError):
        root.tk.call('tk', 'appname', constants.APP_NAME)

    theme.apply_theme(root)
    root._logo_refs = []

    _build_header(root)
    _build_footer(root)

    body = ttk.Frame(root, style='TFrame')
    body.pack(fill='both', expand=True)

    sidebar = _build_side_bar(root)
    content = ttk.Frame(style='TFrame')
    content.pack(side='left', fill='both', expand=True)

    _build_navigation(sidebar, content)

    root.mainloop()


if __name__ == '__main__':
    gui()
