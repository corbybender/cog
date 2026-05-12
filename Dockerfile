FROM python:3.12-slim

WORKDIR /workspace

COPY pyproject.toml .
COPY cog/ cog/

RUN pip install --no-cache-dir .

ENTRYPOINT ["cog"]
CMD ["--help"]
