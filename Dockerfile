FROM python:3

COPY . /api

WORKDIR /api

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["run.py"]