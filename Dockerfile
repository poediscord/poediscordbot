FROM pypy:3.7-slim-buster

WORKDIR /app
ADD . /app
## Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD [ "pypy3", "main.py" ]
#CMD [ "python", "main.py" ]