from application.models import *
from application import cache

@cache.memoize(50)
def get_cards(list_id):
    list = List.query.filter_by(id=list_id).first()
    cards = list.cards
    return cards
