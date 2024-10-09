from flask import request, jsonify, Response
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.exceptions import HttpException
from app.models import User, Advertisement
from app.schemas import CreateUserTokenSchema, CreateAdvertisementSchema
from app.security import hash_password
from app.service import Service
from app.validation import validate_request_data

service = Service()


class CreateUserView(MethodView):
    @staticmethod
    def post() -> tuple[Response, int]:
        validated_data = validate_request_data(request.json, CreateUserTokenSchema)
        validated_data['password'] = hash_password(validated_data['password'])
        user_dict = service.add(validated_data, User)
        return jsonify(user_dict), 201


class CreateTokenView(MethodView):
    @staticmethod
    def post() -> tuple[Response, int]:
        validated_data = validate_request_data(request.json, CreateUserTokenSchema)
        email = service.verify_user_credentials(validated_data, User)
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 201


class AdvertisementViewSet(MethodView):
    @staticmethod
    def get(adv_id: int) -> tuple[Response, int]:
        advertisement_dict = service.get_by_id(adv_id, Advertisement)
        return jsonify(advertisement_dict), 200

    @staticmethod
    @jwt_required()
    def post() -> tuple[Response, int]:
        validated_data = validate_request_data(request.json, CreateAdvertisementSchema)
        current_user_email = get_jwt_identity()
        current_user_id = service.get_user_id_by_email(current_user_email, User)
        validated_data['creator'] = current_user_id
        advertisement_dict = service.add(validated_data, Advertisement)
        return jsonify(advertisement_dict), 201

    @staticmethod
    @jwt_required()
    def delete(adv_id: int) -> tuple[Response, int]:
        current_user_email = get_jwt_identity()
        current_user_id = service.get_user_id_by_email(current_user_email, User)
        creator = service.get_by_id(adv_id, Advertisement).get('creator')
        if current_user_id != creator:
            raise HttpException(403, 'you can delete only your own advertisements')
        response = service.delete(adv_id, Advertisement)
        return jsonify(response), 204


class GetAllAdvertisementView(MethodView):
    @staticmethod
    def get() -> tuple[Response, int]:
        response = service.get_all(Advertisement)
        return jsonify(response), 200
