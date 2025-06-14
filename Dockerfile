FROM python:3.11-slim

# Install nsjail dependencies
RUN apt-get update && \
    apt-get install -y git build-essential flex bison pkg-config libprotobuf-dev protobuf-compiler libnl-3-dev libnl-genl-3-dev libnl-route-3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir before building nsjail
WORKDIR /app

# Build nsjail from source
RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && \
    make && \
    cp nsjail /app/nsjail_bin && \
    cd .. && rm -rf nsjail

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py ./app.py

ENV FLASK_ENV=production
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
