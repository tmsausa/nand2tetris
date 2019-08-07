// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// time complexity: O(w * 2^w), where w is a word size
@result
M=0

(LOOP)
    @R1
    D=M
    @STORE
    D;JEQ

    D=D-1
    @R1
    M=D

    @R0
    D=M
    @result
    M=M+D
    @LOOP
    0;JMP

(STORE)
    @result
    D=M
    @R2
    M=D
(END)
    @END
    0;JMP