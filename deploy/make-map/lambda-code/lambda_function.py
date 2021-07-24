import boto3
import pandas as pd
import coronavirus_map.domain.mapper as mapper 

BUCKET = 's3-bucket-name-here'
REGION_NAME = 'region-name-here'
ACCESS_KEY = 'key-here'
SECRET_ACCESS_KEY = 'secret-key-here'

CONTENT_TYPE = 'text/html'              #type of file to be uploaded
ACL = 'public-read'                     #read permissions of uploaded file

TMP_CSV_FILE = '/tmp/covid_stories.csv' #file to store covid stories
TMP_HTML_FILE = '/tmp/map.html'         #file to store map in before sending to s3

S3_CSV_FILE = 'covid_stories.csv'       #file that contains stories to put on map
S3_HTML_FILE = 'index.html'             #file that will be uploaded to s3

def write_file(data, filename):
    with open(filename, 'w') as f:
        f.write(data)

def create_map():
    #connect to s3
    s3 = boto3.client("s3",
                      region_name= REGION_NAME,
                      aws_access_key_id= ACCESS_KEY,
                      aws_secret_access_key= SECRET_ACCESS_KEY)

    #get covid stories from s3
    s3.download_file(Filename=TMP_CSV_FILE, Bucket=BUCKET, Key=S3_CSV_FILE)

    #load into df
    covid_news = pd.read_csv(TMP_CSV_FILE)

    #create map
    plotly_map = mapper.generate_map(covid_news)

    #write map to /tmp 
    write_file(data=plotly_map, filename=TMP_HTML_FILE)

    #upload to s3
    s3.upload_file(Filename=TMP_HTML_FILE, Bucket=BUCKET, Key=S3_HTML_FILE, ExtraArgs={'ContentType': CONTENT_TYPE, 'ACL': ACL})

def lambda_handler(event, context):
    create_map()
    return {
            'message':'success'
            }
