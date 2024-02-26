# app/Dockerfile
FROM python:3.9-slim
#FROM aminehy/docker-streamlit-app

# Use the official Streamlit image as base

# create folder and move into folder
WORKDIR /code

# copy files
COPY . /code/


# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Command to run the Streamlit app
#CMD ["streamlit", "run", "amain.py"]
CMD ["python", "-m", "streamlit", "run", "app/main.py"]