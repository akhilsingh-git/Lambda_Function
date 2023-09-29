# Steps:
1.) Do not forget to add environment variable available in Configuration tab DESTINATION_BUCKET	<name of the bucket>, GROUP_NAME <name of the group separated by , in case of multiple 
groups, NDAYS	0 (for today, 1 for yesterday and so on) ,PREFIX	exported (it would appear under this folder in your bucket).
2.) Depending on the size of the logs you may need to increase the Timeout of the lambda function in general configuration.
3.) Also, memory in some cases
# Bucket Policy: 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.ap-south-1.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::<bucketname>"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.ap-south-1.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::<bucketname>/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
