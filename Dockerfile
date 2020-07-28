FROM python:alpine3.8

#RUN mkdir -p /app/ConDeBot /data/ConDeBot
#WORKDIR /app/ConDeBot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk -U add haveged && rc-service haveged start && rc-update add haveged

COPY . .
RUN rm -r ./docker

ENTRYPOINT ["python", "./RollDas.py" ]
