from flask import jsonify

from app.core import app, engine
from app.exceptions import HttpException
from app.models import Base
from app.urls import blueprint


@app.errorhandler(HttpException)
def error_handler(e: HttpException):
    response = jsonify({"detail": e.description})
    response.status_code = e.status_code
    return response


Base.metadata.create_all(bind=engine)

app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
