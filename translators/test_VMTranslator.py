import unittest
from pathlib import Path
from VMTranslator import Parser, CodeWriter, Command, CommandType


class TestParser(unittest.TestCase):
    def test_simpleadd(self):
        path_vm = "../projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm"
        parser = Parser(path_vm)
        self.assertEqual(parser.num_lines, 3)
        self.assertTrue(parser.has_more_commands())
        first_command = Command(CommandType.PUSH, "constant", "7")
        second_command = Command(CommandType.PUSH, "constant", "8")
        third_command = Command(CommandType.ARITHMETIC, "add", None)
        for command in (first_command, second_command, third_command):
            parser.advance()
            self.assertEqual(parser.command, command)
        self.assertEqual(parser.num_lines_read, 3)
        parser.close()

    def test_stacktest(self):
        path_vm = "../projects/07/StackArithmetic/StackTest/StackTest.vm"
        parser = Parser(path_vm)
        self.assertEqual(parser.num_lines, 38)
        command_sequence = []
        command_sequence.append(Command(CommandType.PUSH, "constant", "17"))
        command_sequence.append(Command(CommandType.PUSH, "constant", "17"))
        command_sequence.append(Command(CommandType.ARITHMETIC, "eq", None))
        command_sequence.append(Command(CommandType.PUSH, "constant", "17"))
        command_sequence.append(Command(CommandType.PUSH, "constant", "16"))
        command_sequence.append(Command(CommandType.ARITHMETIC, "eq", None))
        for command in command_sequence:
            parser.advance()
            self.assertEqual(parser.command, command)
        parser.close()

    def test_basictest(self):
        path_vm = "../projects/07/MemoryAccess/BasicTest/Basictest.vm"
        parser = Parser(path_vm)
        self.assertEqual(parser.num_lines, 25)
        command_sequence = []
        command_sequence.append(Command(CommandType.PUSH, "constant", "10"))
        command_sequence.append(Command(CommandType.POP, "local", "0"))
        command_sequence.append(Command(CommandType.PUSH, "constant", "21"))
        command_sequence.append(Command(CommandType.PUSH, "constant", "22"))
        command_sequence.append(Command(CommandType.POP, "argument", "2"))
        for command in command_sequence:
            parser.advance()
            self.assertEqual(parser.command, command)
        parser.close()


class TestCodeGenerator(unittest.TestCase):
    def test1(self):
        temp_path = "./temp.asm"
        code_writer = CodeWriter(temp_path)
        command_sequence = [
            Command(CommandType.PUSH, "constant", "1"),
            Command(CommandType.PUSH, "constant", "2"),
            Command(CommandType.ARITHMETIC, "add", None)
        ]
        for command in command_sequence:
            if command.ctype == CommandType.ARITHMETIC:
                code_writer.write_arithmetic(command)
            elif command.ctype in (CommandType.PUSH, CommandType.POP):
                code_writer.write_push_pop(command)
        code_writer.close()

        answer = [
            "// push constant 1",
            "@1",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "// push constant 2",
            "@2",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "// add",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "A=M",
            "A=A-1",
            "M=D+M",
        ]
        with open(temp_path, "r") as fin:
            for i, line in enumerate(fin):
                line = line.rstrip("\n")
                self.assertEqual(line, answer[i])
        Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
