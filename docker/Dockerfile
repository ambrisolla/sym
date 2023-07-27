FROM alpine:latest

RUN apk add python3 bash py-pip 
RUN pip install mysql-connector-python oauth2client gspread
RUN mkdir /app

COPY ../main.py /app/main.py

CMD python3 /app/main.py
