FROM python:3.9-slim
WORKDIR /data
COPY data .
WORKDIR /app
COPY infra/fixtures.json fixtures.json
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY backend/foodgram .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]
