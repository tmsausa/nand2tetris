import logging
from logging import getLogger, StreamHandler
from collections import namedtuple
from pathlib import Path
from argparse import ArgumentParser
from typing import List, Union, Dict
from tqdm import tqdm


comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest_table = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump_table = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

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

AInstruction = namedtuple("AInstruction", ("value"))
AInstructionSymbol = namedtuple("AInstructionSymbol", ("name"))
CInsturction = namedtuple("CInstruction", ("dest", "comp", "jump"))
Label = namedtuple("Label", ("name"))
Instruction = Union[AInstruction, AInstructionSymbol, CInsturction, Label]

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def parse_assembly_with_emptylines_and_comments_removal(path_source: str) \
    -> List[Instruction]:
    list_instructions = []
    with open(path_source, "r") as fin:
        for line in fin:
            line = line.rstrip("\n")
            # If line is empty or a comment, ignore it.
            if not line or line.startswith("//"):
                continue
            # Clean the line, removing white spaces and comments.
            line = "".join(c for c in line.split("//")[0] if c != " ")
            if line.startswith("@") and line[1:].isnumeric():
                list_instructions.append(AInstruction(int(line[1:])))
            elif line.startswith("@"):
                list_instructions.append(AInstructionSymbol(line[1:]))
            elif line.startswith("("):
                list_instructions.append(Label(line[1:-1]))
            else:
                if "=" in line:
                    dest, line = line.split("=")
                else:
                    dest = "null"
                if ";" in line:
                    comp, jump = line.split(";")
                else:
                    comp = line
                    jump = "null"
                list_instructions.append(CInsturction(dest, comp, jump))
    return list_instructions


def add_labels(list_instructions: List[Instruction], symbol_table: Dict[str, int]) -> None:
    cur_instruction_idx = 0
    logger.info("Adding labels to the symbol table...")
    for instruction in tqdm(list_instructions):
        if isinstance(instruction, Label):
            symbol_table[instruction.name] = cur_instruction_idx
        else:
            cur_instruction_idx += 1


def translate_into_machine_code(list_instructions: List[Instruction],
    symbol_table: Dict[str, int]) -> List[str]:
    binary_representation = lambda x: bin(x)[2:].zfill(16)
    machine_code = []
    cur_instruction_idx = 0
    cur_variable_idx = 16
    logger.info("Translating into machine code...")
    for instruction in tqdm(list_instructions):
        if isinstance(instruction, AInstruction):
            translation = binary_representation(instruction.value)
            machine_code.append(translation)
        elif isinstance(instruction, CInsturction):
            translation = "111" + comp_table[instruction.comp] \
                + dest_table[instruction.dest] + jump_table[instruction.jump]
            machine_code.append(translation)
        elif isinstance(instruction, AInstructionSymbol) and instruction.name in symbol_table:
            translation = binary_representation(symbol_table[instruction.name])
            machine_code.append(translation)
        elif isinstance(instruction, AInstructionSymbol):
            symbol_table[instruction.name] = cur_variable_idx
            cur_variable_idx += 1
            translation = binary_representation(symbol_table[instruction.name])
            machine_code.append(translation)
        cur_instruction_idx += 1 if not isinstance(instruction, Label) else 0
    return machine_code


def main():
    parser = ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("-d", "--dest", type=str, default=None)
    args = parser.parse_args()

    list_instructions = parse_assembly_with_emptylines_and_comments_removal(args.source)
    add_labels(list_instructions, symbol_table)
    machine_code = translate_into_machine_code(list_instructions, symbol_table)
    path_to_save = args.dest if args.dest else args.source.replace(".asm", ".hack")
    with open(path_to_save, "w") as fout:
        fout.writelines([code + "\n" for code in machine_code])
    logger.info("Translation Done!")


if __name__ == "__main__":
    main()
