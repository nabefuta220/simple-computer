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
<<<<<<< Updated upstream
    operator %= 8
=======
    value1_sign = (value1 & ((1 << MEMORY_BIT-1)-1)) + (-1) * \
        (bool(value1 & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1)
    value2_sign = (value2 & ((1 << MEMORY_BIT-1)-1))+(-1) * \
        (bool(value2 & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1)
    logger.info("value1:\t%d\t(%d)\t%s", value1, value1_sign, bin(value1))
    logger.info("value2:\t%d\t(%d)\t%s", value2, value2_sign, bin(value2))
    operator = operator % 8
>>>>>>> Stashed changes
    result = 0
    result_sign = 0
    if operator == 0:
        result = value1+1
        result_sign = value1_sign+1
    if operator == 1:
        result = value1+value2
        result_sign = value1_sign+value2_sign
    if operator == 2:
        result = value1-value2
        result_sign = value1_sign-value2_sign
    if operator == 3:
        result = value1-1
        result_sign = value1_sign-1
    if operator == 4:
        result = value1 | value2
        result_sign = value1 | value2
    if operator == 5:
        result = value1 ^ value2
        result_sign = value1 ^ value2
    if operator == 6:
        result = value1 & value2
        result_sign = value1 & value2
    if operator == 7:
        result = ~value1
<<<<<<< Updated upstream
    SIGN = result < 0
    ZERO = result == 0
    CARRY=not (0 <=result <(1<<MEMORY_BIT))
    OVERFLOW = not(-(1 << MEMORY_BIT) <= result <= ((1 << MEMORY_BIT)-1))
    result &= ((1 << MEMORY_BIT)-1)
    RESISTER['1'] = result
=======
        result_sign = ~value1

    logger.info('result:\t%d\t(%d)\t%s',
                result, result_sign, bin(result))
    result_fixed = result & ((1 << MEMORY_BIT)-1)
    result_sign_fixed = (result_fixed & ((1 << MEMORY_BIT-1)-1))+(-1) * \
        (bool(result_fixed & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1)
    logger.info('fixed:\t%d\t(%d)\t%s',
                result_fixed, result_sign_fixed, bin(result_fixed))
    CARRY = result != result_fixed
    OVERFLOW = result_sign != result_sign_fixed

    SIGN = result_sign_fixed < 0
    ZERO = result == 0
    resister['R1'] = result
    logger.info("sign : %d , zero : %d , carry : %d , overflow : %d",
                SIGN, ZERO, CARRY, OVERFLOW)


def p_mov(p):
    'cmd : MOV RESISTER RESISTER'
    global resister
    resister[p[2]] = resister[p[3]]


def p_func_r(p):
    'cmd : FUNC VALUE RESISTER'
    global resister
    logger.info('R1 :\t%d,\t%s :\t %d,\top :\t%d',
                resister['R1'], p[3], resister[p[3]], p[2])
    calc(resister['R1'], resister[p[3]], p[2])


def p_ldi(p):
    'cmd : LDI RESISTER VALUE'
    global resister
    resister[p[2]] = p[3]
    logger.info('%s :\t%d\t(%d)\t%s', p[2],
                (p[3] & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(p[3] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), p[3], bin(p[3]))


def p_fuci(p):
    'cmd : FUCI VALUE VALUE'
    global resister
    calc(resister['R1'], p[3], p[2])


def p_load(p):
    'cmd : LOAD RESISTER VALUE'
    global resister, memory
    resister[p[2]] = memory[p[3]]


def p_sta(p):
    'cmd : STA RESISTER VALUE'
    global resister, memory
    memory[p[3]] = resister[p[2]]


def p_func(p):
    'cmd : FUNC VALUE VALUE'
    global resister, memory
    calc(resister['R1'], memory[p[3]], p[2])


def p_halt(p):
    'cmd : HALT'
    sys.exit()


def p_out(p):
    'cmd : OUT RESISTER VALUE'
    global resister
    if p[3] == 0:
        print(resister[p[2]])
    else:
        raise NotImplementedError('device %s is not resistered!', p[2])


def p_error(p):
    print("Syntax error in input!")
>>>>>>> Stashed changes


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
