import os


def get_base_uri_from_env():
    host = os.environ.get('POSTGRES_HOST')
    db_name = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    if host and db_name and user and password:
        return f"postgresql://{user}:{password}@{host}/{db_name}"
    return None
