"""
Module for food item models
"""
from api.models.database import DatabaseConnection
from api.models.user_model import UserModel
from api.utils.singleton import Singleton


class FoodItemModel:
    """
    Model to hold food item data
    """
    def __init__(self, food_item=None, user_id=None):
        """
        Food Item model template
        :param food_item:
        """
        self.item_id = None
        self.item_name = food_item
        self.user_id = user_id
        self.item_status = "available"


class FoodItems(metaclass=Singleton):
    """
    Define food item module attributes accessed by callers
    """

    _table_ = "menu_items"
    _database_ = DatabaseConnection()

    def add_food_item(self, item_name=None, user_id=None) -> FoodItemModel or None:
        """
        Add new food item to the menu
        :param item_name:
        :param user_id:
        :return:
        """
        menu_data = FoodItemModel(item_name, user_id)

        del menu_data.item_id

        self._database_.insert(self._table_, menu_data.__dict__)

        return menu_data

    def find_item_by_name(self, item_name):
        """
        Find a specific item given it's name
        :param item_name:
        :return:
        """
        criteria = {'item_name': item_name}
        res = self._database_.find(self._table_, criteria=criteria)
        if res and isinstance(res, dict):
            item_data = FoodItemModel(res['item_name'], res['user_id'])
            item_data.item_id = res["item_id"]
            item_data.item_status = res['item_status']
            return item_data
        return None
