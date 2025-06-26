FROM python:3.12-slim

# Prevent .pyc files & enable live logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (will be run again safely in entrypoint too)
RUN python manage.py collectstatic --noinput

# Copy entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose Daphne's port
EXPOSE 8000

# Start the app via the entrypoint script
CMD ["/app/entrypoint.sh"]
