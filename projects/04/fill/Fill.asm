// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// set n 8192 = 2^13.
    @n
    M=1
    D=M
    D=M+D
    M=D // 2
    D=D+M
    M=D // 4
    D=D+M
    M=D // 8
    D=D+M
    M=D // 16
    D=D+M
    M=D // 32
    D=D+M
    M=D // 64
    D=D+M
    M=D // 128
    D=D+M
    M=D // 256
    D=D+M
    M=D // 512
    D=D+M
    M=D // 1024
    D=D+M
    M=D // 2048
    D=D+M
    M=D // 4096
    D=D+M
    M=D // 8192

(CHECKKEYPRESSED)
    @KBD
    D=M
    @BLACKSCREEN
    D;JNE
    @WHITESCREEN
    0;JMP

(BLACKSCREEN)
    @SCREEN
    D=A
    @i
    M=0
    (LOOPBLACK)
        @i
        D=M
        @n
        D=D-M
        @CHECKKEYPRESSED
        D;JEQ

        @i
        D=M
        @SCREEN
        A=A+D
        M=-1
        @i
        M=M+1
        @LOOPBLACK
        0;JMP

(WHITESCREEN)
    @SCREEN
    D=A
    @i
    M=0
    (LOOPWHITE)
    @i
    D=M
    @n
    D=D-M
    @CHECKKEYPRESSED
    D;JEQ

    @i
    D=M
    @SCREEN
    A=A+D
    M=0
    @i
    M=M+1
    @LOOPWHITE
    0;JMP
