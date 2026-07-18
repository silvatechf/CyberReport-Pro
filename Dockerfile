# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# WeasyPrint needs Pango/Cairo for text shaping and rendering — this is
# the trade-off for its much better CSS support compared to xhtml2pdf.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf-2.0-0 \
        libffi-dev \
        shared-mime-info \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only dependency metadata first to maximize Docker layer caching —
# rebuilding the image after a source-only change won't reinstall deps.
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir .

# Sample data is included so the image is immediately runnable for a demo,
# without requiring the user to mount a volume first.
COPY data/ ./data/

# Reports are written here; mount a host directory over /app/output to
# persist them outside the container.
RUN mkdir -p /app/output
VOLUME ["/app/output"]

ENTRYPOINT ["cyberreport-pro"]
CMD ["--help"]
