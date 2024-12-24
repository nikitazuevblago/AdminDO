FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env file
COPY .env .

# Copy the rest of the application
COPY . .

# Command to run the bot
CMD ["python", "bot.py"] 