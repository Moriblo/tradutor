FROM python:3.9
WORKDIR /tradutor
COPY requirements.txt .

RUN pip install --no--cache-dir -r requiremments.txt
COPY . .

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]
