// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// time complexity: O(w^2), where w is a word size

// base preprocessing
    @result
    M=0
    @current_base_R0
    M=-1
    @current_base_R1
    M=-1

    D=1
    @base_arr
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D
    D=D+M
    A=A+1
    M=D

    @result
    M=0
    @current_base_R0
    M=-1

(LOOP1)
    @current_base_R0
    M=M+1
    D=M

    @15
    D=D-A
    @PREEND
    D;JEQ

    @current_base_R0
    D=M
    @base_arr
    A=A+D
    D=M

    @R0
    D=D&M
    @LOOP1
    D;JEQ

    @current_base_R1
    M=-1
    (LOOP2)
        @current_base_R1
        M=M+1
        D=M

        @15
        D=D-A
        @LOOP1
        D;JEQ

        @current_base_R1
        D=M
        @base_arr
        A=A+D
        D=M

        @R1
        D=D&M
        @LOOP2
        D;JEQ

        @current_base_R0
        D=M
        @current_base_R1
        D=D+M
        @base_arr
        A=A+D
        D=M
        @result
        M=M+D

        @LOOP2
        0;JEQ

(PREEND)
    @result
    D=M
    @R2
    M=D
    @END
    0;JMP
(END)
    @END
    0;JMP