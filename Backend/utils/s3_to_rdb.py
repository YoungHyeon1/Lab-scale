import pandas as pd

matches_data = pd.read_csv('s3://mybucket/myfile.csv')

# pandas to sql

from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
matches_data.to_sql('matches', con=engine)


