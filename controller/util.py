from datetime import date
import cx_Oracle, sys, subprocess, re, models
from models import tipoDado as c

#globais#
gUser       = ''
gPass       = ''
gHost       = ''
gCursor     = ''
gObject     = ''
gCommand    = ''
gTemporario = ''

#constantes#
TIPOS_DADOS = []
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.FIXED_CHAR'>","VARCHAR2") )
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.STRING'>"    ,"VARCHAR2") )
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.NUMBER'>"    ,"NUMBER"))
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.DATETIME'>"  ,"DATE"))
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.TIMESTAMP'>" ,"TIMESTAMP"))
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.CLOB'>"      ,"CLOB"))
TIPOS_DADOS.append(c.TipoDado("<class 'cx_Oracle.BLOB'>"      ,"BLOB"))

#metodos#
#----------------------------------------------------#
def getParametrosEntrada():
    parametrosEntrada = []

    for v in sys.argv[1:]:
        parametrosEntrada.append(str(v))

    return parametrosEntrada

#----------------------------------------------------#
def definirDadosConexao(usuario, senha, host):
    global gUser, gPass, gHost
    gUser = usuario
    gPass = senha
    gHost = host    

#----------------------------------------------------#
def gerarArquivo(comandoSql):
    global gObject, gCommand

    indice = comandoSql.find("(")
    
    gObject = comandoSql[:indice]
    gCommand = comandoSql

    comandoCompleto = "connect " + gUser + "/" + gPass + "@" + gHost
    comandoCompleto += "\n desc " + gObject + ";\n exit;"    

    processo = subprocess.Popen(["sqlplus","/nolog"], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    (stdout, stderr) = processo.communicate(comandoCompleto.encode("utf-8"))
    stdoutLinhas = stdout.decode("utf-8").split("\n")
    salvarArquivo(stdoutLinhas, 0)

    if len(stderr) > 0:
        raise NotImplementedError("Erro", "Erro ao Executar sqlPlus")       
    else:
        descreverCursor()

#----------------------------------------------------#
def salvarArquivo(texto, tipo):
    global gObject

    tamanho = len(texto)
    arq = open("log_"+str(date.today())+"_"+gObject+".txt","a+")
    
    if tipo == 0:
        arq.write("\nApi: "+str(gObject)+"\n\r")
        for atual in texto:
            indice = texto.index(atual)
            if indice > 6 and indice < (tamanho - 3):
                arq.write(str(atual))
    else:
        arq.write(str(texto))
        arq.write("/*\n\tFinal do Processamento....\n\r*/")   

    arq.close()    

#----------------------------------------------------#
def descreverCursor():
    global gObject, gCommand, gUser, gPass, gHost, gTemporario

    conexao = cx_Oracle.connect(gUser,gPass, gHost)
    cursor = conexao.cursor()
    textoArquivo = None



    listaParametros = quebrarParametros(gCommand)
    listaVariaveis = []
    if len(listaParametros) > 0:
        for atual in listaParametros:
            variavel = definirVariavel(atual)
            if len(variavel) > 0:
                listaVariaveis.append(variavel)
                variacao = instanciarVariavel(variavel)
                if variacao != None:
                    exec(str(variacao))

    argumentos = retornarArgumentos(gCommand)
    exec("cursor.callproc(gObject.strip(),"+str(argumentos)+")")
    
    #cursor.callproc(gObject.strip(), (0,"CAIXA_REMESSA", poncodigoretorno, pocurdados))
    
    for item in listaVariaveis:

        variavel = item.lower()
        textoArquivo = ''

        if variavel[:5] == "pocur" or variavel[:6] == "piocur":
            textoArquivo += "\n\n Dados do Cursor "+str(variavel)+"\n\r\tNome\t\t\tTipo Dado\t\t\tTamanho\r"
            
            injection = ''+str(variavel).strip()+'.fetchall()\n'
            injection += 'tamanho = len('+str(variavel).strip()+'.description)\n'
            injection += 'contador = 0\n'
            injection += 'for row in '+str(variavel).strip()+'.description:\n'
            injection += '\tcontador += 1\n'
            injection += "\ttipoDeDado = localizarDatatype(str(row[1]))\n"
            injection += '\tatual = chr(9) + str(row[0]) + chr(9) + str(tipoDeDado) + chr(9) + str(row[2]) +chr(13)\n'
            injection += "\ttextoArquivo += atual\n"
            injection += "\tif contador == (tamanho - 1):\n"
            injection += "\t\tsalvarArquivo(textoArquivo,1)\n"
            exec(injection)
    
    cursor.close()
    conexao.close()

#----------------------------------------------------#
def definirVariavel(argumento):
    valorVariavel =  str(str(argumento).lower()).strip()

    if valorVariavel[:2] == 'pi' or valorVariavel[:2] == 'po':
        return valorVariavel

    return ''

#----------------------------------------------------#
def cursorTemporario(cursorAtual):
    global gCursor
    gCursor = cursorAtual

#----------------------------------------------------#
def quebrarParametros(instrucao):
    tamanho = len(instrucao) -1
    listaArgumentos = []
    
    if tamanho > -1:
        parametrosTemp                         = retornarArgumentos(instrucao)
        indexParenteseEsquerdo                 = parametrosTemp.find("(")
        indexParenteseDireito                  = parametrosTemp.rfind(")")
        parametrosTemp                         = list(parametrosTemp)
        parametrosTemp[indexParenteseEsquerdo] = ""
        parametrosTemp[indexParenteseDireito]  = ""
        parametrosTemp                         = "".join( str(x) for x in parametrosTemp)
        listaArgumentos                        = parametrosTemp.split(",")              

    return listaArgumentos

#----------------------------------------------------#
def retornarArgumentos(instrucao):
    indice = instrucao.find("(")
    return instrucao[indice:]

#----------------------------------------------------#
def localizarDatatype(datatype):

    for atual in TIPOS_DADOS:
        if atual.datatype == datatype:
            return atual.real

    return datatype

#----------------------------------------------------#
def instanciarVariavel(variavel):
    temp = str(variavel).lower()
    if temp[:3] == 'pon' or temp[:4] == 'pion':
        return variavel + " = 0".strip()
    elif temp[:3] == 'pos' or temp[:4] == 'pios':
        return variavel + " = '".strip()
    #elif temp[:4] == 'podt' or temp[:5] == 'piodt':
    #    return variavel + " = cx_Oracle.DATE".strip()
    elif temp[:5] == 'pocur' or temp[:6] == 'piocur':
        return variavel + " = conexao.cursor()".strip()
    else:
        return None
