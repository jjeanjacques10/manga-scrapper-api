FROM python:3

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

# Create a workdir for our app
WORKDIR /usr/src/app
COPY . /usr/src/app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
RUN pip install --ignore-installed six watson-developer-cloud

# Expose port 3000
EXPOSE 3000

# Run the app
CMD [ "python", "./app.py" ]