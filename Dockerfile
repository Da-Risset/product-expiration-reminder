FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /product_exp

# Install dependencies
COPY requirements.txt .env.example /product_exp/
RUN pip install -r requirements.txt

# Copy project
COPY . /product_exp/
