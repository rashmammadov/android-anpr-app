FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    unzip \
    openjdk-8-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME correctly for the architecture
RUN if [ "$(uname -m)" = "aarch64" ]; then \
        export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64; \
    else \
        export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64; \
    fi && \
    echo "export JAVA_HOME=$JAVA_HOME" >> /etc/environment

# Install buildozer
RUN pip3 install buildozer cython

# Create app directory
WORKDIR /app

# Copy application files
COPY . .

# Set permissions
RUN chmod +x build.sh

# Create a non-root user for buildozer
RUN useradd -m -s /bin/bash buildozer
RUN chown -R buildozer:buildozer /app

# Switch to non-root user
USER buildozer

# Set JAVA_HOME for the user
RUN if [ "$(uname -m)" = "aarch64" ]; then \
        echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> ~/.bashrc; \
    else \
        echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc; \
    fi

# Expose port for potential debugging
EXPOSE 8080

# Default command
CMD ["./build.sh"]
