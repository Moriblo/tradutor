from googletrans import Translator

from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect, request, Flask, jsonify, make_response

from schemas import *
from urllib.parse import unquote

import os, sys, json

from logger import setup_logger

# ==============================================================================
""" Inicializa service_name com o nome exclusivo do serviço para fins de geração
    de arquivo de log.
"""
# ==============================================================================
service_name = "tradutor"
logger = setup_logger(service_name)

# ==============================================================================
""" Informações de identificação, acesso e documentação do serviço
"""
# ==============================================================================
info = Info(title="Traduz Obra", version="1.0.0")
app = OpenAPI(__name__, info=info)

# ==============================================================================
""" Configurações de "Cross-Origin Resource Sharing"
"""
# ==============================================================================
# Foi colocado "supports_credentials=False" para evitar possíveis conflitos com
# algum tipo de configuração de browser. Mas não é a melhor recomendação por 
# segurança. Para melhorar a segurança desta API, o mais indicado segue nas 
# linhas abaixo comentadas.
CORS(app, supports_credentials=False)

# origins_permitidas = ["Obras de Arte"]
# Configurando o CORS com suporte a credenciais
# CORS(app, origins=origins_permitidas, supports_credentials=True)
# CORS(app, supports_credentials=True, expose_headers=["Authorization"])
# Adicionalmente utilizar da biblioteca PyJWT

# ==============================================================================
""" Rota /tradutor para tratar o fetch de `GET` do script.js.
"""
# ==============================================================================
@app.route('/tradutor', methods=['GET'])
def tradutor():
    # Lê identificação da origem da solicitação de uso desta API
    origin = request.headers.get('X-Origin')
    
    # Lê o valor do parâmetro de consulta 'entrada' da solicitação
    entrada = request.args.get('entrada')

    # Verifica se o parâmetro 'entrada' foi fornecido
    if not entrada:
        return 'Erro: nenhum texto fornecido para tradução'

    # Traduz o texto para o inglês
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(entrada, src='pt', dest='en')
    print(f"Em portugês: {entrada} em inglês: {translation.text}")
    print(f"Origin: {origin}")
    translation.json = json.dumps(translation.text)
    return translation.json

    pass

if __name__ == '__main__':
    app.run(port=5001, debug=True)