import lexer
import compiler

with open("input.ffk", "r") as infile:
    src = infile.read()
with open("out.urcl", "w") as file:
    file.write(compiler.compile(src))