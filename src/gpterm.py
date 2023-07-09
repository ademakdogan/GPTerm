import argparse
import getpass
import os
import subprocess

from llm_writer import Writer
from responser import ShellResponser


class GPTerm:

    def __init__(self) -> None:

        self.cwd = os.getcwd()
        username = getpass.getuser()
        self.bot_name = username + '_AI --->:'

    @staticmethod
    def check_path(path: str) -> bool:

        if not os.path.exists(path):
            #return "", f"cd: no such file or directory: {path}\n", 1
            raise Exception(f"cd: no such file or directory: {path}\n")
        if not os.path.isdir(path):
            #return "", f"cd: {path} is not a directory\n", 1
            raise Exception(f"cd: {path} is not a directory\n")
        if not os.access(path, os.X_OK):
            #return "", f"cd: permission denied: {path}\n", 1
            raise Exception(f"cd: permission denied: {path}\n")

        return True

    def command_executer(self, command: str) -> None:

        command_pieces = command.split()
        res = subprocess.call(command, shell=True, cwd=self.cwd)
        temp_path = self.cwd
        if res == 0:
            if 'cd' in command_pieces:
                elem_idx = [
                    i for i, e in enumerate(command_pieces) if e == 'cd'
                ]
                for idx in elem_idx:
                    if idx == len(command_pieces) - 1:
                        pass
                    else:
                        target_path = command_pieces[idx + 1]
                        if target_path.startswith('/'):
                            # update old path
                            if GPTerm.check_path(target_path) is True:
                                temp_path = target_path
                        else:
                            target_path = os.path.join(self.cwd, target_path)
                            if GPTerm.check_path(target_path) is True:
                                temp_path = target_path
        self.cwd = temp_path
        self.cwd = os.path.normpath(self.cwd)


def main() -> None:

    ap = argparse.ArgumentParser()
    ap.add_argument("-m",
                    "--model",
                    required=False,
                    help="chatgpt, alpaca, wizard or mpt",
                    default="chatgpt")
    ap.add_argument(
        "-p",
        "--model_path",
        required=False,
        help=
        "path of your local llm model (use this if you don't select 'chatgpt' as a model type.)",
        default=None)
    ap.add_argument(
        "-k",
        "--openai_key",
        required=False,
        help=
        "openai api key (use this if you select 'chatgpt' as a model type.)",
        default=None)
    ap.add_argument("-d",
                    "--device",
                    required=False,
                    help="cpu, mps or cuda",
                    default='cpu')

    args = vars(ap.parse_args())

    #-----
    gpterm = GPTerm()
    prefill = ''
    shell_responser = ShellResponser(model_type=args['model'],
                                     model_path=args['model_path'],
                                     openai_key=args['openai_key'],
                                     device=args['device'])
    while True:
        command = Writer.rlinput(gpterm.bot_name, prefill)
        if command == 'q' or command == 'quit':
            break
        elif len(command.strip()) == 0:
            pass
        elif command.split()[0] == '.':
            llm_result = shell_responser.prompt_to_command(command)
            command = llm_result['command']
            Writer(command=command, default_name=gpterm.bot_name).print_all()
            prefill = command
        else:
            gpterm.command_executer(command=command)
            prefill = ''


if __name__ == '__main__':

    main()
