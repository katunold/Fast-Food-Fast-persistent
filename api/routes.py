"""
Urls class , to handel request urls,
"""

from api.controllers.login_controller import LoginController
from api.controllers.logout_controller import LogoutController
from api.controllers.menu_controller import MenuController
from api.controllers.order_controller import OrderController
from api.controllers.sign_up_controller import SignUpController


class Urls:
    """
    Class to generate urls
    """

    @staticmethod
    def generate(app):

        """Authentication routes"""
        app.add_url_rule('/api/v1/auth/signup/', view_func=SignUpController.as_view('sign_up_user'),
                         methods=['POST'], strict_slashes=False)

        app.add_url_rule('/api/v1/auth/login/', view_func=LoginController.as_view('login_user'),
                         methods=['POST'], strict_slashes=False)

        app.add_url_rule('/api/v1/auth/logout/', view_func=LogoutController.as_view('logout'),
                         methods=['POST'], strict_slashes=False)

        """Menu routes"""
        app.add_url_rule('/api/v1/menu', view_func=MenuController.as_view('add_to_menu'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/menu', view_func=MenuController.as_view('get_menu'),
                         methods=['GET'], strict_slashes=False)

        """Order routes"""
        app.add_url_rule('/api/v1/orders', view_func=OrderController.as_view('post_order'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/orders', view_func=OrderController.as_view('get_orders'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/orders/<int:order_id>', view_func=OrderController.as_view('get_an_order'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/orders/<int:order_id>', view_func=OrderController.as_view('update_order_status'),
                         methods=['PUT'], strict_slashes=False)
        app.add_url_rule('/api/v1/users/orders', view_func=LoginController.as_view('order_history'),
                         methods=['GET'], strict_slashes=False)
