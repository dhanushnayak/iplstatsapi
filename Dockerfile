FROM ubuntu:latest
RUN apt update -y && apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3","app.py"]