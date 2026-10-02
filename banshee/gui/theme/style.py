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

import contextlib
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


class Palette:
    """Set the colour palette to be used in the GUI."""

    # Brand
    ELECTRIC_BLUE = '#00B3E3'  # primary accent
    ELECTRIC_BLUE_DK = '#0095BE'  # hover / active
    RED = '#E4002B'  # destructive / alert accent
    RED_DK = '#B30022'  # hover / active

    # Neutrals
    NAVY = '#0B1F33'  # header / dark surfaces
    NAVY_LT = '#13314F'  # header secondary
    INK = '#1B2733'  # primary text
    SLATE = '#5B6B7B'  # secondary text
    LINE = '#D9E0E6'  # borders / separators
    CARD = '#FFFFFF'  # card surface
    CANVAS = '#EEF2F5'  # window background
    FIELD = '#FFFFFF'  # input fields

    # Console
    CONSOLE_BG = '#0D1622'
    CONSOLE_FG = '#D7E3EE'
    CONSOLE_ACCENT = '#00B3E3'

    # Status
    GREEN = '#1F9D55'
    AMBER = '#D9822B'

    PADDING = 10


def _pick_font(root: tk.Misc, font_list: list[str], default_font: str):
    """Return the first font in the font_list that is installed on this system."""
    installed_fonts = set(tkfont.families(root))
    for font_name in font_list:
        if font_name in installed_fonts:
            return font_name
    return default_font


def _configure_tk_widget_default(root: tk.Tk, pallet: type, fonts: dict):
    """Set the background and font defaults for text and listboxes. (Non-ttk widgets)."""
    root.configure(background=pallet.CANVAS)
    root.option_add('*Font', fonts['ui'])
    root.option_add('*Text.background', pallet.FIELD)
    root.option_add('*Text,foreground', pallet.INK)
    root.option_add('*Text.relief', 'flat')
    root.option_add('*Text.highlightThickness', 1)
    root.option_add('*Text.highlightColor', pallet.ELECTRIC_BLUE)
    root.option_add('*Text.highlightBackground', pallet.LINE)
    root.option_add('*Listbox.background', pallet.FIELD)
    root.option_add('*Listbox.foreground', pallet.INK)
    root.option_add('*Listbox.relief', 'flat')
    root.option_add('*Listbox.highlightThickness', 1)
    root.option_add('*Listbox.selectBackground', pallet.ELECTRIC_BLUE)
    root.option_add('*Listbox.selectForeground', '#FFFFFF')


def _configure_base(style: ttk.Style, pallet: type, fonts: dict):
    """Default appearance for ttk widgets."""
    style.configure('.', background=pallet.CANVAS, foreground=pallet.INK, font=fonts['ui'])
    style.configure('TFrame', background=pallet.CANVAS)
    style.configure('Card.TFrame', background=pallet.CARD)
    style.configure('Header.TFrame', background=pallet.NAVY)


def _configure_labels(style: ttk.Style, pallet: type, fonts: dict):
    """Set the styles used for labels."""
    style.configure('TLabel', background=pallet.CANVAS, foreground=pallet.INK)
    style.configure('Card.TLabel', background=pallet.CARD, foreground=pallet.INK)
    style.configure(
        'Muted.TLabel', background=pallet.CARD, foreground=pallet.SLATE, font=fonts['small']
    )
    style.configure('FieldLabel.TLabel', background=pallet.CARD, foreground=pallet.SLATE)
    style.configure('H1.TLabel', background=pallet.NAVY, foreground='#FFFFFF', font=fonts['h1'])
    style.configure(
        'Sub.TLabel', background=pallet.NAVY, foreground=pallet.ELECTRIC_BLUE, font=fonts['small']
    )
    style.configure(
        'SectionTitle.TLabel', background=pallet.CARD, foreground=pallet.INK, font=fonts['h2']
    )
    # Status pill labels (for headers)
    style.configure(
        'StatusOk.TLabel', background=pallet.NAVY, foreground=pallet.GREEN, font=fonts['ui_bold']
    )
    style.configure(
        'StatusBad.TLabel', background=pallet.NAVY, foreground=pallet.RED, font=fonts['ui_bold']
    )
    # Status Bar
    style.configure('StatusBar.TFrame', background=pallet.NAVY_LT)
    style.configure(
        'StatusBar.TLabel', background=pallet.NAVY_LT, foreground='#C7D6E4', font=fonts['small']
    )


