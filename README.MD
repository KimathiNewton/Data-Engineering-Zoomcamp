
docker run -t \
    -e POSTGRES_USER = "root" \
    -e POSTGRES_PASSWORD = "root" \
    -e POSTGRES_DB = "ny_taxi" \
    -v c:/Users/USER/Projects/Data_Engineering/ny_taxi_postgres_data:/var/lib/postgresql/data
    -p 5432:5432 \
    postgress:13


docker run -t \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data
    -p 5432:5432 \
    postgress:13  