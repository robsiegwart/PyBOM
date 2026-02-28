'''
Interactive REPL mode for pyBOM.

Launched when ``pybom`` is run with no arguments or a bare directory path.
Uses :mod:`cmd` from the standard library so no additional dependencies are
required.
'''

import os
import sys
import cmd
from .BOM import BOM


WELCOME = (
    "pyBOM interactive mode  (type 'help' for commands, 'quit' to exit)\n"
    "Directory: {directory}\n"
)


class BomRepl(cmd.Cmd):
    '''Interactive BOM shell.'''

    prompt = 'pybom> '

    def __init__(self, bom: BOM, directory: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bom = bom
        self.directory = directory

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def do_tree(self, arg: str) -> None:
        '''Display the BOM hierarchy as an ASCII tree.'''
        print(self.bom.tree)

    def do_parts(self, arg: str) -> None:
        '''List all unique parts in the BOM with PN, Name, and Description.'''
        counts = self.bom.aggregate
        if not counts:
            print('No parts found.')
            return
        df = self.bom.parts_db.df.copy()
        df = df[df['PN'].isin(counts)]
        cols = ['PN'] + [c for c in ('Name', 'Description') if c in df.columns]
        print(df[cols].to_string(index=False))

    def do_assemblies(self, arg: str) -> None:
        '''List all assemblies in the BOM hierarchy with PN and name.'''
        all_assemblies = self._collect_assemblies(self.bom)
        rows = []
        for asm in all_assemblies:
            pn = asm.PN or ''
            rows.append((pn, asm.Name or ''))

        if not rows:
            print('No assemblies found.')
            return

        pn_width = max(len(r[0]) for r in rows) + 2
        has_names = any(r[1] for r in rows)
        if has_names:
            for pn, name in rows:
                print(f'{pn:{pn_width}}{name}')
        else:
            for pn, _ in rows:
                print(pn)

    def do_summary(self, arg: str) -> None:
        '''Display the aggregated BOM summary table.'''
        try:
            df = self.bom.summary
        except Exception as e:
            print(f'Error: {e}')
            return
        df = df.dropna(axis=1, how='all')
        print(df.to_string(index=False))

    def do_browse(self, arg: str) -> None:
        '''Open the interactive TUI browser for this BOM.'''
        from .browser import BomBrowserApp
        BomBrowserApp(self.bom).run()

    def do_quit(self, arg: str) -> bool:
        '''Exit the REPL.'''
        return True

    def do_EOF(self, arg: str) -> bool:
        '''Exit on Ctrl-D (Ctrl-Z on Windows).'''
        print()
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _collect_assemblies(self, bom: BOM, result: list | None = None) -> list:
        '''Recursively collect all BOM nodes in depth-first order.'''
        if result is None:
            result = []
        result.append(bom)
        for sub in bom.assemblies:
            self._collect_assemblies(sub, result)
        return result

    # ------------------------------------------------------------------
    # Behavioural overrides
    # ------------------------------------------------------------------

    def emptyline(self) -> None:
        # Suppress the default "repeat last command" behaviour.
        pass

    def default(self, line: str) -> None:
        print(f"Unknown command: {line!r}  (type 'help' for commands)")


def run_repl(directory: str = '.') -> None:
    '''
    Load BOMs from *directory*, print the welcome banner and BOM tree, then
    enter the interactive command loop.

    :param str directory: Path to the folder containing BOM Excel files.
                          Defaults to the current working directory.
    '''
    directory = os.path.abspath(directory)
    print(WELCOME.format(directory=directory))

    try:
        bom = BOM.from_folder(directory)
    except FileNotFoundError:
        print(f"Error: No 'Parts list.xlsx' found in {directory}")
        print('Make sure the directory contains BOM Excel files.')
        sys.exit(1)
    except Exception as e:
        print(f'Error loading BOM: {e}')
        sys.exit(1)

    print(bom.tree)
    print()
    BomRepl(bom=bom, directory=directory).cmdloop()
