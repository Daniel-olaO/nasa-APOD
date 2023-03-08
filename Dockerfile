FROM python:3
ENV PYTHONBUFFERED 1
WORKDIR ./app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
