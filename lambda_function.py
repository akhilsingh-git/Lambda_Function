import boto3
import os
import datetime
import time
import re

# Fetching environment variables
GROUP_NAME = os.environ['GROUP_NAME']
DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']
PREFIX = os.environ['PREFIX']
NDAYS = os.environ['NDAYS']
nDays = int(NDAYS)

# Calculating the date range for logs
StartDate = datetime.datetime.now() - datetime.timedelta(seconds=300)
EndDate = datetime.datetime.now()

# Convert the from & to Dates to milliseconds
fromDate = int(StartDate.timestamp() * 1000)
toDate = int(EndDate.timestamp() * 1000)

# Creating the bucket prefix based on date
BUCKET_PREFIX = os.path.join(PREFIX, StartDate.strftime('%Y{0}%m{0}%d').format(os.path.sep))


def process_logs(log_events):
    """
    Process the log events, removing timestamps and returning modified logs.
    """
    processed_logs = []
    for event in log_events:
        # Use regex to remove timestamps from log messages
        log_content = re.sub(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s', '', event['message'])
        processed_logs.append(log_content)
    return processed_logs


def lambda_handler(event, context):
    client = boto3.client('logs')
    log_groups = GROUP_NAME.split(",")  # Splitting the log group names by comma

    for log_group in log_groups:
        try:
            # Fetch the log streams for the log group
            streams_response = client.describe_log_streams(logGroupName=log_group.strip())
            log_streams = [stream['logStreamName'] for stream in streams_response['logStreams']]

            for log_stream in log_streams:
                # For each log stream, get the log events
                log_events = client.get_log_events(
                    logGroupName=log_group.strip(),
                    logStreamName=log_stream,
                    startTime=fromDate,
                    endTime=toDate
                )['events']

                # Process the logs to remove timestamps
                processed_logs = process_logs(log_events)

                # Send processed logs to S3
                s3 = boto3.client('s3')
                s3_key = f"{BUCKET_PREFIX}/{log_group}/{log_stream}.txt"
                s3.put_object(Bucket=DESTINATION_BUCKET, Key=s3_key, Body="\n".join(processed_logs))

                print(f"Processed logs for log group: {log_group}, log stream: {log_stream}")

            time.sleep(60)  # Sleep for 60 seconds before processing the next log group
            
        except client.exceptions.LimitExceededException:
            print(f"Limit exceeded for log group {log_group}. Retrying...")
            time.sleep(120)  # Sleep for 120 seconds before retrying
        except Exception as e:
            print(f"Error processing logs for log group {log_group}: {str(e)}")
