FROM python:3.13

WORKDIR /app

COPY app_order.py .
RUN pip install Flask

EXPOSE 8002

CMD ["python", "app_order.py"]