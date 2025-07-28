FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --timeout=120 --retries=10 --index-url https://pypi.org/simple
RUN pip install pipenv --timeout=120 --retries=10 --index-url https://pypi.org/simple

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]