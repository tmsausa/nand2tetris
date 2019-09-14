from pathlib import Path
from argparse import ArgumentParser
from collections import namedtuple
from enum import Enum
from typing import Tuple


ARITHMETIC_OPERATIONS = {
    "add",
    "sub",
    "neg",
    "eq",
    "gt",
    "lt",
    "and",
    "or",
    "not"
}


class CommandType(Enum):
    ARITHMETIC = 0
    PUSH = 1
    POP = 2
    LABEL = 3
    GOTO = 4
    IF_GOTO = 5
    FUNCTION = 6
    RETURN = 7
    CALL = 8


Command = namedtuple("Command", ("ctype", "arg1", "arg2"))


def remove_entailing_commments(line: str) -> str:
    return line.split("//")[0]


class Parser:
    @staticmethod
    def _parse_command(line: str) -> Command:
        # translate a line, erasing comments.
        # This is the core of the class.
        line = remove_entailing_commments(line)
        blocks = line.split(" ")
        instruction = blocks[0]
        if instruction in ARITHMETIC_OPERATIONS:
            command_type = CommandType.ARITHMETIC
            arg1 = blocks[0]
            return Command(command_type, arg1, None)
        elif instruction in ("push", "pop"):
            command_type = CommandType.PUSH if instruction == "push" else CommandType.POP
            arg1, arg2 = blocks[1:3]
            return Command(command_type, arg1, arg2)
        elif instruction == "label":
            command_type = CommandType.LABEL
            arg1 = blocks[1]
            return Command(command_type, arg1, None)
        elif instruction == "goto":
            command_type = CommandType.GOTO
            arg1 = blocks[1]
            return Command(command_type, arg1, None)
        elif instruction == "if-goto":
            command_type = CommandType.IF_GOTO
            arg1 = blocks[1]
            return Command(command_type, arg1, None)
        else:
            raise NotImplementedError("Not implemented yet.")

    def __init__(self, path_vm: str):
        with open(path_vm, "r") as fin:
            self.num_lines = 0
            for line in fin:
                line = line.rstrip("\n")
                self.num_lines += 1 if line and not line.startswith("//") else 0
        self.fp = open(path_vm, "r")
        self.num_lines_read = 0
        self.command = None

    def has_more_commands(self) -> bool:
        return self.num_lines_read < self.num_lines

    def advance(self) -> None:
        if not self.has_more_commands():
            raise EOFError("File read.")
        line = self.fp.readline().rstrip("\n")
        self.num_lines_read += 1
        # Move to the next instruction.
        while (not line) or (line.startswith("//")):
            line = self.fp.readline().rstrip("\n")
        self.command = self._parse_command(line)

    @property
    def command_type(self) -> CommandType:
        return self.command.ctype

    @property
    def first_arg(self) -> str:
        return self.command.arg1

    @property
    def second_arg(self) -> int:
        return self.command.arg2

    @property
    def current_command(self) -> Command:
        return self.command

    def close(self) -> None:
        self.fp.close()


