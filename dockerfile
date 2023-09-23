FROM python:3.11.3

# Defina a variável de ambiente para o pip
ENV PIP_DEFAULT_TIMEOUT=1000

WORKDIR /tradutor
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]