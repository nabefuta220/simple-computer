import sys

import ply.yacc as yacc

from asmlex import tokens

parser = yacc.yacc()
args = sys.argv

RESISTER = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0},
MEMORY = [0 for _ in range(256)]


if len(args) == 2:
    with open(args[1], "r", encoding='UTF-8') as f:
        while True:
            line = f.readline()
            if line:
                result = parser.parse(line)
            else:
                break
else:
    while True:
        try:
            s = input("SIMCOM> ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
