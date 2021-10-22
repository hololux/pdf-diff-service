# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install poppler-utils version 0.74.0, because pdftohtml produces broken xml in version 0.71.0
# which is the highest version available in Debian 10 (the OS of the base image).
RUN apt-get update && apt-get install wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev -y
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz \
    && tar -xf poppler-data-0.4.9.tar.gz \
    && cd poppler-data-0.4.9 \
    && make install \
    && cd .. \
    && wget https://poppler.freedesktop.org/poppler-0.74.0.tar.xz \
    && tar -xf poppler-0.74.0.tar.xz \
    && cd poppler-0.74.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig

COPY . /home/site/wwwroot