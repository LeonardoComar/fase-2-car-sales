# REST Presenters
# from .employee_presenter import EmployeePresenter  # TODO: Implementar quando necessário
from .client_presenter import ClientPresenter
from .sale_presenter import SalePresenter
from .message_presenter import MessagePresenter
from .car_presenter import CarPresenter
from .motorcycle_presenter import MotorcyclePresenter
from .user_presenter import UserPresenter

__all__ = [
    # "EmployeePresenter",  # TODO: Implementar quando necessário
    "ClientPresenter",
    "SalePresenter",
    "MessagePresenter",
    "CarPresenter",
    "MotorcyclePresenter",
    "UserPresenter",
]
