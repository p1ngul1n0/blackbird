FROM python:3.9.2-alpine3.13
WORKDIR /home/
COPY . /home/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "blackbird.py"]