FROM python:3.10-slim
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install app
WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt

VOLUME /app/data

CMD ["python", "edit.py"]
