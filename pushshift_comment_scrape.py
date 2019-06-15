import requests
from datetime import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

engine = create_engine("postgresql://postgres@localhost:5432/postgres")
db = scoped_session(sessionmaker(bind=engine))

posts_list= db.execute("SELECT post_id from posts ORDER BY created_utc ").fetchall()

for post in posts_list:
    count=0

    url='https://api.pushshift.io/reddit/submission/comment_ids/'+post[0]
    r= requests.get(url)
    comment_list=r.json().get('data')

    for comment in comment_list:
        url='https://api.pushshift.io/reddit/comment/search?ids='+comment
        r=requests.get(url)
        content = r.json().get('data')
        parent_id = content[0].get('parent_id')

        if parent_id[0:2]=='t1':
            parent_id=parent_id[3:len(parent_id)-1]
        else:
            parent_id = post[0]
        content = content[0].get('body')
        db.execute("INSERT INTO comments(comment_id,post_id,parent_comment_id,comment_body) VALUES(:comment_id,:post_id,:parent_comment_id,:comment_body)", \
                {"comment_id":comment,"post_id":post[0],"parent_comment_id":parent_id,"comment_body":content})
        count +=1

    db.commit()
    print(f'entered {count} rows of {post[0]} ')

