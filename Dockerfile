FROM python:3.10-slim as builder

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Build the MkDocs site
RUN mkdocs build

# Use Nginx to serve the static site
FROM nginx:alpine

# Copy built site to Nginx serve directory
COPY --from=builder /app/site /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
