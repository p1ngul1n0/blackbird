FROM python:3
WORKDIR /home/
COPY . /home/
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python", "blackbird.py"]