def _configure_lableframe(style: ttk.Style, pallet: type, fonts: dict):
    """LableFrame styled to look like a card."""
    style.configure(
        'Card.TLableframe',
        background=pallet.CARD,
        bordercolor=pallet.LINE,
        relief='solid',
        borderwidth=1,
    )
    style.configure(
        'Card.TLableframe.Label',
        background=pallet.CARD,
        foreground=pallet.ELECTRIC_BLUE_DK,
        font=fonts['h2'],
    )


def _configure_notebook(style: ttk.Style, pallet: type, fonts: dict):
    """Notebook tab styling — main top-level tabs and nested inner-card tabs."""
    style.configure('TNotebook', background=pallet.CANVAS, borderwidth=0, tabmargins=(2, 6, 2, 0))
    style.configure(
        'TNotebook.Tab',
        background=pallet.CANVAS,
        foreground=pallet.SLATE,
        padding=(14, 7),
        font=fonts['tab'],
        borderwidth=0,
    )
    style.map(
        'TNotebook.Tab',
        background=[('selected', pallet.CARD)],
        foreground=[('selected', pallet.ELECTRIC_BLUE_DK), ('active', pallet.INK)],
        expand=[('selected', (0, 0, 0, 0))],
    )

    # Inner notebook (Sub-pages)
    style.configure('Inner.TNotebook', background=pallet.CARD, borderwidth=0)
    style.configure(
        'Inner.TNotebook.Tab',
        background=pallet.CARD,
        foreground=pallet.SLATE,
        padding=(12, 6),
        font=fonts['tab'],
    )
    style.map(
        'Inner.TNotebook.Tab',
        background=[('selected', pallet.CARD)],
        foreground=[('selected', pallet.ELECTRIC_BLUE_DK), ('active', pallet.INK)],
    )


def _configure_buttons(style: ttk.Style, pallet: type, fonts: dict):
    """Configure the style for the different buttons used within the GUI."""
    # Secondary/Default
    style.configure(
        'TButton',
        background='#E7EDF2',
        foreground=pallet.INK,
        borderwidth=0,
        focusthickness=0,
        padding=(14, 7),
        font=fonts['ui_bold'],
    )
    style.map(
        'TButton',
        background=[('active', '#D7E0E8'), ('pressed', '#CBD6DF')],
    )

    # Primary/Electric Blue
    style.configure(
        'Primary.TButton',
        background=pallet.ELECTRIC_BLUE,
        foreground='#FFFFFF',
        borderwidth=0,
        padding=(16, 8),
        font=fonts['ui_bold'],
    )
    style.map(
        'Primary.TButton',
        background=[('active', pallet.ELECTRIC_BLUE_DK), ('pressed', pallet.ELECTRIC_BLUE_DK)],
        foreground=[('disabled', '#EAF6FB')],
    )

    # Danger/Red
    style.configure(
        'Danger.TButton',
        background=pallet.RED,
        foreground='#FFFFFF',
        borderwidth=0,
        padding=(16, 8),
        font=fonts['ui_bold'],
    )
    style.map(
        'Danger.TButton',
        background=[('active', pallet.RED_DK), ('pressed', pallet.RED_DK)],
    )

    # Subtle
    style.configure(
        'Subtle.TButton',
        background=pallet.CARD,
        foreground=pallet.SLATE,
        borderwidth=1,
        padding=(10, 5),
        font=fonts['ui'],
    )
    style.map(
        'Subtle.TButton',
        background=[('active', '#F0F4F7')],
        foreground=[('active', pallet.INK)],
        bordercolor=[('!disabled', pallet.LINE)],
    )


