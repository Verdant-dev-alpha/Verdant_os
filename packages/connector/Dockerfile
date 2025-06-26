FROM debian:bullseye-slim

# Install curl and CA certificates
RUN apt-get update && \
    apt-get install -y curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /cloud-sql-proxy

# Download the proxy binary
RUN curl -L -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.11.0/cloud-sql-proxy.linux.amd64 && \
    chmod +x cloud-sql-proxy

# Copy your credentials into the container
# Replace this with Docker volume if mounting from outside
COPY ./creds.json /cloud-sql-proxy/creds.json

# Expose default port
EXPOSE 5432

# Entry point
ENTRYPOINT ["./cloud-sql-proxy"]

# Default command (replace with your instance string)
CMD ["--credentials-file=creds.json", "your-project:region:instance"]
