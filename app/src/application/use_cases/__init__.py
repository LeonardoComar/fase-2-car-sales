# Application Use Cases

# Client Use Cases
from .clients import (
    CreateClientUseCase,
    GetClientByIdUseCase,
    GetClientByCpfUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase,
    ListClientsUseCase,
    UpdateClientStatusUseCase,
)

# Employee Use Cases
from .employees import (
    CreateEmployeeUseCase,
    GetEmployeeByIdUseCase,
    UpdateEmployeeUseCase,
    DeleteEmployeeUseCase,
    ListEmployeesUseCase,
    PromoteEmployeeUseCase,
    UpdateEmployeeStatusUseCase,
)

# Vehicle Use Cases
from .vehicles import (
    CreateCarUseCase,
    CreateMotorcycleUseCase,
    GetCarUseCase,
    GetMotorcycleUseCase,
    UpdateCarUseCase,
    UpdateMotorcycleUseCase,
    DeleteCarUseCase,
    DeleteMotorcycleUseCase,
    SearchCarsUseCase,
    SearchMotorcyclesUseCase,
)

# Sale Use Cases
from .sales import (
    CreateSaleUseCase,
    GetSaleByIdUseCase,
    UpdateSaleUseCase,
    DeleteSaleUseCase,
    ListSalesUseCase,
    UpdateSaleStatusUseCase,
    GetSalesStatisticsUseCase,
)

# Message Use Cases
from .messages import (
    CreateMessageUseCase,
    GetMessageByIdUseCase,
    UpdateMessageUseCase,
    DeleteMessageUseCase,
    ListMessagesUseCase,
    AssignMessageUseCase,
    UpdateMessageStatusUseCase,
    GetMessagesStatisticsUseCase,
)

# User Use Cases
from .users import (
    CreateUserUseCase,
    GetUserUseCase,
    AuthenticateUserUseCase,
)

__all__ = [
    # Client Use Cases
    "CreateClientUseCase",
    "GetClientByIdUseCase", 
    "GetClientByCpfUseCase",
    "UpdateClientUseCase",
    "DeleteClientUseCase",
    "ListClientsUseCase",
    "UpdateClientStatusUseCase",
    # Employee Use Cases
    "CreateEmployeeUseCase",
    "GetEmployeeByIdUseCase",
    "UpdateEmployeeUseCase",
    "DeleteEmployeeUseCase",
    "ListEmployeesUseCase",
    "PromoteEmployeeUseCase",
    "UpdateEmployeeStatusUseCase",
    # Vehicle Use Cases
    "CreateCarUseCase",
    "CreateMotorcycleUseCase",
    "GetCarUseCase",
    "GetMotorcycleUseCase",
    "UpdateCarUseCase",
    "UpdateMotorcycleUseCase",
    "DeleteCarUseCase",
    "DeleteMotorcycleUseCase",
    "SearchCarsUseCase",
    "SearchMotorcyclesUseCase",
    # Sale Use Cases
    "CreateSaleUseCase",
    "GetSaleByIdUseCase",
    "UpdateSaleUseCase",
    "DeleteSaleUseCase",
    "ListSalesUseCase",
    "UpdateSaleStatusUseCase",
    "GetSalesStatisticsUseCase",
    # Message Use Cases
    "CreateMessageUseCase",
    "GetMessageByIdUseCase",
    "UpdateMessageUseCase",
    "DeleteMessageUseCase",
    "ListMessagesUseCase",
    "AssignMessageUseCase",
    "UpdateMessageStatusUseCase",
    "GetMessagesStatisticsUseCase",
    # User Use Cases
    "CreateUserUseCase",
    "GetUserUseCase",
    "AuthenticateUserUseCase",
]
