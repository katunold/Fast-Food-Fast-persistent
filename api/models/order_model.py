"""
Module for order model
"""
import datetime

from api.models.database import DatabaseConnection
from api.models.food_item_model import FoodItems
from api.utils.singleton import Singleton


class OrderModel:
    """
    Model to hold order data
    """

    def __init__(self, user_id=None, order_item=None, special_notes=None):
        self.order_id = None
        self.user_id = user_id
        self.order_item = order_item
        self.special_notes = special_notes
        self.order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.item_id = None
        self.order_status = 'New'


class Orders(metaclass=Singleton):
    """
     Define token module attributes accessed by callers
     """
    _table_ = "order"
    _database_ = DatabaseConnection()
    menu = FoodItems()

    def make_order(self, user_id=None, order_item=None, special_notes=None):
        """
        Make new order
        :param user_id:
        :param order_item:
        :param special_notes:
        :return:
        """
        order_data = OrderModel(user_id, order_item, special_notes)
        menu_data = self.menu.find_item_by_name(order_item)
        order_data.item_id = menu_data.item_id
        del order_data.order_id

        self._database_.insert(self._table_, order_data.__dict__)

        return order_data
