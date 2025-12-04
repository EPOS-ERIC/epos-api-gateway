FROM python:3.12-slim

ENV API_VERSION="1.0.0"
ENV API_TITLE="API Gateway"
ENV CONTACT_EMAIL="apis@lists.epos-ip.org"
ENV FLASK_DEBUG=0
ENV OTEL_SDK_DISABLED=true
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Create user first (before copying files)
RUN groupadd -g 1001 python \
 && useradd -r -u 1001 -m -s /sbin/nologin -g python python \
 && mkdir -p /usr/src/app/swagger_server/swagger_downloaded \
 && mkdir -p /usr/src/app/swagger_server/swagger_generated \
 && chown -R 1001:1001 /usr/src/app/

# Install dependencies first (better layer caching)
COPY --chown=1001:1001 requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && opentelemetry-bootstrap -a install \
 && rm -rf /root/.cache/pip

# Copy application code
COPY --chown=1001:1001 . .

EXPOSE 5000

USER 1001

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

ENTRYPOINT ["python3"]
CMD ["-m", "swagger_server"]