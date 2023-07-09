import os
import sys
import time

import gnureadline as readline


class Writer:

    def __init__(self, command: str, default_name: str) -> None:

        self.wait_time: float = 0.1
        self.command = command
        self.default_name = default_name

    @staticmethod
    def rlinput(default_name: str, prefill: str = '') -> str:
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(default_name)
        finally:
            readline.set_startup_hook()

    def print_all(self) -> None:

        command_list = self.command.split()
        for com in command_list:
            print(com, end=" ", flush=True)
            time.sleep(self.wait_time)
        sys.stdout.write('\r')
        sys.stdout.flush()

    def main(self) -> None:

        self.print_all()
        self.rlinput(self.default_name)
