FROM public.ecr.aws/lambda/python:3.8

COPY app.py   ./
COPY requirements.txt   ./
COPY fb_creds.yml   ./

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["app.handler"]
