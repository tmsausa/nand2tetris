import unittest
from tempfile import NamedTemporaryFile
from assemble import parse_assembly_with_emptylines_and_comments_removal, add_labels, \
    translate_into_machine_code, main, AInstruction, AInstructionSymbol, CInsturction, Label


class TestParseAssemblyWithEmptyLinesAndCommentRemoval(unittest.TestCase):
    def test_add(self):
        path = "../projects/06/add/Add.asm"
        result = parse_assembly_with_emptylines_and_comments_removal(path)
        ans = [
            AInstruction(2),
            CInsturction("D", "A", "null"),
            AInstruction(3),
            CInsturction("D", "D+A", "null"),
            AInstruction(0),
            CInsturction("M", "D", "null")
        ]
        self.assertEqual(result, ans)

    def test_maxL(self):
        path = "../projects/06/max/MaxL.asm"
        result = parse_assembly_with_emptylines_and_comments_removal(path)
        ans = [
            AInstruction(0),
            CInsturction("D", "M", "null"),
            AInstruction(1),
            CInsturction("D", "D-M", "null"),
            AInstruction(10),
            CInsturction("null", "D", "JGT"),
            AInstruction(1),
            CInsturction("D", "M", "null"),
            AInstruction(12),
            CInsturction("null", "0", "JMP"),
            AInstruction(0),
            CInsturction("D", "M", "null"),
            AInstruction(2),
            CInsturction("M", "D", "null"),
            AInstruction(14),
            CInsturction("null", "0", "JMP")
        ]
        self.assertEqual(result, ans)

    def test_max(self):
        path = "../projects/06/max/Max.asm"
        result = parse_assembly_with_emptylines_and_comments_removal(path)
        ans = [
            AInstructionSymbol("R0"),
            CInsturction("D", "M", "null"),
            AInstructionSymbol("R1"),
            CInsturction("D", "D-M", "null"),
            AInstructionSymbol("OUTPUT_FIRST"),
            CInsturction("null", "D", "JGT"),
            AInstructionSymbol("R1"),
            CInsturction("D", "M", "null"),
            AInstructionSymbol("OUTPUT_D"),
            CInsturction("null", "0", "JMP"),
            Label("OUTPUT_FIRST"),
            AInstructionSymbol("R0"),
            CInsturction("D", "M", "null"),
            Label("OUTPUT_D"),
            AInstructionSymbol("R2"),
            CInsturction("M", "D", "null"),
            Label("INFINITE_LOOP"),
            AInstructionSymbol("INFINITE_LOOP"),
            CInsturction("null", "0", "JMP")
        ]
        self.assertEqual(result, ans)


class TestAddLabels(unittest.TestCase):
    def test_max(self):
        symbol_table = {}
        path = "../projects/06/max/Max.asm"
        list_instructions = parse_assembly_with_emptylines_and_comments_removal(path)
        add_labels(list_instructions, symbol_table)
        ans = {"OUTPUT_FIRST": 10, "OUTPUT_D": 12, "INFINITE_LOOP": 14}
        self.assertEqual(symbol_table, ans)


class TestTranslateIntoMachineCode(unittest.TestCase):
    def test_add(self):
        path = "../projects/06/add/Add.asm"
        line_instructions = parse_assembly_with_emptylines_and_comments_removal(path)
        machine_code = translate_into_machine_code(line_instructions, {})
        ans = [
            '0000000000000010',
            '1110110000010000',
            '0000000000000011',
            '1110000010010000',
            '0000000000000000',
            '1110001100001000'
        ]
        self.assertEqual(machine_code, ans)

    def test_max(self):
        symbol_table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }
        for i in range(16):
            symbol_table["R" + str(i)] = i
        path = "../projects/06/max/Max.asm"
        line_instructions = parse_assembly_with_emptylines_and_comments_removal(path)
        add_labels(line_instructions, symbol_table)
        machine_code = translate_into_machine_code(line_instructions, symbol_table)
        ans = [
            '0000000000000000',
            '1111110000010000',
            '0000000000000001',
            '1111010011010000',
            '0000000000001010',
            '1110001100000001',
            '0000000000000001',
            '1111110000010000',
            '0000000000001100',
            '1110101010000111',
            '0000000000000000',
            '1111110000010000',
            '0000000000000010',
            '1110001100001000',
            '0000000000001110',
            '1110101010000111'
        ]
        self.assertEqual(len(machine_code), len(ans))
        self.assertEqual(machine_code, ans)


if __name__ == "__main__":
    unittest.main()
