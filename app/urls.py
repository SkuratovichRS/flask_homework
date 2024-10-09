from flask import Blueprint

from app.views import CreateUserView, CreateTokenView, AdvertisementViewSet, GetAllAdvertisementView

blueprint = Blueprint('api/v1', __name__)

user_view = CreateUserView.as_view('user_view')
token_view = CreateTokenView.as_view('token_view')
advertisement_view_set = AdvertisementViewSet.as_view('advertisement_view_set')
advertisement_get_all_view = GetAllAdvertisementView.as_view('get_all_advertisement_view')

blueprint.add_url_rule('/user/', view_func=user_view, methods=['POST'])
blueprint.add_url_rule('/token/', view_func=token_view, methods=['POST'])
blueprint.add_url_rule('/advertisement/', view_func=advertisement_view_set, methods=['POST'])
blueprint.add_url_rule('/advertisement/', view_func=advertisement_get_all_view, methods=['GET'])
blueprint.add_url_rule('/advertisement/<int:adv_id>/', view_func=advertisement_view_set,
                       methods=['GET', 'DELETE'])
