FROM python:3.7

#RUN mkdir /app \
#&& pip install kafka-python
WORKDIR /app
ADD . /app/
RUN pip install requests

#EXPOSE 9092
CMD ["python","-u", "/app/job_consumer.py"]
