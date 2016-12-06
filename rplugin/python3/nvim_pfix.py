"""nvim-pfix neovim plugin."""

from collections import defaultdict
import subprocess

import neovim
from neovim.api.nvim import NvimError


@neovim.plugin
class Main(object):
    """Plugin Main"""

    PFIX_BUFFER = '_-_PFIX_-_'

    def __init__(self, vim):
        self.vim = vim
        self.commands = None

    @neovim.command('Pfind', range='', nargs='*', sync=True)
    def project_find(self, args, range):
        """Find all instances of search query in project files and load into
        buffer self.PFIX_BUFFER."""
        self.commands = defaultdict(bool)
        if not args:
            try:
                args.append(self._ask('Enter search query: '))
            except NvimError:
                return
        cmd = self.vim.vars.get('nvim_pfix_pfind', 'grep')
        cmd_opts = self.vim.vars.get(
            'nvim_pfix_pfind_opts', '--recursive --line-number').split()
        cmd_opts.insert(0, cmd)
        cmd_opts.append(' '.join(args))
        cmd_opts.append('.')
        s = subprocess.run(cmd_opts, stdout=subprocess.PIPE)
        out = s.stdout.decode('utf-8').split('\n')
        buffer_height = int(self.vim.vars.get('nvim_pfix_buffer_height', 10))
        self.vim.command('split {0}'.format(self.PFIX_BUFFER))
        self.vim.command('buffer {0}'.format(self.PFIX_BUFFER))
        self.vim.command('resize {0}'.format(buffer_height))
        self.vim.command('set buftype=nofile')
        self.vim.current.buffer[:] = out

    @neovim.command('Pfix', range='', nargs='*', sync=True)
    def project_replace(self, args, range):
        """Replace lines in project files with edits from self.PFIX_BUFFER."""
        if self.vim.funcs.bufloaded(self.PFIX_BUFFER):
            self.vim.command('buffer {0}'.format(self.PFIX_BUFFER))
        else:
            self.vim.command('echohl WarningMsg')
            self.vim.command('echo ":Pfind must be run before :Pfix"')
            self.vim.command('echohl None')
            return

        for line in self.vim.current.buffer:
            choice = ''
            try:
                filename, lineno, contents = line.split(':', 2)
            except ValueError:
                continue
            try:
                self.vim.command('buffer +{0} {1}'.format(lineno, filename))
            except neovim.api.nvim.NvimError:
                self.vim.command('edit +{0} {1}'.format(lineno, filename))
            self.vim.command('redraw')

            if contents == self.vim.current.line:
                continue

            if self.commands['doall']:
                self.vim.current.line = contents
                continue

            choice = self._ask(
                "Replace with `{0}`? [y/n/a/Q] ".format(contents))
            choice = choice.lower()
            if choice in ('y', 'a'):
                self.vim.current.line = contents
                self.commands['doall'] = choice == 'a'
                self.commands['changes'] = True
            elif choice == 'n':
                continue
            else:  # q or any unknown input
                break

        try:
            choice = ''
            self.vim.command('redraw')
            if self.commands['changes']:
                choice = self._ask("Write all buffers? [y/N] ")
            if choice.lower() == 'y':
                self.vim.command('wall')
            self.vim.command('buffer {0}'.format(self.PFIX_BUFFER))
            self.vim.command('bdelete {0}'.format(self.PFIX_BUFFER))
        except NvimError:
            pass

    def _ask(self, question):
        """Prompt user for input with `question`."""
        self.vim.command('echohl Question')
        try:
            choice = self.vim.funcs.input(question)
        except NvimError:
            choice = ''
        finally:
            self.vim.command('echohl None')
        return choice

