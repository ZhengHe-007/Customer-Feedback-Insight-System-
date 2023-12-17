#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import psycopg2
from sqlalchemy import create_engine


# In[17]:


import pandas as pd
from sqlalchemy import create_engine


csv_file_path = 'sample_df.csv' 
sample_df = pd.read_csv(csv_file_path)


host = "database-1.ccpdrtqkicjw.us-east-1.rds.amazonaws.com" 
port = "5432"
user = "postgres"
password = "123456789"  
dbname = "testyelp"  

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

table_name = 'sample' 

try:
    sample_df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Successful PostgreSQL")
except Exception as e:
    print(f"error：{e}")


# In[ ]:


create_table_stmt = """
CREATE TABLE sample (
    business_id SERIAL PRIMARY KEY,
    review_star FLOAT NOT NULL,
    useful INT NOT NULL,
    funny INT NOT NULL,
    cool INT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    business_overall_star FLOAT NOT NULL,
    review_count INT NOT NULL,
    ByAppointmentOnly INT NOT NULL,
    BusinessAcceptsCreditCards INT NOT NULL,
    BikeParking INT NOT NULL,
    RestaurantsPriceRange2 INT NOT NULL,
    CoatCheck INT NOT NULL,
    RestaurantsTakeOut INT NOT NULL,
    RestaurantsDelivery INT NOT NULL,
    Caterers INT NOT NULL,
    WiFi INT NOT NULL,
    BusinessParking INT NOT NULL,
    WheelchairAccessible INT NOT NULL,
    HappyHour INT NOT NULL,
    OutdoorSeating INT NOT NULL,
    HasTV INT NOT NULL,
    RestaurantsReservations INT NOT NULL,
    DogsAllowed INT NOT NULL,
    GoodForKids INT NOT NULL,
    RestaurantsTableService INT NOT NULL,
    RestaurantsGoodForGroups INT NOT NULL,
    DriveThru INT NOT NULL,
    GoodForMeal INT NOT NULL,
    BusinessAcceptsBitcoin INT NOT NULL,
    Smoking INT NOT NULL,
    GoodForDancing INT NOT NULL,
    AcceptsInsurance INT NOT NULL,
    BYOB INT NOT NULL,
    Corkage INT NOT NULL,
    Open24Hours INT NOT NULL,
    RestaurantsCounterService INT NOT NULL,
    background_music INT NOT NULL,
    open_on_monday INT NOT NULL,
    open_on_tuesday INT NOT NULL,
    open_on_wednesday INT NOT NULL,
    open_on_thursday INT NOT NULL,
    open_on_friday INT NOT NULL,
    open_on_saturday INT NOT NULL,
    open_on_sunday INT NOT NULL,
    noise_average INT NOT NULL,
    noise_loud INT NOT NULL,
    noise_quiet INT NOT NULL,
    noise_very_loud INT NOT NULL,
    alcohol_beer_and_wine INT NOT NULL,
    alcohol_full_bar INT NOT NULL,
    alcohol_none INT NOT NULL,
    review_sentiment FLOAT NOT NULL,
    average_sentiment FLOAT NOT NULL
)

"""

# Execute 
cur.execute(create_table_stmt)

# Commit 
conn.commit()

# Close 
cur.close()
conn.close()


