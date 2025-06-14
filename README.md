# Secure Python Script Execution API

## Quick Start

1. **Build the image:**
   ```bash
   docker build -t flask-nsjail-api .
   ```

2. **Run the container (local only):**
   ```bash
   sudo docker run --rm -p 8080:8080 --privileged flask-nsjail-api
   ```

3. **Test the API:**
   ```bash
   curl -X POST http://localhost:8080/execute \
     -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    print(\"Hello from Docker!\")\n    return {\"status\": \"docker success\"}"}'
   ```

**Note:** `--privileged` is required for nsjail. Not supported on Google Cloud Run.
