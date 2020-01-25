FROM python:3.6
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY *.py ./
ENTRYPOINT ["python3", "api.py"]
