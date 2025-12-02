FROM python:3.13

WORKDIR /app

COPY app_user.py .
RUN pip install Flask

EXPOSE 8001

CMD ["python", "app_user.py"]