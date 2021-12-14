import logging
import sys

import ply.yacc as yacc

import logger
from asmlex import build_lex, tokens
from build import MEMORY_BIT, WARD_BIT, build

logger = logging.getLogger(__name__)


logger.info("value max: %d", 1 << MEMORY_BIT)

resister = {'R0': None, 'R1': 0, 'R2': 0,
            'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0}  # レジスタの情報
labels = {}  # ラベルの情報
memory = [0 for _ in range(1 << WARD_BIT)]  # メモリの情報
counter = 0  # 次に読み込むアドレス
stack_point = 0  # スタックポインタ
OVERFLOW = False
CARRY = False
SIGN = False
ZERO = False
STATE_FLAG = 0  # 状態レジスタ

precedence = (  # 計算の優先順位を決める
    ('left', 'LABEL_IN'),

)


def generate_state_flag():
    """
    ステートフラグを生成する
    順番は 0b(CARRY)(SIGN)(ZERO)(OVERFLOW)の順
    """
    global CARRY, SIGN, ZERO, OVERFLOW
    global STATE_FLAG
    STATE_FLAG = CARRY << 1 | SIGN << 2 | ZERO << 1 | OVERFLOW << 0
    logger.info('state:\t%s', bin(STATE_FLAG))


def det_jmp(condition: int):
    """
    ジャンプするか決定する
    """
    global STATE_FLAG
    condition &= ((1 << 3)-1)
    if condition == 0:
        return True
    if condition == 1:
        return bool(STATE_FLAG & (1 << 0))
    if condition == 2:
        return bool(STATE_FLAG & (1 << 1))
    if condition == 3:
        return not bool(STATE_FLAG & (1 << 1))
    if condition == 4:
        return bool(STATE_FLAG & (1 << 2))
    if condition == 5:
        return not bool(STATE_FLAG & (1 << 2))
    if condition == 6:
        return bool(STATE_FLAG & (1 << 3))
    if condition == 7:
        return not bool(STATE_FLAG & (1 << 3))


def calc(value1: int, value2: int, operator: int):
    """
    演算をする
    """
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

    
    ZERO = result == 0
    resister['R1'] = result
    logger.info('result : singed: %d , unsined : %d bin:(%s)',
                (result & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(result & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), result, bin(result))
    SIGN = bool(result & 1<<MEMORY_BIT-1)
    CARRY = not (0 <= result <= (1 << MEMORY_BIT-1))
    OVERFLOW = not(0 <= result < (1 << MEMORY_BIT))

    result &= ((1 << MEMORY_BIT)-1)
    ZERO = result == 0
    resister['R1'] = result
    logger.info("sign : %d , zero : %d , carry : %d , overflow : %d",
                SIGN, ZERO, CARRY, OVERFLOW)
    generate_state_flag()


def p_mov(p):
    'cmd : MOV RESISTER RESISTER'
    global resister
    global ZERO, SIGN, OVERFLOW, CARRY
    global counter
    resister[p[2]] = resister[p[3]]
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()
    counter += 1


def p_func_r(p):
    'cmd : FUNC VALUE RESISTER'
    global resister
    global counter
    logger.info('R1 :\t%d,\t%s :\t %d,\top :\t%d',
                resister['R1'], p[3], resister[p[3]], p[2])
    calc(resister[p[3]], resister['R1'], p[2])
    counter += 1


def p_ldi(p):
    'cmd : LDI RESISTER VALUE'
    global resister
    global ZERO, SIGN, OVERFLOW, CARRY
    global counter
    resister[p[2]] = p[3]
    logger.info('%s :\t%d\t(%d)\t%s', p[2],
                (p[3] & ((1 << MEMORY_BIT-1)-1))+(-1) *
                (bool(p[3] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1),
                p[3],
                bin(p[3]))
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()
    counter += 1


def p_fuci(p):
    'cmd : FUCI VALUE VALUE'
    global resister
    global counter
    calc(p[3], resister['R1'],  p[2])
    counter += 1


def p_load(p):
    'cmd : LOAD RESISTER VALUE'
    global resister, memory
    global ZERO, SIGN, OVERFLOW, CARRY
    global counter
    resister[p[2]] = memory[p[3]]
    logger.info('%s :\t%d\t(%d)\t%s', p[2],
                (resister[p[2]] & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(resister[p[2]] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), resister[p[2]], bin(resister[p[2]]))
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()
    counter += 1


def p_sta(p):
    'cmd : STA RESISTER VALUE'
    global resister, memory
    global counter
    global ZERO, OVERFLOW, CARRY

    memory[p[3]] = resister[p[2]]
    logger.info('memory[%d] :\t%d\t(%d)\t%s', p[3],
                (resister[p[2]] & ((1 << MEMORY_BIT-1)-1))+(-1)*(bool(resister[p[2]] & (1 << MEMORY_BIT-1)) << MEMORY_BIT-1), resister[p[2]], bin(resister[p[2]]))
    ZERO = resister[p[2]] == 0
    SIGN = bool(resister[p[2]] & (1 << MEMORY_BIT-1))
    OVERFLOW = SIGN
    CARRY = False
    generate_state_flag()

    counter += 1


def p_func(p):
    'cmd : FUNC VALUE VALUE'

    global counter
    global resister, memory
    calc(memory[p[3]], resister['R1'],  p[2])
    counter += 1


def p_jmp(p):
    'cmd : JMP VALUE LABEL_OUT'
    global counter
    global labels
    if det_jmp(p[2]):
        counter = labels[p[3]]
    else:
        counter += 1


def p_cal(p):
    'cmd : CAL VALUE LABEL_OUT'
    # サブルーチンの呼び出し
    global counter
    global labels
    global stack_point
    if det_jmp(p[2]):
        # 復帰番地を追加
        memory[stack_point] = counter+1
        stack_point -= 1
        # ラベルへ飛ばす
        counter = labels[p[3]]

    else:
        counter += 1


def p_ret(p):
    'cmd : RET VALUE'
    # サブルーチンの終了
    global counter
    global labels
    global stack_point
    if det_jmp(p[2]):
        # 番地の復帰
        stack_point += 1
        counter = memory[stack_point]

    else:
        counter += 1


def p_set(p):
    'cmd : SET RESISTER'
    # スタックポインタの設定
    global stack_point
    global resister
    global counter
    stack_point = resister[p[2]]
    counter += 1


def p_halt(p):
    'cmd : HALT'
    sys.exit()


def p_out(p):
    'cmd : OUT RESISTER VALUE'
    global resister

    global counter

    if p[3] == 0:
        print(resister[p[2]])
    else:
        raise NotImplementedError('device %s is not resistered!', p[2])

    counter += 1


def p_label(p):
    'cmd : LABEL_IN cmd'
    pass


def p_error(p):
    print("Syntax error in input!")
    print(p)
    sys.exit()


def parse():
    return yacc.yacc()


def main(args):
    lex = build_lex()
    parser = parse()
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
            if not s:
                continue
            result = parser.parse(s)


def test(file: str):
    """
    実行する

    Parameters
    ----------
    file : str
        入力ファイル
    """
    global counter
    global labels
    labels = build(file)
    print("------")
    lex = build_lex()
    parser = parse()
    counter = 0
    with open(file, 'r') as f:
        lines = f.read().split('\n')
    while True:
        if not lines[counter]:
            counter += 1
        try:
            logger.debug("line %s : %s", counter, lines[counter])
            result = parser.parse(lines[counter])
        except IndexError:
            logger.error("exert did not finished!")
            sys.exit()


test(sys.argv[1])
