import re
import sys
from typing import Callable

import ply.yacc as yacc

from asmlex import tokens

parser = yacc.yacc()
args = sys.argv

WARD_BIT = 8
MEMORY_BIT = 8

RESISTER = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0},
MEMORY = [0 for _ in range(1 << WARD_BIT)]

OVERFLOW = 0
CARRY = 0
SIGN = 0
ZERO = 0


def calc(value1: int, value2: int, operator: int):
    global RESISTER
    global OVERFLOW, CARRY, SIGN, ZERO
    operator %= 8
    result = 0
    if operator == 0:
        result = value1+1
    if operator == 1:
        result = value1+value2
    if operator == 2:
        result = value1-value2
    if operator == 3:
        result = value1-1
    if operator == 4:
        result = value1 | value2
    if operator == 5:
        result = value1 ^ value2
    if operator == 6:
        result = value1 & value2
    if operator == 7:
        result = ~value1
    SIGN = result < 0
    ZERO = result == 0
    CARRY=not (0 <=result <(1<<MEMORY_BIT))
    OVERFLOW = not(-(1 << MEMORY_BIT) <= result <= ((1 << MEMORY_BIT)-1))
    result &= ((1 << MEMORY_BIT)-1)
    RESISTER['1'] = result


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
