"""
Módulo de dependências para injeção de dependência.

Aplicando o princípio Dependency Inversion Principle (DIP) - 
módulos de alto nível não dependem de módulos de baixo nível.

Versão simplificada enquanto a infraestrutura está sendo implementada.
"""

# Use Cases - User
from src.application.use_cases.users import (
    CreateUserUseCase,
    GetUserUseCase,
    AuthenticateUserUseCase,
)

# Use Cases - Vehicles
from src.application.use_cases.vehicles import (
    CreateCarUseCase,
    GetCarUseCase,
    UpdateCarUseCase,
    DeleteCarUseCase,
    SearchCarsUseCase,
    CreateMotorcycleUseCase,
    GetMotorcycleUseCase,
    UpdateMotorcycleUseCase,
    DeleteMotorcycleUseCase,
    SearchMotorcyclesUseCase,
)

# Use Cases - Messages
from src.application.use_cases.messages import (
    CreateMessageUseCase,
    GetMessageByIdUseCase,
    UpdateMessageUseCase,
    DeleteMessageUseCase,
    ListMessagesUseCase,
    AssignMessageUseCase,
    UpdateMessageStatusUseCase,
    GetMessagesStatisticsUseCase,
)

# Use Cases - Sales
from src.application.use_cases.sales import (
    CreateSaleUseCase,
    GetSaleByIdUseCase,
    UpdateSaleUseCase,
    DeleteSaleUseCase,
    ListSalesUseCase,
    UpdateSaleStatusUseCase,
    GetSalesStatisticsUseCase,
)

# Use Cases - Employees
from src.application.use_cases.employees import (
    CreateEmployeeUseCase,
    GetEmployeeByIdUseCase,
    UpdateEmployeeUseCase,
    DeleteEmployeeUseCase,
    ListEmployeesUseCase,
    PromoteEmployeeUseCase,
    UpdateEmployeeStatusUseCase,
)

# Use Cases - Clients
from src.application.use_cases.clients import (
    CreateClientUseCase,
    GetClientByIdUseCase,
    GetClientByCpfUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase,
    ListClientsUseCase,
    UpdateClientStatusUseCase,
)

# Controllers
from src.adapters.rest.controllers.sale_controller import SaleController
from src.adapters.rest.controllers.employee_controller import EmployeeController
from src.adapters.rest.controllers.message_controller import MessageController
from src.adapters.rest.controllers.client_controller import ClientController
from src.adapters.rest.controllers.car_controller import CarController
from src.adapters.rest.controllers.motorcycle_controller import MotorcycleController
from src.adapters.rest.controllers.user_controller import UserController
from src.adapters.rest.controllers.blacklisted_token_controller import BlacklistedTokenController
from src.adapters.rest.controllers.vehicle_image_controller import VehicleImageController

# Presenters
from src.adapters.rest.presenters.sale_presenter import SalePresenter
from src.adapters.rest.presenters.employee_presenter import EmployeePresenter
from src.adapters.rest.presenters.message_presenter import MessagePresenter
from src.adapters.rest.presenters.client_presenter import ClientPresenter
from src.adapters.rest.presenters.car_presenter import CarPresenter
from src.adapters.rest.presenters.motorcycle_presenter import MotorcyclePresenter
from src.adapters.rest.presenters.user_presenter import UserPresenter

# Mock Repositories
from src.infrastructure.driven.mock_car_repository import MockCarRepository
from src.infrastructure.driven.mock_motorcycle_repository import MockMotorcycleRepository
from src.infrastructure.driven.mock_client_repository import MockClientRepository
from src.infrastructure.driven.mock_employee_repository import MockEmployeeRepository
from src.infrastructure.driven.mock_sale_repository import MockSaleRepository
from src.infrastructure.driven.mock_message_repository import MockMessageRepository
from src.infrastructure.driven.mock_user_repository import MockUserRepository

# Real Gateways (for when database is configured)
from src.adapters.persistence.gateways import (
    UserGateway,
    CarGateway,
    ClientGateway,
    MotorcycleGateway,
    EmployeeGateway,
    SaleGateway,
    MessageGateway
)


# Dependency Functions - Use Cases - Car (mock para desenvolvimento)

def get_create_car_use_case() -> CreateCarUseCase:
    """Factory para CreateCarUseCase - versão com banco de dados."""
    return CreateCarUseCase(get_car_gateway())


