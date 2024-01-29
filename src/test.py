from utils import create_recover_token, validate_recover_token
from dotenv import load_dotenv

load_dotenv('.env')
token = create_recover_token(10)

decoded = validate_recover_token(token)

print(decoded)
