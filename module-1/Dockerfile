FROM python:3.11.7

RUN apt-get install wget

RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app

# yellow taxi
COPY ingest_data.py  ingest_data.py 
# green taxi
COPY ingest_data_green.py  ingest_data_green.py 

# yellow taxi
# ENTRYPOINT [ "python", "ingest_data.py" ]
# green taxi
ENTRYPOINT [ "python", "ingest_data_green.py" ]