def get_get_car_use_case() -> GetCarUseCase:
    """Factory para GetCarUseCase - versão com banco de dados."""
    return GetCarUseCase(get_car_gateway())


def get_update_car_use_case() -> UpdateCarUseCase:
    """Factory para UpdateCarUseCase - versão com banco de dados."""
    return UpdateCarUseCase(get_car_gateway())


def get_delete_car_use_case() -> DeleteCarUseCase:
    """Factory para DeleteCarUseCase - versão com banco de dados."""
    return DeleteCarUseCase(get_car_gateway())


def get_search_cars_use_case() -> SearchCarsUseCase:
    """Factory para SearchCarsUseCase - versão com banco de dados."""
    return SearchCarsUseCase(get_car_gateway())


# Dependency Functions - Use Cases - Motorcycle (mock para desenvolvimento)

def get_create_motorcycle_use_case() -> CreateMotorcycleUseCase:
    """Factory para CreateMotorcycleUseCase - versão mock."""
    return CreateMotorcycleUseCase(get_mock_motorcycle_repository())


def get_get_motorcycle_use_case() -> GetMotorcycleUseCase:
    """Factory para GetMotorcycleUseCase - versão mock."""
    return GetMotorcycleUseCase(get_mock_motorcycle_repository())


def get_update_motorcycle_use_case() -> UpdateMotorcycleUseCase:
    """Factory para UpdateMotorcycleUseCase - versão mock."""
    return UpdateMotorcycleUseCase(get_mock_motorcycle_repository())


def get_delete_motorcycle_use_case() -> DeleteMotorcycleUseCase:
    """Factory para DeleteMotorcycleUseCase - versão mock."""
    return DeleteMotorcycleUseCase(get_mock_motorcycle_repository())


def get_search_motorcycles_use_case() -> SearchMotorcyclesUseCase:
    """Factory para SearchMotorcyclesUseCase - versão mock."""
    return SearchMotorcyclesUseCase(get_mock_motorcycle_repository())


# Dependency Functions - Use Cases - User (mock para desenvolvimento)

def get_create_user_use_case() -> CreateUserUseCase:
    """Factory para CreateUserUseCase - versão mock."""
    return CreateUserUseCase(get_mock_user_repository())


def get_get_user_use_case() -> GetUserUseCase:
    """Factory para GetUserUseCase - versão mock."""
    return GetUserUseCase(get_mock_user_repository())


def get_authenticate_user_use_case() -> AuthenticateUserUseCase:
    """Factory para AuthenticateUserUseCase - versão mock."""
    return AuthenticateUserUseCase(get_mock_user_repository())


# Dependency Functions - Use Cases - Client (com mock repository)

def get_create_client_use_case() -> CreateClientUseCase:
    """Factory para CreateClientUseCase - versão com mock."""
    return CreateClientUseCase(get_mock_client_repository())


def get_get_client_by_id_use_case() -> GetClientByIdUseCase:
    """Factory para GetClientByIdUseCase - versão com mock."""
    return GetClientByIdUseCase(get_mock_client_repository())


def get_get_client_by_cpf_use_case() -> GetClientByCpfUseCase:
    """Factory para GetClientByCpfUseCase - versão com mock."""
    return GetClientByCpfUseCase(get_mock_client_repository())


def get_update_client_use_case() -> UpdateClientUseCase:
    """Factory para UpdateClientUseCase - versão com mock."""
    return UpdateClientUseCase(get_mock_client_repository())


def get_delete_client_use_case() -> DeleteClientUseCase:
    """Factory para DeleteClientUseCase - versão com mock."""
    return DeleteClientUseCase(get_mock_client_repository())


def get_list_clients_use_case() -> ListClientsUseCase:
    """Factory para ListClientsUseCase - versão com mock."""
    return ListClientsUseCase(get_mock_client_repository())


def get_update_client_status_use_case() -> UpdateClientStatusUseCase:
    """Factory para UpdateClientStatusUseCase - versão com mock."""
    return UpdateClientStatusUseCase(get_mock_client_repository())


def get_create_sale_use_case() -> CreateSaleUseCase:
    """Factory para CreateSaleUseCase - versão com mock."""
    return CreateSaleUseCase(get_mock_sale_repository())


def get_get_sale_by_id_use_case() -> GetSaleByIdUseCase:
    """Factory para GetSaleByIdUseCase - versão com mock."""
    return GetSaleByIdUseCase(get_mock_sale_repository())


