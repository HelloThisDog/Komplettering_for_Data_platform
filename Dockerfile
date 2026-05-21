FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install uv 
RUN uv sync

CMD ["uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]