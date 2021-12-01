import logging
import sys

import ply.yacc as yacc

import logger
from asmlex import tokens

logger = logging.getLogger(__name__)

WARD_BIT = 8
MEMORY_BIT = 8

resister = {'R0':None,'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0}

memory = [0 for _ in range(1 << WARD_BIT)]

OVERFLOW = 0
CARRY = 0
SIGN = 0
ZERO = 0


def calc(value1: int, value2: int, operator: int):
    global resister
    global OVERFLOW, CARRY, SIGN, ZERO
    operator = operator % 8
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
    logger.info('singed: %d , unsined : %d bin:(%s)',
                result, result, bin(result))
    SIGN = result < 0
    ZERO = result == 0
    CARRY = not (0 <= result < (1 << MEMORY_BIT))
    OVERFLOW = not(-(1 << MEMORY_BIT) <= result <= ((1 << MEMORY_BIT)-1))

    result &= ((1 << MEMORY_BIT)-1)
    resister['R1'] = result
    logger.info("sign : %d , zero : %d , carry : %d , overflow : %d",
                SIGN, ZERO, CARRY, OVERFLOW)


def p_mov(p):
    'cmd : MOV RESISTER RESISTER'
    global resister
    resister[p[2]] = resister[p[3]]


def p_func(p):
    'cmd : FUNC VALUE RESISTER'
    global resister
    logger.info('R1 : %d , %s : %d , op : %d',
                resister['R1'], p[3], resister[p[3]], p[2])
    calc(resister['R1'], resister[p[3]], p[2])


def p_ldi(p):
    'cmd : LDI RESISTER VALUE'
    global resister
    resister[p[2]] = p[3]
    logger.info('%s: %d', p[2], resister[p[2]],)



def p_halt(p):
    'cmd : HALT'
    sys.exit()


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()

while True:
    try:
        s = input("SIMCOM> ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
