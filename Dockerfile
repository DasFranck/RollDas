FROM python:alpine3.8

#RUN mkdir -p /app/ConDeBot /data/ConDeBot
#WORKDIR /app/ConDeBot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk add --no-cache gcc musl-dev \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del gcc
RUN apk -U add openrc haveged

COPY . .

ENTRYPOINT ["python", "./RollDas.py" ]
