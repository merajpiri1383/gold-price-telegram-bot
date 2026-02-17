FROM python:3.12-slim


# Set Environments 
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set Working Directory 
WORKDIR /app

# Copy The requirements.txt File
COPY requirements.txt /app

# Install Packages 
RUN pip install -r requirements.txt

# Copy All Files 
COPY . /app


CMD ["python","main.py"]
