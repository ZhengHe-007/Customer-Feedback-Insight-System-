# Customer-Feedback-Insight-System-
This system will provide small businesses with easy-to-understand reports on the platform. 
Specifically: 
1. Identify business attributes, cities, and states that lead to positive/negative reviews. 
2. Uncover emerging trends and customer sentiments.



# Initial Datasets Pulling: https://www.yelp.com/dataset
Datasets used: yelp_academic_dataset_business.json, yelp_academic_dataset_review.json

# Tools 
1. AWS S3 Bucket
2. AWS Sagemaker Notebook
3. AWS RDS Postgre SQL
4. AWS VPC public & private subnets
5. AWS EC2 instance SSH & Flask

# Cloud Infrastructure Design
<img width="976" alt="Screenshot 2023-12-15 at 4 05 37 PM" src="https://github.com/ZhengHe-007/Customer-Feedback-Insight-System-/assets/105060699/5690a048-674d-41b9-b623-679cb0e7a5b2">



# Final Files:
1. sample_df.csv
2. flaskDB.py

# Final run execution
1. run flaskDB.py in ec2 instance 

# Note:
1. ‘Cleaned_sampled_dataset.csv’ is taken 1GB sample of the overall dataset(8GB+)
2. ‘sample_df.csv’ is the result from ‘Cleaned_sampled_dataset.csv’ after executing this file ’Sentiment Analysis’. 
3. ‘sample_df.csv’ has been transformed into RDS Postgre database by running ‘RDSPostgre.py’.
4.  run flaskDB.py in ec2 instance 
5. Interacting with the website: 44.197.239.78:5001
