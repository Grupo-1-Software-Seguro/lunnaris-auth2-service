from ..src.utils.jwt import read_token, create_token
import datetime

start = datetime.datetime.now()
start += datetime.timedelta(minutes=10)

payload = {
    "id": "1",
    "exp": start
}

token = create_token(payload)

decoded = read_token(token)