def get_update_sale_use_case() -> UpdateSaleUseCase:
    """Factory para UpdateSaleUseCase - versão com mock."""
    return UpdateSaleUseCase(get_mock_sale_repository())


def get_delete_sale_use_case() -> DeleteSaleUseCase:
    """Factory para DeleteSaleUseCase - versão com mock."""
    return DeleteSaleUseCase(get_mock_sale_repository())


def get_list_sales_use_case() -> ListSalesUseCase:
    """Factory para ListSalesUseCase - versão com mock."""
    return ListSalesUseCase(get_mock_sale_repository())


def get_update_sale_status_use_case() -> UpdateSaleStatusUseCase:
    """Factory para UpdateSaleStatusUseCase - versão com mock."""
    return UpdateSaleStatusUseCase(get_mock_sale_repository())


def get_get_sales_statistics_use_case() -> GetSalesStatisticsUseCase:
    """Factory para GetSalesStatisticsUseCase - versão com mock."""
    return GetSalesStatisticsUseCase(get_mock_sale_repository())


# Dependency Functions - Use Cases - Message (com mock repository)

def get_create_message_use_case() -> CreateMessageUseCase:
    """Factory para CreateMessageUseCase - versão com mock."""
    return CreateMessageUseCase(get_mock_message_repository())


def get_get_message_by_id_use_case() -> GetMessageByIdUseCase:
    """Factory para GetMessageByIdUseCase - versão com mock."""
    return GetMessageByIdUseCase(get_mock_message_repository())


def get_update_message_use_case() -> UpdateMessageUseCase:
    """Factory para UpdateMessageUseCase - versão com mock."""
    return UpdateMessageUseCase(get_mock_message_repository())


def get_delete_message_use_case() -> DeleteMessageUseCase:
    """Factory para DeleteMessageUseCase - versão com mock."""
    return DeleteMessageUseCase(get_mock_message_repository())


def get_list_messages_use_case() -> ListMessagesUseCase:
    """Factory para ListMessagesUseCase - versão com mock."""
    return ListMessagesUseCase(get_mock_message_repository())


def get_assign_message_use_case() -> AssignMessageUseCase:
    """Factory para AssignMessageUseCase - versão com mock."""
    return AssignMessageUseCase(get_mock_message_repository())


def get_update_message_status_use_case() -> UpdateMessageStatusUseCase:
    """Factory para UpdateMessageStatusUseCase - versão com mock."""
    return UpdateMessageStatusUseCase(get_mock_message_repository())


def get_get_messages_statistics_use_case() -> GetMessagesStatisticsUseCase:
    """Factory para GetMessagesStatisticsUseCase - versão com mock."""
    return GetMessagesStatisticsUseCase(get_mock_message_repository())


# Singleton mock repository for Employee (shared state during development)
# Singletons para mock repositories
_mock_car_repository = None
_mock_motorcycle_repository = None
_mock_client_repository = None
_mock_user_repository = None
_mock_employee_repository = None
_mock_sale_repository = None
_mock_message_repository = None


def get_mock_car_repository() -> MockCarRepository:
    """Factory para mock Car repository - versão singleton."""
    global _mock_car_repository
    if _mock_car_repository is None:
        _mock_car_repository = MockCarRepository()
    return _mock_car_repository


def get_mock_motorcycle_repository() -> MockMotorcycleRepository:
    """Factory para mock Motorcycle repository - versão singleton."""
    global _mock_motorcycle_repository
    if _mock_motorcycle_repository is None:
        _mock_motorcycle_repository = MockMotorcycleRepository()
    return _mock_motorcycle_repository


def get_mock_client_repository() -> MockClientRepository:
    """Factory para mock Client repository - versão singleton."""
    global _mock_client_repository
    if _mock_client_repository is None:
        _mock_client_repository = MockClientRepository()
    return _mock_client_repository


def get_mock_user_repository() -> MockUserRepository:
    """Factory para mock User repository - versão singleton."""
    global _mock_user_repository
    if _mock_user_repository is None:
        _mock_user_repository = MockUserRepository()
    return _mock_user_repository


def get_mock_employee_repository() -> MockEmployeeRepository:
    """Factory para mock Employee repository - versão singleton."""
    global _mock_employee_repository
    if _mock_employee_repository is None:
        _mock_employee_repository = MockEmployeeRepository()
    return _mock_employee_repository


