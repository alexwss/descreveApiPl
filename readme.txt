******************************************************************************************************************
***********************************************Sample of use******************************************************
******Note:Out parameters mustn't have ":" ***********
***************Must open the CMD on folder of this project, calling with a test on sqlplus           *************
******************************************************************************************************************
------------------------------------------------------------------------------------------------------------------
cmd:> py app.py "sdbanco" "sdbanco" "dev" "sCvApiJpListarArquivos(0,'SAMPLE',poncodigoretorno, pocurdados)"
------------------------------------------------------------------------------------------------------------------





******************************************************************************************************************
***********************************************Installation*******************************************************
******************************************************************************************************************
To use this program 
Install these applications: 
    python3.x, 
    cx_oracle,
    instant client;

Python3
https://www.python.org/downloads/

Driver cx_oracle
run on CMD:> py pip install cx_Oracle
 
Instalar Oracle Instant Cliente(Deve-ser mesma arquitetura do Python ex:32x ou 64x)
http://www.oracle.com/technetwork/database/database-technologies/instant-client/overview/index.html

E inserir o caminho do instant client va variavel de sistema PATH,
de preferência no inicio das declarações ex: PATH>C:\oracle\instantclient_12_2;