FROM python:3.10
RUN apt-get update
RUN apt-get install -y --no-install-recommends postgresql-client unzip vim
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./cards-server-app/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./cards-server .

RUN chmod +755 start.sh

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
