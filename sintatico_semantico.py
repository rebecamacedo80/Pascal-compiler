from lexico import Lexico
from simbolo import Simbolo
import sys

class Sintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenAtual = ''
        self.tokenAntigo = ''
        self.tab_simbolos = []  # tabela de simbolos (SEMANTICO)
        self.pilha_tipos = [] # pilha de símbolos (SEMANTICO)

    def lerToken(self):

        if len(self.tokens) != 0:            
            self.tokenAntigo = self.tokenAtual
            self.tokenAtual = self.tokens.pop(0)
            return self.tokenAtual

        elif self.tokenAtual.token != '.':
            self.erroToken('.', self.tokenAtual.token, self.tokenAtual.linha)

    def pegaAntigo(self):

        if self.tokenAtual != '':
            self.tokens.insert(0, self.tokenAtual)
        
        self.tokenAtual = self.tokenAntigo
        self.tokenAntigo = ''
        return self.tokenAtual
            
    def erroToken(self, esperado, atual, linha):
        msgErro = '[ERRO SINTÁTICO] TOKEN ESPERADO: ' +  esperado + ' | TOKEN ATUAL: ' + atual + ' | LINHA: ' + str(linha)
        sys.exit(msgErro)     

    def erroTipo(self, esperado, atual, token, linha):
        msgErro = '[ERRO SINTÁTICO] TIPO ESPERADO: ' +  esperado + ' | TIPO ATUAL: ' + atual + ' | TOKEN: ' + token + ' | LINHA: ' + str(linha)
        sys.exit(msgErro)   

    def exibeLista(self):

        for i in reversed(self.tab_simbolos):
            print(i.ident, '\t', i.tipo)

        print('\n')

    def colocaTipo(self, tipo_listaVar): # (SEMANTICO) insere tipo em identificadores com tipo = '-'

        for symbol in self.tab_simbolos:
            
            if symbol.tipo == '-':

                if tipo_listaVar == 'integer':
                    symbol.tipo = 'inteiro'

                else:
                    symbol.tipo = tipo_listaVar

            else:
                continue

    def verificaIdLista(self, token_identif): # (SEMANTICO) verifica se já existe algum identificador igual na tabela

        for symbol in reversed(self.tab_simbolos):

            if symbol.ident != '$':

                if symbol.ident == token_identif.token:
                    sys.exit('Identificador repetido! Linha: ' + str(token_identif.linha))

            else:                              
                break
   
    def destroiEscopo(self): # (SEMANTICO) destroi escopo que já foi analisado

        for symbol in reversed(self.tab_simbolos):

            if symbol.ident != '$':
                self.tab_simbolos.pop() # remove os identificadores desse escopo

            else:                
                self.tab_simbolos.pop() # remove o 'mark' desse escopo
                break
    
    def verificaUsoLista(self, token_identif): # (SEMANTICO) verifica se o identificador pode ser utilizado
        flag = True # flag para dizer se o identificador foi declarado ou não

        for symbol in reversed(self.tab_simbolos):
            
            if symbol.ident != '$': # delimita procura apenas para um escopo (o atual)

                if symbol.ident == token_identif.token: # se encontrar identificador declarado na tabela
                    flag = True                    
                    break

                else:
                    flag = False
                    continue
                
            elif not flag:
                sys.exit('Variavel ' + token_identif.token + ' não foi declarada. Linha: ' + str(token_identif.linha))

                break
    
    #(MODIFICAÇÃO SEMÂNTICA) permite que um procedimento tenha mesmo nome de uma variável no msm escopo
    def verificaIDProcedure(self, token_identif):
        
        for symbol in reversed(self.tab_simbolos):
            
            if symbol.ident != '$':

                if symbol.tipo == 'procedimento':

                    if symbol.ident == token_identif.token:
                        sys.exit('Identificador de procedimento igual! Linha:' + str(token_identif.linha))

                    else:
                        pass
            else:
                break;        

    def compat_OpAtirmetrica(self): # (SEMANTICO) Verifica compatibilidade aritmétrica e atualiza pilha

        topo = self.pilha_tipos.pop()
        subtopo = self.pilha_tipos.pop()

        if  topo == 'inteiro' and subtopo == 'inteiro':
            self.pilha_tipos.append('inteiro')

        elif topo == 'real' and subtopo == 'real':
            self.pilha_tipos.append('real')
                
        elif topo == 'inteiro' and subtopo == 'real':
            self.pilha_tipos.append('real')

        elif topo == 'real' and subtopo == 'inteiro':
            self.pilha_tipos.append('real')
        
        else:
            sys.exit('ERRO: Incompatibilidade de tipos aritmétrica')
    
    def compat_OpLogica(self): # (SEMANTICO) Verifica compatibilidade lógica e atualiza pilha
        topo = self.pilha_tipos.pop()
        subtopo = self.pilha_tipos.pop()

        if  topo == 'boolean' and subtopo == 'boolean':
            self.pilha_tipos.append('boolean')
        
        else:
            sys.exit('ERRO: Incompatibilidade de tipos logica')

    def compat_OpRelacional(self): # (SEMANTICO) Verifica compatibilidade relacional e atualiza pilha
        topo = self.pilha_tipos.pop()
        subtopo = self.pilha_tipos.pop()

        if topo in ['inteiro', 'real'] and subtopo in ['inteiro', 'real']:
            self.pilha_tipos.append('boolean')
        
        else:
            sys.exit('ERRO: Incompatibilidade de tipos relacional')

    def pegaTipoLista(self, token_identif): # (SEMANTICO)

        for symbol in self.tab_simbolos:

            if symbol.ident == token_identif.token:
                return symbol.tipo 
    
    def compat_Atribuição(self): # (SEMANTICO) Verifica compatibilidade de atribuição e atualiza pilha
        topo = self.pilha_tipos.pop()
        subtopo = self.pilha_tipos.pop()

        if  subtopo == 'real' and topo in ['inteiro', 'real']:
            return True

        elif subtopo == 'inteiro' and topo == 'inteiro':
            return True

        elif subtopo == 'boolean' and topo == 'boolean':
            return True

        else:
            return False


    def programa(self):
        
        if self.lerToken().token == 'program':
            
            if self.lerToken().cla == 'Identificador':
                self.tab_simbolos.append(Simbolo('$')) # (SEMANTICO) adc primeiro 'mark' na tabela de simbolos (SEMANTICO)
                #self.tab_simbolos.append(Simbolo(self.tokenAtual.token, 'program'))

                if self.lerToken().token == ';':
                    self.declaracoesVariaveis()
                    self.declaracoesDeSubprogramas()                    
                    self.comandoComposto()
                    
                    if self.lerToken().token == '.':
                        print('Análise e sintaxe e semântica finalizada')
                    
                    else:
                        self.erroToken('.', self.tokenAtual.token, self.tokenAtual.linha)

                else:
                    self.erroToken(';', self.tokenAtual.token, self.tokenAtual.linha)
            
            else:
                self.erroTipo('Identificador', self.tokenAtual.cla, self.tokenAtual.token, self.tokenAtual.linha) 
        
        else:
            self.erroToken('program', self.tokenAtual.token, self.tokenAtual.linha)

    def declaracoesVariaveis(self):

        if self.lerToken().token == 'var':
            self.listaDeclaracoesVariaveis()

        else:
            self.pegaAntigo()

    def listaDeclaracoesVariaveis(self):

        if self.listaDeIdentificadores():

            if self.lerToken().token == ':':
                self.tipo()

                if self.lerToken().token == ';':
                    self.listaDeclaracoesVariaveis_()

                else: 
                    self.erroToken(';', self.tokenAtual.token, self.tokenAtual.linha)

            else:
                self.erroToken(':', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.erroTipo('Identificador', self.tokenAtual.cla, self.tokenAtual.token, self.tokenAtual.linha)

    def listaDeclaracoesVariaveis_(self):

        if self.listaDeIdentificadores():
            
            if self.lerToken().token == ':':
                self.tipo()
                                
                if self.lerToken().token == ';':
                    self.listaDeclaracoesVariaveis_()

                else: 
                    self.erroToken(';', self.tokenAtual.token, self.tokenAtual.linha)

            else:
                self.erroToken(':', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            pass

    def listaDeIdentificadores(self):

        if self.lerToken().cla == 'Identificador':
            self.verificaIdLista(self.tokenAtual) # (SEMANTICO) verifica se ja existe na lista           
            self.tab_simbolos.append(Simbolo(self.tokenAtual.token, '-', self.tokenAtual.linha)) # (SEMANTICO) adc na tabela de simbolos
            self.listaDeIdentificadores_()
            return True

        else:
            self.pegaAntigo()
            return False
            
    def listaDeIdentificadores_(self):

        if self.lerToken().token == ',':
            
            if self.lerToken().cla == 'Identificador':
                self.verificaIdLista(self.tokenAtual) # (SEMANTICO) verifica se ja existe na lista
                self.tab_simbolos.append(Simbolo(self.tokenAtual.token, '-', self.tokenAtual.linha)) # (SEMANTICO) adc identificador na tabela de simbolos
                self.listaDeIdentificadores_()

            else:
                self.erroTipo('Identificador', self.tokenAtual.cla, self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.pegaAntigo()

    def tipo(self):

        if self.lerToken().token in ['integer', 'real', 'boolean']:
                self.colocaTipo(self.tokenAtual.token)
                
        else:
            self.erroToken('integer/real/boolean', self.tokenAtual.token, self.tokenAtual.linha)

    def declaracoesDeSubprogramas(self):
        self.declaracoesDeSubprogramas_()

    def declaracoesDeSubprogramas_(self):

        if self.declaracaoDeSubprograma():

            if self.lerToken().token == ';':
                self.declaracoesDeSubprogramas_()

            else:
                self.erroToken(';', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            pass # vazio

    def declaracaoDeSubprograma(self):
        
        if self.lerToken().token == 'procedure':
                        
            if self.lerToken().cla == 'Identificador':
                self.verificaIDProcedure(self.tokenAtual) # verifica se já existe esse procedimento na lista
                self.tab_simbolos.append(Simbolo(self.tokenAtual.token, 'procedimento', self.tokenAtual.linha)) # (SEMANTICO) adc na tabela de simbolos 
                self.tab_simbolos.append(Simbolo('$')) # (SEMANTICO) adc um 'mark' pois aqui muda o escopo
                self.argumentos()
                
                if self.lerToken().token == ';':
                    self.declaracoesVariaveis()
                    self.declaracoesDeSubprogramas()
                    self.comandoComposto()
                    return True

                else:
                    self.erroToken(';', self.tokenAtual.token, self.tokenAtual.linha)

            else:
                self.erroTipo('Identificador', self.tokenAtual.cla, self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.pegaAntigo()
            return False 
                    
    def argumentos(self):

        if self.lerToken().token == '(':
            self.listaDeParametros()
            
            if self.lerToken().token == ')':
                pass

            else:
                self.erroToken(')', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.pegaAntigo()
        
    def listaDeParametros(self):        
        self.listaDeIdentificadores()

        if self.lerToken().token == ':':
            self.tipo()
            self.listaDeParametros_()

        else:
            self.erroToken(':', self.tokenAtual.token, self.tokenAtual.linha)

    def listaDeParametros_(self):
        
        if self.lerToken().token == ';':
            self.listaDeIdentificadores()

            if self.lerToken().token == ':':
                self.tipo()
                self.listaDeParametros_()

            else:
                self.erroToken(':', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.pegaAntigo()

    def comandoComposto(self):
        
        if self.lerToken().token == 'begin':
            self.comandosOpcionais()
            
            if self.lerToken().token == 'end':
                self.destroiEscopo() # (SEMANTICO) destrói escopo que acabou
                return True

            else:
                self.erroToken('end', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.pegaAntigo()
            return False

    def comandosOpcionais(self):        
        self.listaDeComandos()

    def listaDeComandos(self):        
        self.comando()
        self.listaDeComandos_()
                
    def listaDeComandos_(self):

        if self.lerToken().token == ';':
            self.comando()
            self.listaDeComandos_()

        else:
            self.pegaAntigo()

    def comando(self):
        
        if self.variavel():

            if self.lerToken().token == ':=':
                self.verificaUsoLista(self.tokenAntigo) # (SEMANTICO) verifica se esse identificador foi declarado
                self.pilha_tipos.append(self.pegaTipoLista(self.tokenAntigo)) # (SEMANTICO)
                self.expressao()

                if self.compat_Atribuição(): # (SEMANTICO)
                    pass

                else:
                    sys.exit('ERRO: Incompatibilidade de tipo')
                
            else:
                self.erroToken(':=', self.tokenAtual.token, self.tokenAtual.linha)

        elif self.ativacaoDeProcedimento():
            pass

        elif self.comandoComposto():
            pass

        elif self.lerToken().token == 'if':
            self.expressao()
                        
            if self.lerToken().token == 'then':
                self.comando()                
                self.parteElse()
                return

            else:
                self.erroToken('then', self.tokenAtual.token, self.tokenAtual.linha)
                
        else:
            self.pegaAntigo()
        
        if self.lerToken().token == 'while':
            self.expressao()
            
            if self.lerToken().token == 'do':
                self.comando()

            else:
                self.erroToken('do', self.tokenAtual.token, self.tokenAtual.linha)

        else:
            self.pegaAntigo()

    def parteElse(self):
        
        if self.lerToken().token == 'else':
            self.comando()    

        else:
            self.pegaAntigo()

    def variavel(self):    

        if self.lerToken().cla == 'Identificador':
            return True

        else:
            self.pegaAntigo()
            return False

    def ativacaoDeProcedimento(self):

        if self.lerToken().cla == 'Identificador':
            
            if self.lerToken().token == '(':
                self.listaDeExpressoes()

                if self.lerToken().token == ')':
                    return True

                else:
                    self.erroToken(')', self.tokenAtual.token, self.tokenAtual.linha)

            else:
                self.pegaAntigo()
                return True

        else:
            self.pegaAntigo()
            return False

    def listaDeExpressoes(self):        
        self.expressao()
        self.listaDeExpressoes_()

    def listaDeExpressoes_(self):
        
        if self.lerToken().token == ',':
            self.expressao()
            self.listaDeExpressoes_()

        else:
            self.pegaAntigo()

    def expressao(self):        
        self.expressaoSimples()

        if self.opRelacional():
            operador = self.tokenAtual.token
            self.expressaoSimples()
            self.compat_OpRelacional()

        else:
            pass

    def expressaoSimples(self):
        
        if self.termo():
            self.expressaoSimples_()

        elif self.sinal():

            if self.termo():
                self.expressaoSimples_()
        
        else:
            msg = 'ERRO: ERA ESPERADO UMA EXPRESSÃO! linha: ' + str(self.tokenAtual.linha)
            sys.exit(msg)
        
    def expressaoSimples_(self):
        
        if self.opAditivo():
            operador = self.tokenAtual.token
            self.termo()
            self.expressaoSimples_()

            if operador == 'or':
                self.compat_OpLogica() # (SEMANTICO)

            else:
                self.compat_OpAtirmetrica() # (SEMANTICO)

        else:
            pass
    
    def termo(self):
        
        if self.fator():
            self.termo_()
            return True

        else:
            return False
            
    def termo_(self):
        
        if self.opMultiplicativo():
            operador = self.tokenAtual.token
            self.fator()            
            self.termo_()

            if operador == 'and':
                self.compat_OpLogica() # (SEMANTICO)

            else:
                self.compat_OpAtirmetrica() # (SEMANTICO)

        
    def fator(self):
        x = self.lerToken()

        if x.token in ['true', 'false']:
                self.pilha_tipos.append('boolean') # (SEMANTICO)
                return True

        elif x.cla == 'Identificador':
                      
            self.verificaUsoLista(self.tokenAtual) # (SEMANTICO) verifica se identificador foi declarado            
            self.pilha_tipos.append(self.pegaTipoLista(self.tokenAtual)) # (SEMANTICO) empilha tipo do identificador
                        
            if self.lerToken().token == '(':
                self.listaDeExpressoes()

                if self.lerToken().token != ')':
                   self.erroToken(')', self.tokenAtual.token, self.tokenAtual.linha)

            else:
                self.pegaAntigo()              
                return True

        elif x.cla in ['inteiro', 'real']:
            
            if x.cla == 'inteiro': 
                self.pilha_tipos.append('inteiro') # (SEMANTICO)
            
            else:
                self.pilha_tipos.append('real') # (SEMANTICO)

            return True

        elif x.token == '(':
            self.expressao()

            if self.lerToken().token != ')':
                self.erroToken(')', self.tokenAtual.token, self.tokenAtual.linha)

            else:
                return True
            
        elif x.token == 'not':
            self.lerToken()
            self.fator()
        
        else:
            self.pegaAntigo()
            return False

    def sinal(self):
        
        if self.lerToken().token == '+' or self.tokenAtual.token == '-':
            return True

        else:
            self.pegaAntigo()
            return False
            
    def opRelacional(self):
        
        if self.lerToken().token in ["=","<",">","<=",">=","<>"]:
            return True

        else:
            self.pegaAntigo()
            return False

    def opAditivo(self):

        if self.lerToken().token in ["+","-","or"]:
            return True

        else:
            self.pegaAntigo()
            return False

    def opMultiplicativo(self):

        if self.lerToken().token in ["*","/","and"]:       
            return True

        else:            
            self.pegaAntigo()
            return False