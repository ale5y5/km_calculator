FROM python:3.7-alpine

WORKDIR /var/km_calculator/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./webapp.py" ]
