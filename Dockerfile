FROM python:alpine
## Install any needed packages specified in requirements.txt
RUN apk add linux-headers gcc libc-dev

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /home/appuser/app
ADD --chown=appuser:appgroup . /home/appuser/app

RUN pip install --upgrade pip --trusted-host pypi.python.org -r requirements.txt
CMD [ "python", "main.py" ]