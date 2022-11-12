FROM docker.io/python:3.10

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD scripts/restapi/*.py .

CMD ["python", "scrape_continous.py"]
