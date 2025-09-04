"""
Gateways de persistência - Adapter Layer

Os gateways implementam as interfaces de repositório definidas no domínio,
fornecendo acesso aos dados através do SQLAlchemy.

Aplicando o padrão Gateway e o princípio Dependency Inversion Principle (DIP).
"""

from .user_gateway import UserGateway
from .car_gateway import CarGateway
from .client_gateway import ClientGateway
from .motorcycle_gateway import MotorcycleGateway
from .employee_gateway import EmployeeGateway
from .sale_gateway import SaleGateway
from .message_gateway import MessageGateway

__all__ = [
    "UserGateway",
    "CarGateway",
    "ClientGateway",
    "MotorcycleGateway",
    "EmployeeGateway",
    "SaleGateway",
    "MessageGateway"
]
