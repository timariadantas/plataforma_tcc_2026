FROM python:3.11

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["python", "app/main.py"]