"""
Modelos de banco de dados - Infrastructure Layer

Modelos SQLAlchemy para persistência de dados.
Definem a estrutura das tabelas do banco de dados.

Aplicando o princípio Single Responsibility Principle (SRP) - 
cada modelo é responsável pela estrutura de uma tabela.
"""

from .user_model import UserModel
from .motor_vehicle_model import MotorVehicleModel
from .car_model import CarModel
from .motorcycle_model import MotorcycleModel
from .client_model import ClientModel
# from .employee_model import EmployeeModel  # TODO: Implementar quando necessário
from .sale_model import SaleModel
from .message_model import MessageModel

__all__ = [
    "UserModel",
    "MotorVehicleModel",
    "CarModel",
    "MotorcycleModel", 
    "ClientModel",
    # "EmployeeModel",  # TODO: Implementar quando necessário
    "SaleModel",
    "MessageModel"
]
