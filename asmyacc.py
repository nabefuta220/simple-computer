import ply.yacc as yacc
import sys





parser = yacc.yacc()
args= sys.argv

if len(args)==2:
    with open(args[1],"r",encoding='UTF-8') as f:
        while True:
            line=f.readline()
            if line:
                result = parser.parse(line)
            else:
                break
else:
    while True:
        try:
            s=input("SIMCOM> ")
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)