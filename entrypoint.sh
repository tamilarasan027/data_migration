#!/bin/bash
# Download config.json based on the provided filename from S3
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
filename=$CONFIG_FILE_NAME
bucket=$S3_BUCKET
last_pulled_time=$PULLED_TIME
echo "Downloaded config.json"
aws s3 cp s3://$bucket/$filename /app/config.json
aws s3 cp s3://$bucket/$last_pulled_time /app/las_pulled_time.txt
# Run the ETL script
echo "Running ETL script"
python /app/sync_automation_kpis.py

aws s3 cp /app/las_pulled_time.txt s3://$bucket/$last_pulled_time