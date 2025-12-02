FROM python:3.13

WORKDIR /app

COPY appA.py .
RUN pip install Flask

EXPOSE 8080

CMD ["python", "appA.py"]