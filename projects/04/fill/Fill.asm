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

@8192
D=M
@num_repetitions
M=D
(CHECK_KEY_PRESSED)
    @KBD
    D=M
    @BLACKEN_SCREEN
    D;JGT
    @WHITEN_SCREEN
    0;JMP

(BLACKEN_SCREEN)
    @i
    M=0
    (BLK_INNER_LOOP)
    @i
    D=M
    @num_repetitions
    D=D-M
    @CHECK_KEY_PRESSED
    D;JEQ
    @i
    D=M
    @SCREEN
    A=A+D
    M=-1
    @i
    M=M+1
    @BLK_INNER_LOOP
    0;JMP

(WHITEN_SCREEN)
    @i
    M=0
    (WTE_INNER_LOOP)
    @i
    D=M
    @num_repetitions
    D=D-M
    @CHECK_KEY_PRESSED
    D;JEQ
    @i
    D=M
    @SCREEN
    A=A+D
    M=0
    @i
    M=M+1
    @WTE_INNER_LOOP
    0;JMP
