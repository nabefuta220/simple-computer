import logging
import sys


import ply.yacc as yacc

import logger
from asmlex import tokens, build_lex
logger = logging.getLogger(__name__)

WARD_BIT = 8  # 1ワードのビット長
MEMORY_BIT = 8  # アドレスのビット長

labels: dict = {}  # ラベルの情報
used_labels: set = set()  # 使用しているラベルの情報
counter = 0  # 行数
precedence = (  # 計算の優先順位を決める
    ('left', 'LABEL_IN'),

)


def p_mov(p):
    'cmd : MOV RESISTER RESISTER'


def p_func_r(p):
    'cmd : FUNC VALUE RESISTER'


def p_ldi(p):
    'cmd : LDI RESISTER VALUE'


def p_fuci(p):
    'cmd : FUCI VALUE VALUE'


def p_load(p):
    'cmd : LOAD RESISTER VALUE'


def p_sta(p):
    'cmd : STA RESISTER VALUE'


def p_func(p):
    'cmd : FUNC VALUE VALUE'


def p_label_out(p):
    'cmd : JMP VALUE LABEL_OUT'
    global used_labels
    used_labels.add(p[3])


def p_label_in(p):
    'cmd : LABEL_IN cmd'
    global labels
    global counter
    if p[1] in labels:
        logger.error("labal : %s has alrealy used!", p[1])
        exit(1)
    else:
        labels[p[1]] = counter


def p_halt(p):
    'cmd : HALT'


def p_out(p):
    'cmd : OUT RESISTER VALUE'


def p_error(p):
    print("Syntax error in input!")
    print(p)
    sys.exit()


def parse():
    return yacc.yacc()


def cheak_label(labels: set, used_labels: set):
    """
    定義したが、使われていないラベルがあるか、

    もしくは使われているが、定義されていないラベルがあるかチェックする

    Parameters
    ---------
    labels : set of str
        定義されたラベルの集合
    used_labels : set of str
        使用されているラベルの集合 
    """
    unused_label = labels - used_labels
    undefined_lavel = used_labels - labels

    for unused in unused_label:
        logger.warning("label %s is defained, but never used", unused)
    for undefined in undefined_lavel:
        logger.error("label %s is not defained", undefined)
        sys.exit(1)


def build(file: str):
    """
    ファイルを静的解析する
    """
    global counter
    global labels, used_labels
    build_lex()
    parser = parse()
    try:
        # 改行ごとにファイルを区切る
        with open(file, 'r') as f:
            lines = f.read().split('\n')
    except FileNotFoundError:
        logger.error("file : %s not found", file)
        sys.exit(1)
    # 行数分繰り返す
    for command in lines:
        if not command:
            continue
        logger.debug("line %4d : %s", counter, command)
        result = parser.parse(command)
        counter += 1

    cheak_label(used_labels=used_labels, labels=set(labels))

    return labels


print(build(sys.argv[1]))
