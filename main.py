from lexico import Lexico
from sintatico_semantico import Sintatico

def main():
    arq = open('pascal_programs/program3.pas', 'r')
    prog = arq.read()
    arq.close()

    print('-- Análise Léxica --')
    lex = Lexico()
    lex.analizar(prog)
    listaTokens = lex.analizar(prog)

    print('Análise léxica finalizada \n')
    """ for i in listaTokens:
        print(i.token+"\t\t"+i.cla+"\t\t"+str(i.linha)) """

    print('-- Análise Sintática e Semântica --')
    sint = Sintatico(listaTokens)
    sint.programa()
    sint.exibeLista()
 
if __name__ == "__main__":
    main()