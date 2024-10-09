from typing import Type

from sqlalchemy.exc import IntegrityError

from app.exceptions import HttpException
from app.models import User, Advertisement
from app.security import check_password
from app.unit_of_work import UnitOfWork


class Service:
    def __init__(self):
        self._uow = UnitOfWork()

    def get_by_id(self, adv_id: int, model: Type[Advertisement]) -> dict:
        with self._uow as uow:
            advertisement = uow.session.query(model).filter(model.id == adv_id).first()
            if not advertisement:
                raise HttpException(404, 'advertisement does not exists')
            return advertisement.to_dict()

    def get_all(self, model: Type[Advertisement]):
        with self._uow as uow:
            advertisements = uow.session.query(model).all()
            result = [advertisement.to_dict() for advertisement in advertisements]
            return result

    def add(self, data: dict, model: Type[User] | Type[Advertisement]) -> dict:
        obj = model(**data)
        try:
            with self._uow as uow:
                uow.session.add(obj)
                uow.session.flush()
                return obj.to_dict()
        except IntegrityError as e:
            raise HttpException(409, str(e))

    def delete(self, adv_id: int, model: Type[Advertisement]) -> dict:
        with self._uow as uow:
            uow.session.query(model).filter(model.id == adv_id).delete()
            return {'deleted': adv_id}

    def verify_user_credentials(self, data: dict, model: Type[User]) -> str:
        with self._uow as uow:
            email, password = data.get('email'), data.get('password')
            user = uow.session.query(model).filter(model.email == email).first()
            if not user:
                raise HttpException(404, 'user does not exists')
            if not check_password(password, user.password):
                raise HttpException(400, 'invalid password')
            return user.email

    def get_user_id_by_email(self, email: str, model: Type[User]) -> int:
        with self._uow as uow:
            user = uow.session.query(model).filter(model.email == email).first()
            if not user:
                raise ValueError('user with this token does not exists in database')
            return user.id
