FROM python:3.9
WORKDIR /scrapper
COPY . /scrapper/
RUN pip install -r requirements.txt
CMD python /scrapper/app.py
