AWS Lambda Log Exporter to S3
This AWS Lambda function is designed to export logs to an S3 bucket. Follow the steps below to set it up correctly.

Setup Steps
Environment Variables:

DESTINATION_BUCKET: The target S3 bucket where logs will be exported.
GROUP_NAME: Name of the CloudWatch Log Group. If you have multiple groups, separate them with commas.
NDAYS: Number of days in the past for which logs are to be exported. Use 0 for today, 1 for yesterday, and so on.
PREFIX: The logs will be placed under this folder in your S3 bucket. For example, if you set this to "exported", the logs will appear under the "exported" folder in your bucket.
Lambda Timeout:
Depending on the size of the logs, you might need to adjust the timeout of the Lambda function. Navigate to the general configuration of your Lambda function to do this.

Lambda Memory:
In certain cases, you might need to allocate more memory to your Lambda function. Adjust this in the Lambda configuration if required.

S3 Bucket Policy
To allow the Lambda function to export logs to your S3 bucket, you need to attach the following bucket policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "logs.ap-south-1.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::<YOUR_BUCKET_NAME>"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "logs.ap-south-1.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::<YOUR_BUCKET_NAME>/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