def _configure_inputs(style: ttk.Style, pallet: type):
    """Set the style for Entry/Combo/Spinbox inputs."""
    inputs = ['TEntry', 'TCombobox', 'TSpinbox']
    for input_type in inputs:
        style.configure(
            input_type,
            fieldbackground=pallet.FIELD,
            background=pallet.FIELD,
            foreground=pallet.INK,
            bordercolor=pallet.LINE,
            lightcolor=pallet.LINE,
            darkcolor=pallet.LINE,
            borderwidth=1,
            relief='solid',
            padding=5,
        )
        style.map(
            input_type,
            bordercolor=[('focus', pallet.ELECTRIC_BLUE)],
            lightcolor=[('focus', pallet.ELECTRIC_BLUE)],
        )
    style.configure('TCombobox', arrowcolor=pallet.SLATE)
    style.map(
        'TCombobox',
        fieldbackground=[('readonly', pallet.FIELD)],
        foreground=[('readonly', pallet.INK)],
    )


def _configure_checkbuttons(style: ttk.Style, pallet: type):
    style.configure(
        'Card.TCheckbutton',
        background=pallet.CARD,
        foreground=pallet.INK,
        focuscolor=pallet.CARD,
    )
    style.map(
        'Card.TCheckbutton',
        background=[('active', pallet.CARD)],
        foreground=[('active', pallet.ELECTRIC_BLUE_DK)],
    )
    style.configure(
        'Console.TCheckbutton',
        background=pallet.CARD,
        foreground=pallet.SLATE,
    )
    style.map('Console.TCheckbutton', background=[('active', pallet.CARD)])


def _configure_nav(style: ttk.Style, pallet: type, fonts: dict, ui_family: str) -> None:
    """Sidebar navigation frame/buttons."""
    style.configure('Nav.TFrame', background=pallet.CARD)
    style.configure(
        'NavHeader.TLabel',
        background=pallet.CARD,
        foreground=pallet.SLATE,
        font=(ui_family, 8, 'bold'),
    )
    style.configure(
        'Nav.TButton',
        background=pallet.CARD,
        foreground=pallet.INK,
        borderwidth=0,
        anchor='w',
        padding=(16, 8),
        font=fonts['ui'],
    )
    style.map(
        'Nav.TButton',
        background=[('active', '#EAF1F6')],
        foreground=[('active', pallet.ELECTRIC_BLUE_DK)],
    )
    style.configure(
        'NavActive.TButton',
        background='#E1F4FB',
        foreground=pallet.ELECTRIC_BLUE_DK,
        borderwidth=0,
        anchor='w',
        padding=(16, 8),
        font=fonts['ui_bold'],
    )
    style.map(
        'NavActive.TButton',
        background=[('active', '#D5EEF8'), ('pressed', '#D5EEF8')],
        foreground=[('active', pallet.ELECTRIC_BLUE_DK)],
    )


def _configure_scrollbar_separator(style: ttk.Style, p: type) -> None:
    """Set the Separator and scrollbar styling."""
    style.configure('TSeparator', background=p.LINE)
    style.configure(
        'Vertical.TScrollbar',
        background='#C3CED7',
        troughcolor=p.CANVAS,
        bordercolor=p.CANVAS,
        arrowcolor=p.SLATE,
        borderwidth=0,
    )
    style.map('Vertical.TScrollbar', background=[('active', p.SLATE)])


def apply_theme(root: tk.Tk):
    """Apply the theme to the GUI elements."""
    style = ttk.Style(root)

    with contextlib.suppress(tk.TclError):
        style.theme_use('calm')

    p = Palette
    ui_family = _pick_font(
        root, ['Segoe UI', 'SF Pro Text', 'Helvetica Neue', 'Inter', 'Arial'], 'Arial'
    )
    mono_family = _pick_font(
        root, ['SF Mono', 'Menlo', 'Consolas', 'DejaVu Sans Mono', 'Courier New'], 'Courier'
    )

    fonts = {
        'ui': (ui_family, 10),
        'ui_bold': (ui_family, 10, 'bold'),
        'small': (ui_family, 9),
        'h1': (ui_family, 16, 'bold'),
        'h2': (ui_family, 11, 'bold'),
        'tab': (ui_family, 10),
        'mono': (mono_family, 10),
    }

    _configure_tk_widget_default(root, p, fonts)
    _configure_base(style, p, fonts)
    _configure_labels(style, p, fonts)
    _configure_lableframe(style, p, fonts)
    _configure_notebook(style, p, fonts)
    _configure_buttons(style, p, fonts)
    _configure_inputs(style, p)
    _configure_checkbuttons(style, p)
    _configure_nav(style, p, fonts, ui_family)
    _configure_scrollbar_separator(style, p)

    return fonts
