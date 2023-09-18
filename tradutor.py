# =============================================================================
""" 1 - Carga Inicial.
"""
# =============================================================================
from googletrans import Translator

from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect, request, Flask, jsonify, make_response

from schemas import *
from urllib.parse import unquote

import os, sys, json

from logger import setup_logger

# ===============================================================================
""" 2 - Inicializa variáveis de Informações gerais de identificação do serviço.
"""
#  ==============================================================================
info = Info(title="API Tradutor", version="1.0.0")
app = OpenAPI(__name__, info=info)

home_tag = Tag(name="Documentação", description="Apresentação da documentação via Swagger.")
obra_tag = Tag(name="Rota em tradutor", description="Realiza tradução do português para o inglês")
doc_tag = Tag(name="Rota em tradutor", description="Documentação da API tradutor no github")

# ==============================================================================
""" 3 - Inicializa "service_name" para fins de geração de arquivo de log.
"""
# ==============================================================================
service_name = "tradutor"
logger = setup_logger(service_name)

# ==============================================================================
""" 4 - Configurações de "Cross-Origin Resource Sharing" (CORS).
# Foi colocado "supports_credentials=False" para evitar possíveis conflitos com
# algum tipo de configuração de browser. Mas não é a melhor recomendação por 
# segurança. Para melhorar a segurança desta API, o mais indicado segue nas 
# linhas abaixo comentadas.
#> origins_permitidas = ["Obras de Arte"]
#> Configurando o CORS com suporte a credenciais
#> CORS(app, origins=origins_permitidas, supports_credentials=True)
#> CORS(app, supports_credentials=True, expose_headers=["Authorization"])
#> Adicionalmente utilizar da biblioteca PyJWT
"""
# ==============================================================================
CORS(app, supports_credentials=False)

# ================================================================================
""" 5.1 - DOCUMENTAÇÂO: Rota "/" para geração da documentação via Swagger.
"""
# ================================================================================
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger.
    """
    return redirect('/openapi/swagger')

# ================================================================================
""" 5.2 - DOCUMENTAÇÂO: Rota "/doc" para documentação via github.
"""
# ================================================================================
@app.get('/doc', tags=[doc_tag])
def doc():
    """Redireciona para documentação no github.
    """
    return redirect('https://github.com/Moriblo/tradutor')

# ==============================================================================++
""" 6 - Rota "/tradutor" para tratar o fetch de `GET`.
"""
# ==============================================================================++
@app.get('/tradutor', methods=['GET'], tags=[obra_tag],
            responses={"200": TradutorSchema})

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

# ===============================================================================
""" 7 - Garante a disponibilidade da API em "suspenso".
"""
# ===============================================================================
if __name__ == '__main__':
    app.run(port=5001, debug=True)