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

"""The base tab layout that is used within the GUI."""

import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from ..helpers import command_runner, pretty_json
from .style import Palette


class BaseTab(ttk.Frame):
    """Console output."""

    def __init__(self, parent: ttk.Notebook):
        super().__init__(parent, style='TFrame', padding=Palette.PADDING)
        self._queue: queue.Queue[tuple[str, str, bool]] = queue.Queue()
        self.pretty_var = tk.BooleanVar(value=False)
        self._on_done = None
        self._cmd_display = ''

        self._paned = ttk.PanedWindow(self, orient='vertical')
        self._paned.pack(fill='both', expand=True)

        self._top = top = ttk.Frame(self._paned, style='TFrame')
        self.body = ttk.Frame(top, style='TFrame')
        self.body.pack(fill='x')
        self._paned.add(top, weight=0)

    def _build_console(self):
        """Build the Banshee console."""
        wrap = ttk.LabelFrame(self._paned, text='Output', style='Card.TLabelframe', padding=10)
        self._paned.add(wrap, weight=1)
        self._paned.bind('<Map>', self._set_initial_sash, add='+')

        toolbar = ttk.Frame(wrap, style='Card.TFrame')
        toolbar.pack(fill='x', pady=(0, 8))
        ttk.Checkbutton(
            toolbar,
            text='Pretty output (-p)',
            variable=self.pretty_var,
            style='Console.TCheckbutton',
        ).pack(side='left')
        ttk.Button(toolbar, text='Clear', command=self._clear_output, style='Subtle.TButton').pack(
            side='right'
        )
        ttk.Button(
            toolbar, text='Copy Output', command=self._copy_output, style='Subtle.TButton'
        ).pack(side='right', padx=(0, 6))
        ttk.Button(
            toolbar, text='Copy Command', command=self._copy_cmd, style='Subtle.TButton'
        ).pack(side='right', padx=(0, 6))

        console = ttk.Frame(wrap, style='Card.TFrame')
        console.pack(fill='both', expand=True)
        console.rowconfigure(0, weight=1)
        console.columnconfigure(0, weight=1)
        self.output = tk.Text(
            console,
            wrap='none',
            height=16,
            bd=0,
            relief='flat',
            background=Palette.CONSOLE_BG,
            foreground=Palette.CONSOLE_FG,
            insertbackground=Palette.CONSOLE_FG,
            font=('TkFixedFont',),
            padx=12,
            pady=10,
            state='disabled',
        )
        self.output.grid(row=0, column=0, sticky='nsew')
        y_scroll_bar = ttk.Scrollbar(console, orient='vertical', command=self.output.yview)
        y_scroll_bar.grid(row=0, column=1, sticky='ns')
        x_scroll_bar = ttk.Scrollbar(console, orient='horizontal', command=self.output.xview)
        x_scroll_bar.grid(row=1, column=0, sticky='ew')

        self.output.configure(yscrollcommand=y_scroll_bar.set, xscrollcommand=x_scroll_bar.set)
        self.output.tag_configure('muted', foreground='#6F8298')
        self.output.tag_configure('error', foreground='#FF6B6B')
        self.output.tag_configure('accent', foreground=Palette.CONSOLE_ACCENT)
        self.output.tag_configure('cmd', foreground=Palette.CONSOLE_ACCENT)
        self.output.tag_configure('prompt', foreground='#5AD16A')

    def _set_initial_sash(self, _event=None):
        """Size the form pane to its content once the paned window is actually on screen."""
        self._paned.unbind('<Map>')
        self.update_idletasks()
        self._paned.sashpos(0, self._top.winfo_reqheight())

    def _set_output(self, text: str, tag: str | None = None):
        """Replace the console with text, rather then blank."""
        self.output.configure(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('end', text, tag or ())
        self.output.configure(state='disabled')

    def _clear_output(self):
        """Clear text from the console."""
        self._set_output('')

    def _copy_output(self):
        """Copy any output text that is being displayed from the console."""
        self.clipboard_clear()
        self.clipboard_append(self.output.get('1.0', 'end'))

    def _copy_cmd(self):
        """Copy the Banshee command being run in the console."""
        cmd = (self._cmd_display or '').strip()
        if not cmd:
            messagebox.showinfo('Copy command', 'Run a command first — nothing to copy yet.')
            return
        self.clipboard_clear()
        self.clipboard_append(cmd)

    def _console(self, cmd: str, body: str, body_tag=None):
        """Render the command and the output into the console."""
        self._cmd_display = cmd
        self.output.configure(state='normal')
        self.output.delete('1.0', 'end')
        if cmd:
            self.output.insert('end', '$', 'prompt')
            self.output.insert('end', f'{cmd}\n', 'cmd')
            self.output.insert('end', '─' * 60 + '\n', 'muted')

        self.output.insert('end', body, body_tag or ())
        self.output.configure(state='disabled')
        self.output.see('1.0')

    def _console_note(self, note_text: str):
        """Add a accent-coloured note to existing text within the console."""
        self.output.configure(state='normal')
        self.output.insert('end', note_text, 'accent')
        self.output.configure(state='disabled')
        self.output.see('end')

    # Run commands
    def _showcommand_runnerning_command(self, cmd_display: str):
        self._cmd_display = cmd_display
        self.output.configure(state='normal')
        self.output.delete('1.0', 'end')
        if cmd_display:
            self.output.insert('end', '$', 'prompt')
            self.output.insert('end', f'{cmd_display}\n', 'cmd')
            self.output.insert('end', '─' * 60 + '\n', 'muted')
        self.output.insert('end', '⟳  running…', 'muted')
        self.output.configure(state='disabled')

    def command_runner_async(
        self,
        args: list[str],
        stdin_text: str | None = None,
        on_done=None,
        allow_pretty: bool = True,
    ):
        """Run a Banshee command in a background thread and show the result."""
        pretty = self.pretty_var.get() and allow_pretty
        if pretty and '-p' not in args:
            args.append('-p')
        self._on_done = on_done
        self._showcommand_runnerning_command('banshee ' + ' '.join(args))

        def worker():
            stdout, stderr = command_runner(args, stdin_text)
            self._queue.put((stdout, stderr, pretty))

        threading.Thread(target=worker, daemon=True).start()
        self.after(80, self._poll)

    def _pipe_async(self, first_command: list[str], second_command: list[str]):
        """Run a banshee command and then pipe the output into another command."""
        self._on_done = None
        self._showcommand_runnerning_command(
            f'banshee {" ".join(first_command)} | banshee {" ".join(second_command)}'
        )

        def worker():
            out, err = command_runner(first_command)
            if err and not out:
                self._q.put((out, err, False))
                return
            out2, err2 = command_runner(second_command, stdin_text=out)
            self._q.put((out2, err + err2, False))

        threading.Thread(target=worker, daemon=True).start()
        self.after(80, self._poll)

    def _poll(self):
        """Check to see if the command has finished running."""
        try:
            stdout, stderr, pretty = self._queue.get_nowait()
        except queue.Empty:
            self.after(80, self._poll)
            return

        self.output.configure(state='normal')
        self.output.delete('1.0', 'end')
        if self._cmd_display:
            self.output.insert('end', '$ ', 'prompt')
            self.output.insert('end', f'{self._cmd_display}\n', 'cmd')
            self.output.insert('end', f'{"─" * 60}\n', 'muted')

        if stdout.strip():
            self.output.insert('end', stdout if pretty else pretty_json(stdout))

        if stderr.strip():
            self.output.insert('end', '── stderr ──\n', 'error')
            self.output.insert('end', stderr, 'error')

        if not stdout.strip() and not stderr.strip():
            self.output.insert('end', '(no output)', 'muted')
        self.output.configure(state='disabled')
