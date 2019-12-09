from token import Token
import sys

class Lexico:
    def __init__(self):
        self.palavras_chaves = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not']
        self.delimitadores = ['.', ',', ';', ':', '(', ')']
        self.aditivos = ['+', '-']
        self.multiplicativos = ['*', '/']
        self.relacionais = ['=', '<', '>']
        
    def analizar(self, prog):
        token = ''
        cla = ''
        linha = 1
        table = []
        i = 0
        comentario = 0
        tamanho = len(prog)
        pulou_linha = False
        contp = 0
        contl = 0

        while i < tamanho:
            # QUEBRA DE LINHA
            if prog[i] == '\n':
                linha += 1
                i += 1

            # COMENTARIO
            elif prog[i] == '{':
                #comentario = True
                comentario += 1
                i+= 1
                while i < tamanho:
                    if prog[i] == '\n':                        
                        linha += 1
                        i += 1
                    # elif prog[i] == '{':
                    #     comentario += 1
                    #     i += 1
                    elif prog[i] == '}':
                        comentario -= 1
                        i+= 1
                        if(comentario == 0):
                            break
                    else:
                        i+= 1

                if comentario != 0:
                    sys.exit('EXCEPTION: Comentário não fechado!')
                    
            # IDENTIFICADOR #
            elif prog[i].isalpha(): # verifica letra
                token += prog[i]                
                i+= 1

                while i < tamanho:
                    if prog[i] == '_' or prog[i].isalpha() or prog[i].isdigit():
                        token += prog[i]
                        i+= 1

                    elif prog[i] == '\n':
                        #print ('incrementou', linha)
                        i += 1
                        pulou_linha = True
                        #linha += 1
                        break
                    
                    else:                        
                        break

                    # (MODIFICAÇÃO LÉXICA)
                    """ elif prog[i] == '.':                        
                        contp += 1
                        token += prog[i]
                        i+= 1
                        while i < tamanho:
                            if prog[i] == '_' or prog[i].isalpha() or prog[i].isdigit():                                
                                
                                token += prog[i]
                                i+= 1
                                
                            elif prog[i] == '\n':
                                #print ('incrementou', linha)
                                i += 1
                                pulou_linha = True
                                #linha += 1
                                break

                            else:
                                break
                        if pulou_linha:
                            linha += 1
                            pulou_linha = False """                    
                                            
                if token in self.palavras_chaves:
                    table.append(Token(token, 'Palavra-chave', linha))
                    token = ''

                elif token == 'and':
                    table.append(Token(token, 'Operador multiplicativo', linha))
                    token = ''

                elif token == 'or':
                    table.append(Token(token, 'Operador aditivo', linha))
                    token = ''

                elif contp == 2 and not token[-1] == '.':
                    table.append(Token(token, 'Id 3D', linha))
                    token = ''                
                
                else:
                    if contp > 0:
                        pass
                    else:
                        table.append(Token(token, 'Identificador', linha))
                        token = ''
                    
                if pulou_linha:
                    linha += 1
                    pulou_linha = False
            
            # NUMEROS INTEIROS E REAIS
            elif prog[i].isdigit():
                token += prog[i]
                cla = 'inteiro'
                i += 1
                while i < tamanho: 
                    if prog[i] == '\n': # se for new line sai pra concatenar na tabela como int                      
                        pulou_linha = True
                        i += 1
                        break

                    elif prog[i].isdigit(): # se há mais numeros compondo o inteiro
                        token += prog[i]
                        i += 1  
                    
                    elif prog[i] == '.': # se ocorrer '.' é NUMERO REAL
                        token += prog[i]
                        cla = 'real'
                        i += 1
                        while i < tamanho: #busca mais char depois do ponto
                            if prog[i] == '\n': # se for new line sai pra concatenar na tabela como int
                                pulou_linha = True
                                i += 1
                                break
                            
                            elif prog[i].isdigit(): # se há mais numero compondo o real após o ponto
                                token += prog[i]
                                i += 1

                            else: 
                                break
                            
                        if pulou_linha: # verifica e incrementa contador de linha
                            linha += 1
                            pulou_linha = False
                        
                    else:
                        if pulou_linha:  # verifica e incrementa contador de linha
                            linha += 1
                            pulou_linha = False
                        break

                table.append(Token(token, cla, linha)) #concatena tabela com tokens 
                token = ''
                cla = ''

            # DELIMITADORES ((( PRECISA VERIFICAR \n????)))
            elif prog[i] in self.delimitadores:
                if prog[i] == ':':
                    token += prog[i]
                    i += 1
                    # caso do : ou :=
                    if prog[i] == '=':
                        token += prog[i]
                        cla = 'Atribuição'
                        i+= 1
                        table.append(Token(token, cla, linha))
                        token = ''
                    else:
                        cla = 'Delimitador'
                        #i += 1
                        table.append(Token(token, cla, linha))
                        token = ''
                # caso dos outros delimitadores
                else:
                    token += prog[i]
                    cla = 'Delimitador'
                    i += 1
                    table.append(Token(token, cla, linha))
                    token = ''

            # OPERADORES ADITIVOS
            elif prog[i] in self.aditivos:
                token += prog[i]
                cla = 'Operador aditivo'
                i+= 1
                table.append(Token(token, cla, linha))
                token = ''

            # OPERADORES MULTIPLICATIVOS
            elif prog[i] in self.multiplicativos:
                token += prog[i]
                cla = 'Operador multiplicativos'
                i+= 1
                table.append(Token(token, cla, linha))
                token = ''

            # OPERADORES RELACIONAIS
            elif prog[i] in self.relacionais:
                cla = 'Operador relacional'
                # Caso <, <= ou <>
                if prog[i] == '<':
                    token += prog[i]
                    i+= 1
                    if prog[i] == '=':
                        token += prog[i]
                        i+= 1
                        table.append(Token(token, cla, linha))
                        token = ''
                    elif prog[i] == '>':
                        token += prog[i]
                        i+= 1
                        table.append(Token(token, cla, linha))
                        token = ''
                    else:
                        table.append(Token(token, cla, linha))
                        token = ''
                # Caso >, >=
                elif prog[i] == '>':
                    token += prog[i]
                    i+= 1
                    if prog[i] == '=':
                        token+= prog[i]
                        i+= 1
                        table.append(Token(token, cla, linha))
                        token = ''
                    else:
                        table.append(Token(token, cla, linha))
                        token = ''
                # Caso =
                else:
                    token += prog[i]
                    table.append(Token(token, cla, linha))
                    token = ''
                    i+= 1

            # ESPAÇO EM BRANCO    
            elif prog[i] == ' ' or prog[i] == '\t':
                i += 1
                continue
            else:
                sys.exit('EXCEPTION: Caractere inválido: ' + prog[i] + ' na linha: ' + str(linha))
                i+= 1    
        return table 
