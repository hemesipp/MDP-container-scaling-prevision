FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install fastapi uvicorn kubernetes kafka-python

EXPOSE 80
CMD ["python", "/app/pacman.py"]