def get_mock_sale_repository() -> MockSaleRepository:
    """Factory para mock Sale repository - versão singleton."""
    global _mock_sale_repository
    if _mock_sale_repository is None:
        _mock_sale_repository = MockSaleRepository()
    return _mock_sale_repository


def get_mock_message_repository() -> MockMessageRepository:
    """Factory para mock Message repository - versão singleton."""
    global _mock_message_repository
    if _mock_message_repository is None:
        _mock_message_repository = MockMessageRepository()
    return _mock_message_repository


# =============================================================================
# REAL DATABASE GATEWAYS - Uncomment and configure when database is ready
# =============================================================================
#
# To use real database persistence instead of mock repositories:
# 1. Configure your database connection in the infrastructure layer
# 2. Uncomment the gateway functions below
# 3. Replace the mock repository calls in the use case factories above
#
# Example: Instead of get_mock_car_repository(), use get_car_gateway()

def get_car_gateway() -> CarGateway:
    """Factory for CarGateway with database connection."""
    return CarGateway()

def get_client_gateway() -> ClientGateway:
    """Factory for ClientGateway with database connection."""
    return ClientGateway()

def get_motorcycle_gateway() -> MotorcycleGateway:
    """Factory for MotorcycleGateway with database connection."""
    return MotorcycleGateway()

def get_employee_gateway() -> EmployeeGateway:
    """Factory for EmployeeGateway with database connection."""
    return EmployeeGateway()

def get_user_gateway() -> UserGateway:
    """Factory for UserGateway with database connection."""
    return UserGateway()

def get_sale_gateway() -> SaleGateway:
    """Factory for SaleGateway with database connection."""
    return SaleGateway()

def get_message_gateway() -> MessageGateway:
    """Factory for MessageGateway with database connection."""
    return MessageGateway()
#
# def get_sale_gateway() -> SaleGateway:
#     """Factory for SaleGateway with database session."""
#     return SaleGateway(get_database_session())
#
# def get_message_gateway() -> MessageGateway:
#     """Factory for MessageGateway with database session."""
#     return MessageGateway(get_database_session())
#
# def get_user_gateway() -> UserGateway:
#     """Factory for UserGateway with database session."""
#     return UserGateway(get_database_session())
#
# =============================================================================


# Dependency Functions - Use Cases - Employee (com mock repository)

def get_create_employee_use_case() -> CreateEmployeeUseCase:
    """Factory para CreateEmployeeUseCase - versão com mock."""
    return CreateEmployeeUseCase(get_mock_employee_repository())


def get_get_employee_by_id_use_case() -> GetEmployeeByIdUseCase:
    """Factory para GetEmployeeByIdUseCase - versão com mock."""
    return GetEmployeeByIdUseCase(get_mock_employee_repository())


def get_update_employee_use_case() -> UpdateEmployeeUseCase:
    """Factory para UpdateEmployeeUseCase - versão com mock."""
    return UpdateEmployeeUseCase(get_mock_employee_repository())


def get_delete_employee_use_case() -> DeleteEmployeeUseCase:
    """Factory para DeleteEmployeeUseCase - versão com mock."""
    return DeleteEmployeeUseCase(get_mock_employee_repository())


def get_list_employees_use_case() -> ListEmployeesUseCase:
    """Factory para ListEmployeesUseCase - versão com mock."""
    return ListEmployeesUseCase(get_mock_employee_repository())


def get_promote_employee_use_case() -> PromoteEmployeeUseCase:
    """Factory para PromoteEmployeeUseCase - versão com mock."""
    return PromoteEmployeeUseCase(get_mock_employee_repository())


def get_update_employee_status_use_case() -> UpdateEmployeeStatusUseCase:
    """Factory para UpdateEmployeeStatusUseCase - versão com mock."""
    return UpdateEmployeeStatusUseCase(get_mock_employee_repository())


# Dependency Functions - Presenters

def get_sale_presenter() -> SalePresenter:
    """Factory para SalePresenter."""
    return SalePresenter()


def get_employee_presenter() -> EmployeePresenter:
    """Factory para EmployeePresenter."""
    return EmployeePresenter()


def get_message_presenter() -> MessagePresenter:
    """Factory para MessagePresenter."""
    return MessagePresenter()


def get_client_presenter() -> ClientPresenter:
    """Factory para ClientPresenter."""
    return ClientPresenter()


def get_car_presenter() -> CarPresenter:
    """Factory para CarPresenter."""
    return CarPresenter()


