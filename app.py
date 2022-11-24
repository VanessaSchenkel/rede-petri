from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/engine/executar/tudo", methods=['POST'])
def executarEngine():
    try:
        return "<p>/engine/executar/tudo</p>"
    except:
        print("Erro ao executar engine")
        
@app.route("/engine/executar/tudo/sem-parar", methods=['POST'])
def executarEngineSemParar():
    try:
        return "<p>/engine/executar/tudo/sem-parar</p>"
    except:
        print("Erro ao executar engine sem parar")  
        
@app.route("/engine/executar/passo", methods=['GET'])
def executarEnginePassoAPasso():
    try:
        return "<p>/engine/executar/passo</p>"
    except:
        print("Erro ao executar engine sem parar")    
        
@app.route("/criar/rede", methods=['POST'])
def criaRedeDePetri():
    try:
        return "<p>/engine/executar/passo</p>"
    except:
        print("Erro ao executar engine sem parar")  

@app.route("/criar/conexao", methods=['POST'])
def criaConexao():
    try:
        return "<p>/engine/executar/passo</p>"
    except:
        print("Erro ao executar engine sem parar") 

@app.route("/criar/transicao", methods=['POST'])
def criaTransicao():
    try:
        return "<p>/engine/executar/passo</p>"
    except:
        print("Erro ao executar engine sem parar") 
        
@app.route("/criar/lugar", methods=['POST'])
def criaLugar():
    try:
        return "<p>/engine/executar/passo</p>"
    except:
        print("Erro ao executar engine sem parar")    
        
@app.route("/deletar/lugar/<nome_lugar>", methods=['DELETE'])
def deletarLugar(nome_lugar):
    try:
        return "<p>/engine/executar/passo</p>" + str(nome_lugar)
    except:
        print("Erro ao executar engine sem parar")
        
@app.route("/deletar/transicao/<nome_transicao>", methods=['DELETE'])
def deletarTransicao(nome_transicao):
    try:
        return "<p>/engine/executar/passo</p>" + str(nome_transicao)
    except:
        print("Erro ao executar engine sem parar")

@app.route("/deletar/conexao/<nome_conexao>", methods=['DELETE'])
def deletarConexao(nome_conexao):
    try:
        return "<p>/engine/executar/passo</p>" + str(nome_conexao)
    except:
        print("Erro ao executar engine sem parar")
        
@app.route("/consultar", methods=['GET'])
def getRedeDePetri():
    try:
        return "<p>/engine/executar/passo</p>" 
    except:
        print("Erro ao executar engine sem parar")  
        
@app.route("/adiciona/token/lugar/<nome_lugar>", methods=['PATCH'])
def adicionaToken(nome_lugar):
    try:
        return "<p>/engine/executar/passo</p>" 
    except:
        print("Erro ao executar engine sem parar")  
        
@app.route("/remove/token/lugar/<nome_lugar>", methods=['PATCH'])
def removeToken(nome_lugar):
    try:
        return "<p>/engine/executar/passo</p>" 
    except:
        print("Erro ao executar engine sem parar")
        
@app.route("/consultar/token/lugar/<nome_lugar>", methods=['GET'])
def getToken(nome_lugar):
    try:
        return "<p>/engine/executar/passo</p>" 
    except:
        print("Erro ao executar engine sem parar")                     