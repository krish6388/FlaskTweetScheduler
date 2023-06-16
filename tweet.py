from os import environ
import gspread
import tweepy,time
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

customer_key=environ["customer_key"]
customer_token=environ["customer_token"]
access_token=environ["access_token"]
access_token_secret=environ["access_token_secret"]

auth = tweepy.OAuth1UserHandler(
    customer_key, customer_token, access_token, access_token_secret
)

api = tweepy.API(auth)

gc = gspread.service_account(filename = 'gCredentials.json')
sh = gc.open_by_key('1nZ1nxXPDoPGW3sH-8IxBht2Ulplzd6kI5R6BEveCOKE')
worksheet = sh.sheet1

INTERVAL = int(environ["INTERVAL"])
DEBUG = environ["DEBUG"] == '1'

def main():
    while True:
        time.sleep(3)
        tweet_records = worksheet.get_all_records()
        current_time = datetime.utcnow() + timedelta(hours=2)
        logger.info(f'{len(tweet_records)} tweets found at {current_time.time()}')

        for idx, tweet in enumerate(tweet_records, start=2):
            msg=tweet['message']
            time_str=tweet['time']
            done=tweet['done']
            date_time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            if not done:
                now_time_cet = datetime.utcnow() + timedelta(hours=2)
                if  date_time_obj < now_time_cet:
                    logger.info('this should be tweeted')
                    try:
                        # if not DEBUG:
                        api.update_status(msg)
                        worksheet.update_cell(idx, 3, 1)
                    except Exception as e:
                        logger.warning(f'Exception during tweet {e}')



if __name__ == '__main__':
    main()
