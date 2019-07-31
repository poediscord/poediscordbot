FROM pypy:3.6-slim-stretch

RUN mkdir app
COPY requirements.txt app
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r app/requirements.txt
COPY poediscordbot app