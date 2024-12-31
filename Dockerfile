FROM python

WORKDIR /app

COPY pipeline.py pipeline.py

CMD ["python", "pipeline.py"]


