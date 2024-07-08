FROM python:3.9-slim

RUN apt update && apt install git -y
WORKDIR /app
ADD ./data/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt
ADD ./app /app/

ENTRYPOINT [ "python","sync.py" ]