FROM python:3.11-slim

# Install all dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y curl && apt-get autoremove -y && apt-get clean

# Work directory
WORKDIR /app

# Cpy
COPY . . 

# Port to expose
EXPOSE 8000

# Launch API
CMD [ "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000" ]