FROM pypy:3.7-slim-stretch
#FROM python:3.7.4-slim-stretch

WORKDIR /app
ADD . /app
## Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD [ "pypy3", "main.py" ]
#CMD [ "python", "main.py" ]