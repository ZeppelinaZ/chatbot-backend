import os

from app.providers.postgresDBProvider import PostgresDBProvider

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE = PostgresDBProvider(DATABASE_URL)
