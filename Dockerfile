FROM python:3.9
RUN apt-get update && apt-get install -y awscli
WORKDIR /app
COPY requirement.txt /app
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app
RUN chmod +x entrypoint.sh sync_automation_kpis.py las_pulled_time.txt

ENTRYPOINT ["./entrypoint.sh"]
