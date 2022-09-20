# FROM python:3-slim
FROM --platform=linux/amd64 python:3-slim
COPY . /app
WORKDIR /app
RUN pip3 --no-cache-dir install -r requirements.txt   
# EXPOSE 5001
ENTRYPOINT  ["python3"]
CMD ["app.py"]
# COPY wait.sh /wait.sh
# RUN chmod +x /wait.sh