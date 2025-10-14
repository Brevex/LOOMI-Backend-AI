FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
COPY ./scripts /app/scripts
COPY Base_de_Dados_de_Tintas_Suvinil.csv /app/Base_de_Dados_de_Tintas_Suvinil.csv

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]