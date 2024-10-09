from pydantic import ValidationError

from app.exceptions import HttpException


def validate_request_data(request_data: dict, schema):
    try:
        return schema(**request_data).model_dump()
    except ValidationError as e:
        error = e.errors()[0]
        error.pop("ctx", None)
        raise HttpException(400, error)
