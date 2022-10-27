import sys
import lexer
import compiler

if sys.argv.__len__() < 3: print("read the docs"), exit(-1)

with open(sys.argv[1], "r") as infile:
    src = infile.read()
with open(sys.argv[2], "w") as file:
    file.write(compiler.compile(src))