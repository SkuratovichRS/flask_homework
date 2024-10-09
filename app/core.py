from flask import Flask
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import Settings

engine = create_engine(
    f"postgresql://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}@{Settings.POSTGRES_HOST}:"
    f"{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}",
)

Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Settings.SECRET_KEY

jwt = JWTManager(app)
