FROM python:3.8-alpine
COPY . /app
WORKDIR /app
RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev
RUN pip --no-cache-dir install -r requirements.txt   
EXPOSE 5001
ENTRYPOINT  ["python3"]
CMD ["app.py"]