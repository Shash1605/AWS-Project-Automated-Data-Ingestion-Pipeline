import json
import pandas as pd
import boto3
import io
import re
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Initialize S3 client
s3 = boto3.client('s3')

# Lambda-specific NLTK setup
# NLTK needs a writable directory; /tmp is the only one available in Lambda
nltk.data.path.append("/tmp")
nltk.download('stopwords', download_dir="/tmp")

def clean_text(text):
    """Applies regex cleaning, stopword removal, and stemming."""
    # Replace email, urls, money, and numbers
    text = re.sub(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', 'emailaddr', str(text))
    text = re.sub(r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$', 'webaddress', text)
    text = re.sub(r'£|\$', 'moneysymb', text)
    text = re.sub(r'\d+(\.\d+)?', 'num', text)
    text = re.sub(r'[^\w\d\s]', ' ', text)
    text = text.lower()
    
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    
    words = text.split()
    cleaned = [ps.stem(w) for w in words if w not in stop_words]
    return " ".join(cleaned)

def lambda_handler(event, context):
    try:
        # 1. Capture the source bucket and file name from the S3 Event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # 2. Get the file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()), encoding="ISO-8859-1")
        
        # 3. Transform the data (Column 1 is usually the message)
        df['cleaned_text'] = df[df.columns[1]].apply(clean_text)
        
        # 4. Define destination and save
        output_bucket = "YOUR_PROCESSED_BUCKET_NAME" # Change this!
        output_key = f"processed/processed_{key}"
        
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=csv_buffer.getvalue())
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {key} and saved to {output_bucket}')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e