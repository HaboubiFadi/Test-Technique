# Python 3.10.2. This ensures a consistent Python runtime environment for the application.
FROM python:3.10.2 

# specifies the working directory inside the container.
WORKDIR /app

# copies the requirements.txt file containing the list of Python dependencies into the container
COPY requirements.txt /app/
# installs the dependencies listed in requirements.txt without caching, reducing the container size.
RUN pip install --no-cache-dir -r requirements.txt
#  copies the entire application source code from the build context into the /app directory inside the container.
        
COPY . /app/
#  indicates that the application will run on port 8080, making it accessible for networking within the containerized environment.
EXPOSE 8080
# defines the command to execute the application. Here, it runs the app module using Python.
CMD ["python","-m","app"]