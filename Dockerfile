# get python image
FROM python:3.9-buster

# copy necessary files for the container
COPY requirements.txt .
COPY src/ .
COPY main.py .


# install dependencies
RUN pip install -r requirements.txt

# expose port
EXPOSE 8000

# finally run the application inside the container 
CMD exec uvicorn main:app --workers 1 --timeout-keep-alive 0 --port 8000 --host 0.0.0.0