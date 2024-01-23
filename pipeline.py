services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    restart: always




mintty docker run -t \
    -e POSTGRES_USER = "root" \
    -e POSTGRES_PASSWORD = "root" \
    -e POSTGRES_DB = "ny_taxi" \
    -v c:/Users/USER/Projects/Data_Engineering/ny_taxi_postgres_data:/var/lib/postgresql/data
    -p 5432:5432 \
    postgress:13
 
