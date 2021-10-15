FROM python:3.8-alpine

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /code/
COPY Pipfile /code/
COPY Pipfile.lock /code/

RUN pipenv install --system --deploy --dev
COPY . /code/

# CMD python app.py
