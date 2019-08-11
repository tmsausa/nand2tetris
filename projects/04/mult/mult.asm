// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// time complexity: O(w * 2^w), where w is a word size
@R2
M=0
@R1
D=M
@remaining_num_repetitions
M=D
(LOOP)
    @remaining_num_repetitions
    D=M
    @INFINITE_LOOP
    D;JEQ
    @R0
    D=M
    @R2
    M=D+M
    @remaining_num_repetitions
    M=M-1
    @LOOP
    0;JMP

(INFINITE_LOOP)
    @INFINITE_LOOP
    0;JMP
