import ply.lex as lex


tokens = ('MOV',  # レジスタ間のデータ転送
          'LDI',  # 即値からレジスタへのデータ転送
          'HALT',  # 停止
          'FUCI',  # オペラントとレジスタとの演算
          'LOAD',  # メモリからレジスタへのデータ転送
          'STA',  # レジスタからメモリへのデータ転送
          'FUNC',  # レジスタとメモリとの演算
          'OUT',  # 出力
          'RESISTER',  # レジスタ
          'VALUE',  # 値

          )


t_MOV = r'MOV'
t_FUNC = r'FUNC'
t_LDI = r'LDI'
t_FUCI = r'FUCI'
t_LOAD = r'LOAD'
t_STA = r'STA'
t_HALT = r'HALT'
t_OUT = r'OUT'
t_RESISTER = r'R[0-7]'


def t_VALUE(t):
    r'([0-9A-Fa-f]+H)|\d+'
    t.value = int(t.value[:-1], 16) if t.value[-1] == 'H' else int(t.value, 10)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'



def t_error(t):
    print(f"at line {t.lexer.lineno}:Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def main():
    lexer = lex.lex()


main()
