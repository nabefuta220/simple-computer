"""
字句解析を行う
"""
import re
import ply.lex as lex

# パターンの設定
t_MOV = 'MOV'
t_FUNC = 'FUNC'
t_LDI = 'LDI'
t_FUCI = 'FUCI'
t_LOAD = 'LOAD'
t_STA = 'STA'
t_JMP = 'JMP'
t_HALT = 'HALT'
t_IN = 'IN'
t_OUT = 'OUT'
t_RET = 'RET'
t_SET = 'SET'
t_CAL = 'CAL'
t_RESISTER = r'R[0-7]'

# 予約後の設定
reserved = {
    'MOV': t_MOV,  # レジスタ間のデータ転送
    'LDI': t_LDI,  # 即値からレジスタへのデータ転送
    'FUCI': t_FUCI,  # オペラントとレジスタとの演算
    'LOAD': t_LOAD,  # メモリからレジスタへのデータ転送
    'STA': t_STA,  # レジスタからメモリへのデータ転送
    'FUNC': t_FUNC,  # レジスタとメモリとの演算
    'JMP': t_JMP,  # 特定の番地に飛ばす
    'CAL': t_CAL,  # サブルーチン呼び出し
    'RET': t_RET,  # サブルーチン復帰
    'SET': t_SET,  # スタックポインタ変更
    'IN': t_IN,  # 入力
    'OUT': t_OUT,  # 出力
    'HALT': t_HALT,  # 停止
}
# トークンの設定
tokens = [
    'RESISTER',  # レジスタ
    'VALUE',  # 値
    'LABEL_IN',  # ラベル(生成)
    'LABEL_OUT',  # ラベル(遷移)

] + list(reserved.values())

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*$'

# ラベルへのジャンプ


def t_LABEL_OUT(t):
    r'[0-9A-Za-z]+$'
    t.type = reserved.get(t.value, 'LABEL_OUT')
    if re.fullmatch(r'R[0-7]', t.value):
        t.type = 'RESISTER'
    if re.fullmatch(r'([0-9A-Fa-f]+H)|\d+', t.value):
        t.type = 'VALUE'
        return t_VALUE(t)
    return t

# 数値


def t_VALUE(t):
    r'([0-9A-Fa-f]+H)|\d+'
    t.value = int(t.value[:-1], 16) if t.value[-1] == 'H' else int(t.value, 10)
    return t

# ラベルの定義


def t_LABEL_IN(t):
    r'[0-9A-Za-z]+:'
    t.value = t.value[:-1]
    t.type = reserved.get(t.value, 'LABEL_IN')

    if t.type != 'LABEL_IN':
        print(f"at line {t.lexer.lineno} : '{t.value}' can't use as label")
        t.lexer.skip(1)
    return t

# 改行


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"at line {t.lexer.lineno}:Illegal character '{t.value}'")
    t.lexer.skip(1)


def build_lex():
    """
    字句解析をする
    """

    return lex.lex()
