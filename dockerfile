# Use an official Python runtime as a parent image
FROM python:3.10.12-slim

# Set the working directory in the container to /app
WORKDIR /

# Add the current directory contents into the container at /app
ADD . /

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME streamlit_app

# Run streamlit when the container launches
CMD streamlit run application/src/home.py --server.port 8501 --server.address 0.0.0.0 --server.enableXsrfProtection=false --server.enableCORS=false

