FROM python:3.7

#RUN mkdir /app \
#&& pip install kafka-python
WORKDIR /app
ADD . /app/

#EXPOSE 9092
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","-u", "/app/producer.py"]

