# Builder stage
FROM python:3.11-slim as builder

# Set build-time environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install build dependencies and clean up in the same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
    jupyter \
    notebook \
    jupyterlab \
    ipykernel

# Create Jupyter kernel in builder stage
RUN python -m ipykernel install --user --name python311 --display-name "Python 3.11"

# Final stage
FROM python:3.11-slim

# Install AWS CLI dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    groff \
    less \
    && rm -rf /var/lib/apt/lists/*

# Copy AWS CLI from builder
COPY --from=builder /usr/local/aws-cli /usr/local/aws-cli
RUN ln -s /usr/local/aws-cli/v2/current/bin/aws /usr/local/bin/aws

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
# Copy Jupyter kernel files
COPY --from=builder /root/.local/share/jupyter /root/.local/share/jupyter

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

# Expose port
EXPOSE 8000

# Keep container running
CMD ["tail", "-f", "/dev/null"]
