FROM python:3.11

# set work directory
WORKDIR /usr/app/api

# set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install -y wkhtmltopdf


# copy project
COPY . .

WORKDIR /usr/app

# creating a non-root user
RUN groupadd -r apiuser && useradd -r -g apiuser apiuser

RUN chown -R apiuser:apiuser /usr/app

# switch to non-root user
USER apiuser

EXPOSE 8000

CMD ["python", "-m", "api"]
