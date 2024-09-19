FROM python:3.8-slim
WORKDIR /app
#Install dependencies

COPY . /app

RUN pip install --upgrade pip
#copy the entire project code
RUN pip install -r /app/requirements.txt



# Set PYTHONPATH to make sure all modules are available
# ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONPATH="/app:${PYTHONPATH}"