import ply.lex as lex


tokens = ('MOV',  # レジスタ間のデータ転送
          'FUNC',  # 演算
          'LDI',  # 即値からレジスタへのデータ転送
          'HALT',  # 停止
          'RESISTER',  # レジスタ
          'OPERATOR',  # 演算子の種類
          'VALUE',#値


          )


t_MOV = r'MOV'
t_FUNC = r'FUNC'
t_LDI=r'LDI'
t_HALT = r'HALT'
t_RESISTER = r'R[1-7]'


def t_OPERATOR(t):
    r'[0-7]'
    t.value = int(t.value)
    return t


def t_VALUE(t):
    r'=(0x|0b|)?\d+'
    t.value = int(t.value[1:],0)
    return t




def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
