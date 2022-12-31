FROM python:alpine
RUN apk add linux-headers gcc libc-dev libffi-dev zlib-dev libjpeg-turbo-dev cairo-dev cairo cairo-tools

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY --chown=appuser:appgroup . /home/appuser/app
WORKDIR /home/appuser/app

## Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip --trusted-host pypi.python.org -r requirements.txt
CMD [ "python", "main.py" ]