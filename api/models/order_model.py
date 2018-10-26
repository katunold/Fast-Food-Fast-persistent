"""
Module for order model
"""
import datetime
from typing import List

from flask import jsonify

from api.models.database import DatabaseConnection
from api.models.food_item_model import FoodItems
from api.models.user_model import Users
from api.utils.singleton import Singleton


class OrderModel:
    """
    Model to hold order data
    """

    def __init__(self, user_id=None, order_item=None, special_notes=None):
        self.order_id = None
        self.order_cost = None
        self.user_id = user_id
        self.client = None
        self.client_contact = None
        self.client_email = None
        self.order_item = order_item
        self.special_notes = special_notes
        self.order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.item_id = None
        self.order_status = 'New'


class Orders(metaclass=Singleton):
    """
     Define token module attributes accessed by callers
     """
    _table_ = "orders"
    _database_ = DatabaseConnection()
    menu = FoodItems()
    user = Users()

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
        del order_data.order_id, order_data.client, order_data.client_contact, order_data.client_email, \
            order_data.order_cost

        self._database_.insert(self._table_, order_data.__dict__)

        return order_data

    def get_orders(self) -> [OrderModel]:
        """
        Get all orders
        :return:
        """
        response = self._database_.find(self._table_, criteria=None)

        if response:
            if isinstance(response, list) and len(response) > 1:
                data: List[OrderModel] = []
                for res in response:
                    order_data = OrderModel(res['user_id'], res['order_item'], res['special_notes'])
                    client_data = self.user.find_user_by_id(res['user_id'])
                    item_data = self.menu.find_item_by_id(res["item_id"])
                    order_data.client = client_data.user_name
                    order_data.client_contact = client_data.contact
                    order_data.client_email = client_data.email
                    order_data.order_cost = item_data.price
                    order_data.item_id = res['item_id']
                    order_data.order_id = res['order_id']
                    order_data.order_date = res['order_date']
                    order_data.order_status = res['order_status']
                    del order_data.item_id
                    data.insert(0, order_data)
                return data
            elif isinstance(response, dict) or (isinstance(response, list) and len(response) == 1):
                if isinstance(response, list):
                    response = response[0]
                order_data = OrderModel(response['user_id'], response['order_item'], response['special_notes'])
                client_data = self.user.find_user_by_id(response['user_id'])
                item_data = self.menu.find_item_by_id(response["item_id"])
                order_data.client = client_data.user_name
                order_data.client_contact = client_data.contact
                order_data.client_email = client_data.email
                order_data.order_cost = item_data.price
                order_data.item_id = response['item_id']
                order_data.order_id = response['order_id']
                order_data.order_date = response['order_date']
                order_data.order_status = response['order_status']
                del order_data.item_id
                return order_data
        return None

    def order_history(self, user_id) -> [OrderModel]:
        """
        Get order history of a user
        :return:
        """
        criteria = {'user_id': user_id}
        response = self._database_.find(self._table_, criteria=criteria)

        if response:
            if isinstance(response, list) and len(response) > 1:
                data: List[OrderModel] = []
                for res in response:
                    order_data = OrderModel(res['user_id'], res['order_item'], res['special_notes'])
                    client_data = self.user.find_user_by_id(res['user_id'])
                    item_data = self.menu.find_item_by_id(res["item_id"])
                    order_data.client = client_data.user_name
                    order_data.client_contact = client_data.contact
                    order_data.client_email = client_data.email
                    order_data.order_cost = item_data.price
                    order_data.item_id = res['item_id']
                    order_data.order_id = res['order_id']
                    order_data.order_date = res['order_date']
                    order_data.order_status = res['order_status']
                    del order_data.item_id
                    data.insert(0, order_data)
                return data
            elif isinstance(response, dict) or (isinstance(response, list) and len(response) == 1):
                if isinstance(response, list):
                    response = response[0]
                order_data = OrderModel(response['order_id'], response['order_item'], response['special_notes'])
                client_data = self.user.find_user_by_id(response['user_id'])
                item_data = self.menu.find_item_by_id(response["item_id"])
                order_data.client = client_data.user_name
                order_data.client_contact = client_data.contact
                order_data.client_email = client_data.email
                order_data.order_cost = item_data.price
                order_data.item_id = response['item_id']
                order_data.order_id = response['order_id']
                order_data.order_date = response['order_date']
                order_data.order_status = response['order_status']
                del order_data.item_id
                return order_data
        return None

    def find_order_by_id(self, order_id):
        criteria = {'order_id': order_id}
        res = self._database_.find(self._table_, criteria=criteria)
        if res and isinstance(res, dict):
            order_data = OrderModel(res['order_id'], res['order_item'], res['special_notes'])
            client_data = self.user.find_user_by_id(res['user_id'])
            item_data = self.menu.find_item_by_id(res["item_id"])
            order_data.client = client_data.user_name
            order_data.client_contact = client_data.contact
            order_data.client_email = client_data.email
            order_data.order_cost = item_data.price
            order_data.item_id = res['item_id']
            order_data.order_id = res['order_id']
            order_data.order_date = res['order_date']
            order_data.order_status = res['order_status']
            del order_data.item_id
            return order_data
        return None

    def update_order(self, order_id, order_status):
        selection = {
            'order_id': order_id
        }
        new_update = {
            'order_status': order_status
        }
        self._database_.update(self._table_, selection, new_update)
        response_object = {
            'status': 'success',
            'message': 'Status has been updated'
        }
        return jsonify(response_object), 202
