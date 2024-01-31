from utils.jwt import read_token, create_token
import datetime
import os

os.environ["JWT_SECRET_KEY"] = "helloworld"

start = datetime.datetime.now()
start += datetime.timedelta(minutes=10)
print(start)
payload = {
    "id": "1",
    "exp": start.timestamp()
}

token = create_token(payload)
print(token)
decoded = read_token(token)