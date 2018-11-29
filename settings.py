import os

# DB

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
MINSIZE = 1
MAXSIZE = 5

# AUTH

JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_TOKEN_SCHEME = os.environ.get("JWT_TOKEN_SCHEME", "Auth")
JWT_HEADER_NAME = os.environ.get("JWT_HEADER_NAME", "Authorization")
JWT_TTL_SEC = int(os.environ.get("JWT_SECRET", 3600))
