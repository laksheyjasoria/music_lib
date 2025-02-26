# Use an official Python image as base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r required.txt

# Expose the port Railway uses (default 8000, change if needed)
EXPOSE 8000

# Run the app
CMD ["python", "app.py", "--port=8000"]
