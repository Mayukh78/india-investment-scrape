import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

engine = create_engine("postgresql://postgres@localhost:5432/postgres")
db = scoped_session(sessionmaker(bind=engine))

url = 'https://api.pushshift.io/reddit/submission/search/?subreddit=IndiaInvestments&title=bi%2Dweekly&size=500'

r = requests.get(url)

submission_list = r.json().get('data')
for submission in submission_list:
    id = submission.get('id')
    creation_time = submission.get('created_utc')

    db.execute(
        "INSERT INTO posts(post_id,created_utc) VALUES(:post_id,:created_utc)", \
        {"post_id": id, "created_utc": datetime.fromtimestamp(creation_time)})
    print(f"Inserted id-{id}, time-{creation_time} ")

db.commit()

print('Entered data successfully')