FROM python:3
ADD hello_world.py /
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD [ "python", "./hello_world.py" ]
