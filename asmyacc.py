import logging
import sys
from types import SimpleNamespace

import ply.yacc as yacc

import logger
from asmlex import tokens

logger = logging.getLogger(__name__)

WARD_BIT = 8
MEMORY_BIT = 8
logger.info("value max: %d", 1 << MEMORY_BIT)

resister = {'R0': None, 'R1': 0, 'R2': 0,
            'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0}

memory = [0 for _ in range(1 << WARD_BIT)]

OVERFLOW = False
CARRY = False
SIGN = False
ZERO = False
STATE_FLAG = 0


def generate_state_flag():
    """
    ステートフラグを生成する
    順番は　0b(CARRY)(SIGN)(ZERO)(OVERFLOW)の順
    """
    global CARRY, SIGN, ZERO, OVERFLOW
    global STATE_FLAG
    STATE_FLAG = CARRY << 1 | SIGN << 2 | ZERO << 1 | OVERFLOW << 0
    logger.info('state:\t%s', bin(STATE_FLAG))


def calc(value1: int, value2: int, operator: int):
    global resister
    global OVERFLOW, CARRY, SIGN, ZERO
    value1_sign = (value1 & ((1 << MEMORY_BIT-1)-1)) + (-1) * \
        (bool(value1 & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1)
    value2_sign = (value2 & ((1 << MEMORY_BIT-1)-1))+(-1) * \
        (bool(value2 & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1)
    logger.info("value1:\t%d\t(%d)\t%s", value1, value1_sign, bin(value1))
    logger.info("value2:\t%d\t(%d)\t%s", value2, value2_sign, bin(value2))
    operator = operator % 8
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
    logger.info('result : singed: %d , unsined : %d bin:(%s)',
                (result & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(result & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), result, bin(result))

    CARRY = not (0 <= result <= (1 << MEMORY_BIT-1))
    OVERFLOW = not(0 <= result < (1 << MEMORY_BIT))

    result &= ((1 << MEMORY_BIT)-1)
    SIGN = result < 0
    ZERO = result == 0
    resister['R1'] = result
    logger.info("sign : %d , zero : %d , carry : %d , overflow : %d",
                SIGN, ZERO, CARRY, OVERFLOW)
    generate_state_flag()


def p_mov(p):
    'cmd : MOV RESISTER RESISTER'
    global resister
    global ZERO, SIGN, OVERFLOW, CARRY
    resister[p[2]] = resister[p[3]]
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()


def p_func_r(p):
    'cmd : FUNC VALUE RESISTER'
    global resister
    logger.info('R1 :\t%d,\t%s :\t %d,\top :\t%d',
                resister['R1'], p[3], resister[p[3]], p[2])
    calc(resister['R1'], resister[p[3]], p[2])


def p_ldi(p):
    'cmd : LDI RESISTER VALUE'
    global resister
    global ZERO, SIGN, OVERFLOW, CARRY
    resister[p[2]] = p[3]
    logger.info('%s :\t%d\t(%d)\t%s', p[2],
                (p[3] & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(p[3] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), p[3], bin(p[3]))
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()


def p_fuci(p):
    'cmd : FUCI VALUE VALUE'
    global resister
    calc(resister['R1'], p[3], p[2])


def p_load(p):
    'cmd : LOAD RESISTER VALUE'
    global resister, memory
    global ZERO,SIGN,OVERFLOW,CARRY
    resister[p[2]] = memory[p[3]]
    logger.info('%s :\t%d\t(%d)\t%s', p[2],
                (resister[p[2]] & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(resister[p[2]] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), resister[p[2]], bin(resister[p[2]]))
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()


def p_sta(p):
    'cmd : STA RESISTER VALUE'
    global resister, memory
    memory[p[3]] = resister[p[2]]
    logger.info('memory[%d] :\t%d\t(%d)\t%s', p[3],
                (resister[p[2]] & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(resister[p[2]] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), resister[p[2]], bin(resister[p[2]]))
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()




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


parser = yacc.yacc()

args = sys.argv
if len(args) == 2:
    f = open(args[1], "r")
    while True:
        line = f.readline()
        if line:
            result = parser.parse(line)
        else:
            raise Exception("exert not finished!")
else:
    while True:
        try:
            s = input('SIMCOM > ')
        except EOFError:
            raise Exception("exert not finished!")
            break
        if not s:
            continue
        result = parser.parse(s)
