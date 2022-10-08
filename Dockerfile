FROM python:alpine
RUN apk add linux-headers gcc libc-dev build-base cairo-dev cairo cairo-tools \
        jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY --chown=appuser:appgroup . /home/appuser/app
WORKDIR /home/appuser/app

## Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip --trusted-host pypi.python.org -r requirements.txt
CMD [ "python", "main.py" ]