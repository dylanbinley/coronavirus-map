import boto3
import pandas as pd
import coronavirus_map.domain.classifier as classifier

BUCKET = 's3-bucket-name-here'
REGION_NAME = 'region-name-here'
ACCESS_KEY = 'key-here'
SECRET_ACCESS_KEY = 'secret-key-here'

CONTENT_TYPE = 'csv'        #type of file to be uploaded
ACL = 'public-read'         #read permissions of uploaded file

S3_CSV_ALL = 'all_stories.csv'
S3_CSV_COVID = 'covid_stories.csv'

TMP_CSV_ALL = '/tmp/all_stories.csv'
TMP_CSV_COVID= '/tmp/covid_stories.csv'

COLUMNS_TO_KEEP = ['ARTICLE.TITLE',
                   'ARTICLE.TEXT',
                   'GDELT.Day',
                   'GDELT.DATEADDED',
                   'GDELT.Actor1Geo_Lat',
                   'GDELT.Actor1Geo_Long',
                   'GDELT.Actor1Geo_Fullname',
                   'GDELT.SOURCEURL']

N_STORIES_TO_KEEP = 200

TITLE_COL = 'ARTICLE.TITLE'
DATE_COL = 'GDELT.DATEADDED'

def update_covid_stories():
    #connect to s3
    s3 = boto3.client("s3",
                      region_name= REGION_NAME,
                      aws_access_key_id= ACCESS_KEY,
                      aws_secret_access_key= SECRET_ACCESS_KEY)

    # get all stories csv
    s3.download_file(Filename=TMP_CSV_ALL, Bucket=BUCKET, Key=S3_CSV_ALL)
    s3.download_file(Filename=TMP_CSV_COVID, Bucket=BUCKET, Key=S3_CSV_COVID)

    #load data into pd dataframes
    df_new_stories = pd.read_csv(TMP_CSV_ALL)[COLUMNS_TO_KEEP].dropna()
    df_existing_covid_stories = pd.read_csv(TMP_CSV_COVID)[COLUMNS_TO_KEEP].dropna()

    #filter out non covid new data
    df_new_covid_stories = classifier.find_coronavirus_stories(df_new_stories)

    #combine new and old covid stories    
    covid_news = pd.concat([df_new_covid_stories, 
                            df_existing_covid_stories], 
                            axis=0).drop_duplicates(subset=[TITLE_COL])

    #sort the stories by date added and save most recent ones 
    most_recent_covid_stories = covid_news.sort_values(by=[DATE_COL], ascending=False).head(N_STORIES_TO_KEEP)

    #store data in /tmp
    most_recent_covid_stories.to_csv(TMP_CSV_COVID)

    #upload to s3
    s3.upload_file(Filename=TMP_CSV_COVID, Bucket=BUCKET, Key=S3_CSV_COVID, ExtraArgs={'ContentType': CONTENT_TYPE, 'ACL': ACL})

def lambda_handler(event, context):
    update_covid_stories()
    return {
            'message':'success'
            }
