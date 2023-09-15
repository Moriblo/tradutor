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

# ======================================================================================
""" Informações de identificação, acesso e documentação do serviço
"""
#  =====================================================================================
info = Info(title="API Tradutor", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Apresentação da documentação via Swagger.")
obra_tag = Tag(name="Rotas em tradutor", description="Realiza tradução do português para o inglês")

# ========================================================================================
""" Rota /openapi para geração da documentação via Swagger
"""
# ========================================================================================
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger.
    """
    return redirect('/openapi/swagger')

# ==============================================================================
""" Rota /tradutor para tratar o fetch de `GET` do script.js.
"""
# ==============================================================================
#> @app.route('/tradutor', methods=['GET'])
@app.get('/tradutor', methods=['GET'], tags=[obra_tag],
            responses={"200": TradutorSchema})

#> def tradutor():
def get_tradutor(query: ObraBuscaSchema):
    """Traduz do português para o inglês.
    """

    # Lê identificação da origem da solicitação de uso desta API
    origin = request.headers.get('X-Origin')
    
    # Lê o valor do parâmetro de consulta 'entrada' da solicitação
    entrada = request.args.get('entrada')

    # Verifica se o parâmetro 'entrada' foi fornecido
    if not entrada:
        mesage = "Erro: nenhum texto fornecido para tradução"
        return mesage
    else:
        # Traduz o texto para o inglês
        translator = Translator(service_urls=['translate.google.com'])
        translation = translator.translate(entrada, src='pt', dest='en')
        print(f"Em portugês: {entrada} em inglês: {translation.text}")
        print(f"Origin: {origin}")
        translation.json = json.dumps(translation.text)
        
        # Retorna o conteúdo traduzido e mensagem de confirmação
        logger.debug(f"Tradução realizada de {entrada} para {translation.json}")
        mesage ="Tradução realizada"
        translation.json = translation.json.replace('"', '')
        return jsonify(entrada, mesage, translation.json)

        pass

if __name__ == '__main__':
    app.run(port=5001, debug=True)