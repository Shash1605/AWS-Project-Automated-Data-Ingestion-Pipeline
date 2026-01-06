# Automated Data Ingestion & NLP Preprocessing Pipeline

An event-driven, serverless data pipeline built on AWS to automate the ingestion, cleaning, and cataloging of SMS datasets for spam classification.



## 🏗️ Architecture
1. **Amazon S3 (Raw Zone):** Acts as the landing zone for incoming CSV data.
2. **AWS Lambda:** Triggered automatically by S3 uploads; executes a Python script for NLP-based text cleaning (Regex, Stemming, Stopword removal).
3. **Amazon S3 (Processed Zone):** Stores the standardized, "ML-ready" CSV output.
4. **AWS Glue:** A crawler scans the processed data to discover the schema and update the Data Catalog.
5. **Amazon Athena:** Provides a serverless SQL interface to query and validate the processed data.

## 🛠️ Tech Stack
- **Cloud:** AWS (S3, Lambda, Glue, Athena, CloudWatch)
- **Language:** Python (Pandas, Boto3, NLTK)
- **Data Engineering:** ETL, Event-Driven Architecture, Schema-on-Read

## 🚀 Key Features
- **Serverless Scaling:** Zero infrastructure to manage; scales automatically with data volume.
- **Automated Text Normalization:** Handles messy text patterns (URLs, emails, symbols) using advanced Regular Expressions.
- **Cost Optimization:** Utilizes AWS Free Tier limits to maintain a zero-cost operational profile.

## 📊 Sample Athena Query
Once the pipeline finishes, data is queried using SQL:
```sql
SELECT cleaned_text, label 
FROM "spam_db"."processed_data" 
WHERE label = 1 
LIMIT 10;
