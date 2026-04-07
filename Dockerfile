FROM python:3.11.9-slim-bullseye

WORKDIR /app

<<<<<<< HEAD
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
=======
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
>>>>>>> 785131a (DockerFile Fixed)

COPY . .

EXPOSE 7860

<<<<<<< HEAD
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
=======
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
>>>>>>> 785131a (DockerFile Fixed)