def get_motorcycle_presenter() -> MotorcyclePresenter:
    """Factory para MotorcyclePresenter."""
    return MotorcyclePresenter()


def get_user_presenter() -> UserPresenter:
    """Factory para UserPresenter."""
    return UserPresenter()


# Dependency Functions - Controllers

def get_sale_controller() -> SaleController:
    """Factory para SaleController."""
    return SaleController(
        create_sale_use_case=get_create_sale_use_case(),
        get_sale_by_id_use_case=get_get_sale_by_id_use_case(),
        update_sale_use_case=get_update_sale_use_case(),
        delete_sale_use_case=get_delete_sale_use_case(),
        list_sales_use_case=get_list_sales_use_case(),
        update_sale_status_use_case=get_update_sale_status_use_case(),
        get_sales_statistics_use_case=get_get_sales_statistics_use_case(),
        sale_presenter=get_sale_presenter()
    )


def get_employee_controller() -> EmployeeController:
    """Factory para EmployeeController."""
    return EmployeeController(
        create_employee_use_case=get_create_employee_use_case(),
        get_employee_by_id_use_case=get_get_employee_by_id_use_case(),
        update_employee_use_case=get_update_employee_use_case(),
        delete_employee_use_case=get_delete_employee_use_case(),
        list_employees_use_case=get_list_employees_use_case(),
        promote_employee_use_case=get_promote_employee_use_case(),
        update_employee_status_use_case=get_update_employee_status_use_case(),
        employee_presenter=get_employee_presenter()
    )


def get_message_controller() -> MessageController:
    """Factory para MessageController."""
    return MessageController(
        create_message_use_case=get_create_message_use_case(),
        get_message_by_id_use_case=get_get_message_by_id_use_case(),
        update_message_use_case=get_update_message_use_case(),
        delete_message_use_case=get_delete_message_use_case(),
        list_messages_use_case=get_list_messages_use_case(),
        assign_message_use_case=get_assign_message_use_case(),
        update_message_status_use_case=get_update_message_status_use_case(),
        get_messages_statistics_use_case=get_get_messages_statistics_use_case(),
        message_presenter=get_message_presenter()
    )


def get_client_controller() -> ClientController:
    """Factory para ClientController."""
    return ClientController(
        create_use_case=get_create_client_use_case(),
        get_by_id_use_case=get_get_client_by_id_use_case(),
        get_by_cpf_use_case=get_get_client_by_cpf_use_case(),
        update_use_case=get_update_client_use_case(),
        delete_use_case=get_delete_client_use_case(),
        list_use_case=get_list_clients_use_case(),
        update_status_use_case=get_update_client_status_use_case(),
        client_presenter=get_client_presenter()
    )


# ====== CAR DEPENDENCIES ======

def get_car_controller() -> CarController:
    """Factory para CarController."""
    return CarController(
        create_use_case=get_create_car_use_case(),
        get_use_case=get_get_car_use_case(),
        update_use_case=get_update_car_use_case(),
        delete_use_case=get_delete_car_use_case(),
        search_use_case=get_search_cars_use_case(),
        car_presenter=get_car_presenter()
    )


# ====== MOTORCYCLE DEPENDENCIES ======

def get_motorcycle_controller() -> MotorcycleController:
    """Factory para MotorcycleController."""
    return MotorcycleController(
        create_use_case=get_create_motorcycle_use_case(),
        get_use_case=get_get_motorcycle_use_case(),
        update_use_case=get_update_motorcycle_use_case(),
        delete_use_case=get_delete_motorcycle_use_case(),
        search_use_case=get_search_motorcycles_use_case(),
        motorcycle_presenter=get_motorcycle_presenter()
    )


# ====== USER DEPENDENCIES ======

def get_user_controller() -> UserController:
    """Factory para UserController."""
    return UserController(
        create_use_case=get_create_user_use_case(),
        get_use_case=get_get_user_use_case(),
        authenticate_use_case=get_authenticate_user_use_case(),
        user_presenter=get_user_presenter()
    )


# ====== BLACKLISTED TOKEN DEPENDENCIES ======

def get_blacklisted_token_controller() -> BlacklistedTokenController:
    """Factory para BlacklistedTokenController."""
    return BlacklistedTokenController()


# ====== VEHICLE IMAGE DEPENDENCIES ======

def get_vehicle_image_controller() -> VehicleImageController:
    """Factory para VehicleImageController."""
    return VehicleImageController()
