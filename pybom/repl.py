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

    def do_quit(self, arg: str) -> bool:
        '''Exit the REPL.'''
        return True

    def do_EOF(self, arg: str) -> bool:
        '''Exit on Ctrl-D (Ctrl-Z on Windows).'''
        print()
        return True

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
