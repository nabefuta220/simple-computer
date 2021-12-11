import re

import ply.lex as lex

t_MOV = 'MOV'
t_FUNC = 'FUNC'
t_LDI = 'LDI'
t_FUCI = 'FUCI'
t_LOAD = 'LOAD'
t_STA = 'STA'
t_JMP = 'JMP'
t_HALT = 'HALT'
t_OUT = 'OUT'

t_RESISTER = r'R[0-7]'

reserved = {
    'MOV': t_MOV,  # レジスタ間のデータ転送
    'LDI': t_LDI,  # 即値からレジスタへのデータ転送
    'FUCI': t_FUCI,  # オペラントとレジスタとの演算
    'LOAD': t_LOAD,  # メモリからレジスタへのデータ転送
    'STA': t_STA,  # レジスタからメモリへのデータ転送
    'FUNC': t_FUNC,  # レジスタとメモリとの演算
    'JMP': t_JMP,  # 特定の番地に飛ばす
    'OUT': t_OUT,  # 出力
    'HALT': t_HALT,  # 停止
}
tokens = [
    'RESISTER',  # レジスタ
    'VALUE',  # 値
    'LABEL_IN',  # ラベル(生成)
    'LABEL_OUT',  # ラベル(遷移)

] + list(reserved.values())

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*$'

#ラベルへのジャンプ
def t_LABEL_OUT(t):
    r'[0-9A-Za-z]+$'
    t.type = reserved.get(t.value, 'LABEL_OUT')
    if re.fullmatch(r'R[0-7]', t.value):
        t.type = 'RESISTER'
    if re.fullmatch(r'([0-9A-Fa-f]+H)|\d+', t.value):
        t.type = 'VALUE'
        return t_VALUE(t)
    if t.type != 'LABEL_OUT' and False:
        print(f"at line {t.lexer.lineno} : '{t.value}' can't use as label")
        t.lexer.skip(1)
    return t

#数値
def t_VALUE(t):
    r'([0-9A-Fa-f]+H)|\d+'
    t.value = int(t.value[:-1], 16) if t.value[-1] == 'H' else int(t.value, 10)
    return t

#ラベルの定義
def t_LABEL_IN(t):
    r'[0-9A-Za-z]+:'
    t.value = t.value[:-1]
    t.type = reserved.get(t.value, 'LABEL_IN')

    if t.type != 'LABEL_IN':
        print(f"at line {t.lexer.lineno} : '{t.value}' can't use as label")
        t.lexer.skip(1)
    return t

#改行
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)





def t_error(t):
    print(f"at line {t.lexer.lineno}:Illegal character '{t.value}'")
    t.lexer.skip(1)


def build_lex():
    #構文解析をする
    return lex.lex()


def bebug(lexer, data):
    datas = data.split('\n')  # 改行ごとに区切る
    print(f"command : {datas}")
    for command in datas:
        if not command:  # 空文字列を飛ばす
            continue
        lexer.input(command)  # dataを読み込む
        while True:
            tok = lexer.token()  # トークンに分解する
            if not tok:
                break


if __name__ == '__main__':
    bebug(build_lex(), "casat1:OUT R3 0\nHALT")
