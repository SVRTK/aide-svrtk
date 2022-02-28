FROM python:3.9.5

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py
COPY application.py application.py
COPY manifest.json manifest.json

CMD ["python", "main.py"]