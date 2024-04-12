import os
from dotenv import load_dotenv
from S3Client import S3Client
from league_cralwer import LeagueCrawler


if __name__ == '__main__':
    load_dotenv()
    cralwer = LeagueCrawler()
    response = cralwer.get_league_v4()

