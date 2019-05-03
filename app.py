from controller import util as u

#
# Fonte destinado a geracao de documentacao de API's Pl/sql
# versao 1.0
#   

parametrosEntrada = u.getParametrosEntrada()

user      = parametrosEntrada[0]
pwrd      = parametrosEntrada[1]
server    = parametrosEntrada[2]
procedure = parametrosEntrada[3]

u.definirDadosConexao(user, pwrd, server)
u.gerarArquivo(procedure)
