FROM python:3.8-bullseye
USER root

RUN apt update
RUN apt install -y \
    vim \
    htop \
    jq \
    curl

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir \
    autopep8 \
    flake8

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

RUN useradd -m user
USER user

EXPOSE 5000 5000

CMD ["bash"]
