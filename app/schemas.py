from pydantic import BaseModel, constr


class CreateUserTokenSchema(BaseModel):
    email: constr(max_length=50)
    password: str


class CreateAdvertisementSchema(BaseModel):
    title: constr(max_length=50)
    description: constr(max_length=100)