class CodeWriter:
    def __init__(self, path_asm: str):
        self.fp = open(path_asm, "w")
        self.file_name = Path(path_asm).stem
        self.function_name = None
        self.num_commands_written_so_far = 0

    def _writelines(self, translations):
        self.fp.writelines(translation + "\n" for translation in translations)
        self.num_commands_written_so_far += 1

    def write_arithmetic(self, command: Command) -> None:
        if not command.ctype == CommandType.ARITHMETIC:
            raise ValueError("An arithmetic command should be passed.")
        translations = ["// {}".format(command.arg1)]
        if command.arg1 in ("add", "sub", "and", "or"):
            translations.append("@SP")
            translations.append("M=M-1")
            translations.append("A=M")
            translations.append("D=M")
            translations.append("@SP")
            translations.append("A=M")
            translations.append("A=A-1")
            translations.append({
                "add": "M=D+M", "sub": "M=M-D", "and": "M=D&M", "or": "M=D|M"
            }[command.arg1])
        elif command.arg1 in ("eq", "gt", "lt"):
            translations.append("@SP")
            translations.append("M=M-1")
            translations.append("A=M")
            translations.append("D=M")
            translations.append("@SP")
            translations.append("A=M")
            translations.append("A=A-1")
            translations.append("M=M-D")
            translations.append("D=M")
            translations.append("@IF_TRUE_{}".format(self.num_commands_written_so_far))
            translations.append({
                "eq": "D;JEQ", "gt": "D;JGT", "lt": "D;JLT"
            }[command.arg1])
            translations.append("D=0")
            translations.append("@STORE_{}".format(self.num_commands_written_so_far))
            translations.append("0;JMP")
            translations.append("(IF_TRUE_{})".format(self.num_commands_written_so_far))
            translations.append("\tD=-1")
            translations.append("@STORE_{}".format(self.num_commands_written_so_far))
            translations.append("0;JMP")
            translations.append("(STORE_{})".format(self.num_commands_written_so_far))
            translations.append("\t@SP")
            translations.append("\tA=M")
            translations.append("\tA=A-1")
            translations.append("\tM=D")
        else:  # "neg" or "not"
            translations.append("@SP")
            translations.append("A=M")
            translations.append("A=A-1")
            translations.append({
                "neg": "M=-M", "not": "M=!M"
            }[command.arg1])
        self._writelines(translations)

    def write_push_pop(self, command: Command) -> None:
        if command.ctype not in (CommandType.PUSH, CommandType.POP):
            raise ValueError("A push or pop command should be passed.")
        translations = []
        if command.ctype == CommandType.PUSH:
            translations.append("// {} {} {}".format("push", command.arg1, command.arg2))
            if command.arg1 == "constant":
                translations.append("@{}".format(command.arg2))
                translations.append("D=A")
            elif command.arg1 in ("local", "argument", "this", "that"):
                translations.append("@{}".format(command.arg2))
                translations.append("D=A")
                translations.append({
                    "local": "@LCL", "argument": "@ARG", "this": "@THIS", "that": "@THAT"
                }[command.arg1])
                translations.append("A=D+M")
                translations.append("D=M")
            elif command.arg1 == "temp":
                addr = int(command.arg2) + 5
                translations.append("@{}".format(addr))
                translations.append("D=M")
            elif command.arg1 == "static":
                translations.append("@{}.{}".format(self.file_name, command.arg2))
                translations.append("D=M")
            else:  # pointer
                translations.append("@3" if command.arg2 == "0" else "@4")
                translations.append("D=M")
            translations.append("@SP")
            translations.append("A=M")
            translations.append("M=D")
            translations.append("@SP")
            translations.append("M=M+1")
        else:  # pop
            translations.append("// {} {} {}".format("pop", command.arg1, command.arg2))
            if command.arg1 == "constant":
                raise ValueError("Constant cannot be pushed.")
            elif command.arg1 in ("local", "argument", "this", "that"):
                translations.append("@{}".format(command.arg2))
                translations.append("D=A")
                translations.append({
                    "local": "@LCL", "argument": "@ARG", "this": "@THIS", "that": "@THAT"
                }[command.arg1])
                translations.append("A=D+M")
            elif command.arg1 == "temp":
                translations.append("@{}".format(int(command.arg2) + 5))
            elif command.arg1 == "static":
                translations.append("@{}.{}".format(self.file_name, command.arg2))
            else:  # pointer
                translations.append("@3" if command.arg2 == "0" else "@4")
            translations.append("D=A")
            translations.append("@addr")
            translations.append("M=D")
            translations.append("@SP")
            translations.append("M=M-1")
            translations.append("A=M")
            translations.append("D=M")
            translations.append("@addr")
            translations.append("A=M")
            translations.append("M=D")
        self._writelines(translations)

    def write_label(self, command: Command) -> None:
        if command.ctype != CommandType.LABEL:
            raise ValueError("A label command should be passed.")
        label = command.arg1
        translations = []
        translations.append("// label {}".format(label))
        if self.function_name:
            # TODO: If this line is within a function, then the appropriate name would be
            # {}.{}${}.format(file_name, function_name, label)
            translations.append("({}.{}${})".format(self.file_name, self.function_name, label))
        else:
            translations.append("({}${})".format(self.file_name, label))
        self._writelines(translations)

    def write_goto(self, command: Command) -> None:
        if command.ctype != CommandType.GOTO:
            raise ValueError("A goto comand should be passed.")
        label = "{}.{}${}".format(self.file_name, self.function_name, command.arg1) if self.function_name \
            else "{}${}".format(self.file_name, command.arg1)
        translations = []
        translations.append("// goto {}".format(label))
        translations.append("@{}".format(label))
        translations.append("0;JMP")
        self._writelines(translations)

    def write_if(self, command: Command) -> None:
        if command.ctype != CommandType.IF_GOTO:
            raise ValueError("A if-goto command should be passed.")
        label = "{}.{}${}".format(self.file_name, self.function_name, command.arg1) if self.function_name \
            else "{}${}".format(self.file_name, command.arg1)
        translations = []
        translations.append("// if-goto {}".format(label))
        translations.append("@SP")
        translations.append("M=M-1")
        translations.append("A=M")
        translations.append("D=M")
        translations.append("@{}".format(label))
        translations.append("D;JNE")
        self._writelines(translations)

    def close(self) -> None:
        self.fp.close()


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("path", type=str, help="Path to a source vm file or directory")
    args = arg_parser.parse_args()

    path = Path(args.path)
    if path.is_file():
        parser = Parser(args.path)
        dest = args.path.replace(".vm", ".asm")
        code_writer = CodeWriter(dest)
        while parser.has_more_commands():
            parser.advance()
            if parser.command_type == CommandType.ARITHMETIC:
                code_writer.write_arithmetic(parser.current_command)
            elif parser.command_type in (CommandType.PUSH, CommandType.POP):
                code_writer.write_push_pop(parser.current_command)
            elif parser.command_type == CommandType.LABEL:
                code_writer.write_label(parser.current_command)
            elif parser.command_type == CommandType.GOTO:
                code_writer.write_goto(parser.current_command)
            elif parser.command_type == CommandType.IF_GOTO:
                code_writer.write_if(parser.current_command)


if __name__ == "__main__":
    main()
