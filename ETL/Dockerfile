# Python 3.10.2. This ensures a consistent Python runtime environment for the application.

FROM python:3.10.2 
# specifies the working directory inside the container.

WORKDIR /app
# copies the requirements.txt file containing the list of Python dependencies into the container
COPY requirements.txt /app/
# installs the dependencies listed in requirements.txt without caching, reducing the container size.

RUN pip install --no-cache-dir -r requirements.txt
# specifies the working directory inside the container.
        
COPY . /app/

# defines the command to execute the main script. Here, it runs the app module using Python.

CMD ["python","-m","main"]

