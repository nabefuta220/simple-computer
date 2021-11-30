import ply.lex as lex


tokens = ('MOV',#レジスタ間のデータ転送
        'FUNC', # 演算
          'HALT',#停止
          'RESISTER',#レジスタ
          'OPERATOR',#演算子の種類
          )


t_MOV = r'MOV'
t_FUNC = r'FUNC'
t_RESISTER = r'R[1-7]'
t_HALT = r'HALT'

def t_OPERATOR(t):
    r'[0-7]'
    t.value=int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
