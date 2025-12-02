FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app_gateway.py .

EXPOSE 80
CMD ["python", "app_gateway.py"]