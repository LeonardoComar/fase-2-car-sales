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
    GetEmployeeUseCase,
    UpdateEmployeeUseCase,
    DeleteEmployeeUseCase,
    ListEmployeesUseCase,
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
    SaleStatisticsUseCase,
)

# Message Use Cases
from .messages import (
    CreateMessageUseCase,
    GetMessageByIdUseCase,
    GetAllMessagesUseCase,
    StartServiceUseCase,
    UpdateMessageStatusUseCase,
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
    "GetEmployeeUseCase",
    "UpdateEmployeeUseCase",
    "DeleteEmployeeUseCase",
    "ListEmployeesUseCase",
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
    "SaleStatisticsUseCase",
    # Message Use Cases
    "CreateMessageUseCase",
    "GetMessageByIdUseCase",
    "GetAllMessagesUseCase",
    "StartServiceUseCase",
    "UpdateMessageStatusUseCase",
    # User Use Cases
    "CreateUserUseCase",
    "GetUserUseCase",
    "AuthenticateUserUseCase",
]
