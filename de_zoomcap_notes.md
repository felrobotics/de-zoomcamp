
# DE ZOOM CAMP NOTES
https://github.com/DataTalksClub/data-engineering-zoomcamp

## NY TAXI DATA | DATA 

download data 
https://github.com/DataTalksClub/nyc-tlc-data?tab=readme-ov-file


```bash
# POSTGRES COMMANDS 

\dt # 
```

```bash
# Postgres docker from console 
docker run -it \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=root \
-e POSTGRES_DB=ny_taxi \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \                                
-p 5432:5432 \
postgres:13

# above command not working because I am not user root, so I had to modify it
docker volume create pg_data

docker run -it --rm \
--name postgres \
--network pg-network \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=root \
-e POSTGRES_DB=ny_taxi \
-v pg_data:/var/lib/postgresql/data \
-p 5433:5432 \
postgres:13

# inspect pg 
docker inspect pg

# connect in other terminal with pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi

# run commands on postgres 
\dt 
SELECT 1

# install virtual env
pyenv virtualenv 3.11.7 de 
pyenv activate de 

#packages 
pip install pip --upgrade
pip install jupyter

# run jupyter
jupyter notebook

# download data 
https://github.com/DataTalksClub/nyc-tlc-data?tab=readme-ov-file
# using file : yellow_tripdata_2021-01.csv

# to work with only 100 rows 
head -n 100 yellow_tripdata_2021-01.csv > yellow_head.csv

# count the nr of lines 
wc -l yellow_tripdata_2021-01.csv 
## >> 1369766
wc -l yellow_head.csv

# with jupyter insert values to postgres

# check table with pgcli 
pgcli -h localhost -p 5433 -u root -d ny_taxi
DESCRIBE yellow_taxi_data 
# or with short command 
\d yellow_taxi_data 

# inject all data with jupyter  and count
SELECT count(1) FROM yellow_taxi_data;

#PGADMIN with docker
# to connect to pg we need a network

docker network create pg-network

docker run -it --rm \
--name pgadmin \
--network pg-network \
-e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
-e PGADMIN_DEFAULT_PASSWORD=root \
-p 8080:80 \
dpage/pgadmin4


## CONVERT JUPYTER TO SCRIPT
jupyter nbconvert --to=script upload-data.ipynb 

# arrange things, bring argparse and create ingest_data.py
CSV_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
--user=root \
--password=root \
--host=localhost \
--port=5433 \
--db_name=ny_taxi \
--table_name=yellow_taxi_data \
--csv_url=${CSV_URL}

## Create Dockerfile and build it 

docker build -t taxi_ingest:v001 .

# Let's run it (command very similar to the one above)
# but add the network and instead of localhost use the name of postgres container (pg)
# change now port to 5432

CSV_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it --rm --network=de_zoomcamp_default taxi_ingest:v001 \
--user=root \
--password=root \
--host=postgres \
--port=5432 \
--db_name=ny_taxi \
--table_name=yellow_taxi_data \
--csv_url=${CSV_URL}


# DOCKER COMPOSE 
# to run it detached 
docker compose up -d
```


## RUN SOME QUERIES 

```sql 
SELECT 
  *
FROM 
  yellow_taxi_data t,
  zones zpu,
  zones zdo
where
t."PULocationID" = zpu."LocationID" AND 
t."DOLocationID" = zdo."LocationID"
limit 100;

-- MAKE TABLE MORE CLEAR instead of * show only some fields
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime, 
  total_amount, 
  concat(zpu."Borough",' / ', zpu."Zone"),
  concat(zdo."Borough", ' / ' , zdo."Zone")
FROM 
  yellow_taxi_data t,
  zones zpu,
  zones zdo
where
t."PULocationID" = zpu."LocationID" AND 
t."DOLocationID" = zdo."LocationID"
limit 100;

--SAME AS ABOVE USING JOIN
SELECT    tpep_pickup_datetime,
          tpep_dropoff_datetime,
          total_amount,
          CONCAT(zpu."Borough", ' / ',zpu."Zone") as pickup_loc,
          CONCAT(zdo."Borough", ' / ',zdo."Zone") as drop_loc
FROM      yellow_taxi_data t
JOIN      zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN      zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT     100
;

-- COUNT AND GROUP BY
SELECT    CAST(tpep_dropoff_datetime AS DATE) AS "day",
          COUNT(1)
FROM      yellow_taxi_data t
GROUP BY  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY  "day"
;

-- ORDERED BY COUNT
SELECT    CAST(tpep_dropoff_datetime AS DATE) AS "day",
          COUNT(1)                            AS "count"
FROM      yellow_taxi_data t
GROUP BY  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY  "count" DESC
;   

-- EXTRACT SOME ANALYTICS AND GROUP BY WITH MORE VARIABLES
SELECT    CAST(tpep_dropoff_datetime AS DATE) AS "day",
          "DOLocationID",
          COUNT(1)                            AS "count",
          MAX(total_amount),
          MAX(passenger_count)
FROM      yellow_taxi_data t
GROUP BY  1,
          2
ORDER BY  "day" ASC,
          "DOLocationID" ASC
;

```


## CONNECT TO POSTGRES 

```bash 
# with pgcli
pgcli -u root -h localhost -p 5433 -d ny_taxi

# with psql
psql -U root -h localhost -p 5433 -d ny_taxi
```


## POSTGRES CLIENT 
pgcli

to install it : 

```bash 
# apt install
sudo apt install pgcli
# pip install
pip install pgcli
```

## TERRAFORM 

```bash 
export GOOGLE_CREDENTIALS="../gcp/key/<name>.json"
echo $GOOGLE_CREDENTIALS
```
