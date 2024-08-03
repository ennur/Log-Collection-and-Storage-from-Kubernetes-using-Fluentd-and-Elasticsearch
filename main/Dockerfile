FROM python:3.8.10-alpine

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install --upgrade pip
EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]