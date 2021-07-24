import boto3
import pandas as pd
import training_scripts.domain.retriever as retriever

BUCKET = 's3-bucket-name-here'
REGION_NAME = 'region-name-here'
ACCESS_KEY = 'key-here'
SECRET_ACCESS_KEY = 'secret-key-here'

CONTENT_TYPE = 'csv'        #type of file to be uploaded
ACL = 'public-read'         #read permissions of uploaded file

TMP_FILE = '/tmp/tmp.csv'   #file to store data before sending to s3
S3_FILE = 'all_stories.csv' #name of file that will be uploaded to s3

N_DATASETS = 5              #number of datasets to scrape from gdelt
BALANCE_DATA = True         #whether or not to have scraped stories be balanced geographically
SAMPLE_SIZE = 1             #fraction of stories to be scraped (1=100%)

COLUMNS_TO_KEEP = ['ARTICLE.TITLE',
                   'ARTICLE.TEXT',
                   'GDELT.Day',
                   'GDELT.DATEADDED',
                   'GDELT.Actor1Geo_Lat',
                   'GDELT.Actor1Geo_Long',
                   'GDELT.Actor1Geo_Fullname',
                   'GDELT.SOURCEURL']

def scrape_news_stories():
    #connect to s3
    s3 = boto3.client("s3",
                      region_name= REGION_NAME,
                      aws_access_key_id= ACCESS_KEY,
                      aws_secret_access_key= SECRET_ACCESS_KEY)

    #scrape stories
    news = retriever.scrape_latest_gdelt_datasets(N_DATASETS, BALANCE_DATA, SAMPLE_SIZE)

    #store in pandas df and remove rows with null values
    dataframe = pd.json_normalize(news)[COLUMNS_TO_KEEP].dropna()     

    #store data in /tmp 
    dataframe.to_csv(TMP_FILE)

    #upload to s3
    s3.upload_file(Filename=TMP_FILE, Bucket=BUCKET, Key=S3_FILE, ExtraArgs={'ContentType': CONTENT_TYPE, 'ACL': ACL})
        
def lambda_handler(event, context):
    scrape_news_stories()
    return {
            'message':'success'
            }
