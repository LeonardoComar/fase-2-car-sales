"""
Configuração do módulo Client - Startup Configuration

Configura dependências e injeção de dependência para o módulo Client.
Responsável por conectar todas as camadas do módulo seguindo Clean Architecture.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela configuração do módulo Client
- OCP: Facilita extensão sem modificação
- DIP: Gerencia inversão de dependências
"""

from typing import Dict, Any
from functools import lru_cache

# Use Cases
from src.application.use_cases.clients import (
    CreateClientUseCase,
    GetClientByIdUseCase,
    GetClientByCpfUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase,
    ListClientsUseCase,
    UpdateClientStatusUseCase,
)

# Repository
from src.domain.ports.client_repository import ClientRepository
from src.infrastructure.driven.mock_client_repository import MockClientRepository

# Controller
from src.adapters.rest.controllers.client_controller import ClientController


class ClientModule:
    """
    Configuração do módulo Client.
    
    Responsável por configurar e fornecer todas as dependências
    necessárias para o funcionamento do módulo Client.
    """
    
    def __init__(self):
        """Inicializa a configuração do módulo."""
        self._repository = None
        self._use_cases = {}
        self._controller = None
    
    @lru_cache(maxsize=1)
    def get_repository(self) -> ClientRepository:
        """
        Obtém instância do repositório de clientes.
        
        Returns:
            Instância do repositório configurado
        """
        if self._repository is None:
            self._repository = MockClientRepository()
        
        return self._repository
    
    def get_use_cases(self) -> Dict[str, Any]:
        """
        Obtém todas as instâncias dos use cases.
        
        Returns:
            Dicionário com todos os use cases
        """
        if not self._use_cases:
            repository = self.get_repository()
            
            self._use_cases = {
                'create_client': CreateClientUseCase(repository),
                'get_client_by_id': GetClientByIdUseCase(repository),
                'get_client_by_cpf': GetClientByCpfUseCase(repository),
                'update_client': UpdateClientUseCase(repository),
                'delete_client': DeleteClientUseCase(repository),
                'list_clients': ListClientsUseCase(repository),
                'update_client_status': UpdateClientStatusUseCase(repository)
            }
        
        return self._use_cases
    
    def get_controller(self) -> ClientController:
        """
        Obtém instância do controller de clientes.
        
        Returns:
            Instância do controller configurado
        """
        if self._controller is None:
            use_cases = self.get_use_cases()
            self._controller = ClientController(use_cases)
        
        return self._controller


# Instância global do módulo
client_module = ClientModule()


def get_client_repository() -> ClientRepository:
    """
    Factory function para obter repositório de clientes.
    
    Returns:
        Instância do repositório
    """
    return client_module.get_repository()


def get_create_client_use_case() -> CreateClientUseCase:
    """
    Factory function para obter use case de criação.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['create_client']


def get_get_client_by_id_use_case() -> GetClientByIdUseCase:
    """
    Factory function para obter use case de busca por ID.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['get_client_by_id']


def get_get_client_by_cpf_use_case() -> GetClientByCpfUseCase:
    """
    Factory function para obter use case de busca por CPF.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['get_client_by_cpf']


def get_update_client_use_case() -> UpdateClientUseCase:
    """
    Factory function para obter use case de atualização.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['update_client']


def get_delete_client_use_case() -> DeleteClientUseCase:
    """
    Factory function para obter use case de exclusão.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['delete_client']


def get_list_clients_use_case() -> ListClientsUseCase:
    """
    Factory function para obter use case de listagem.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['list_clients']


def get_update_client_status_use_case() -> UpdateClientStatusUseCase:
    """
    Factory function para obter use case de atualização de status.
    
    Returns:
        Instância do use case
    """
    return client_module.get_use_cases()['update_client_status']


def get_client_controller() -> ClientController:
    """
    Factory function para obter controller de clientes.
    
    Returns:
        Instância do controller
    """
    return client_module.get_controller()


def configure_client_dependencies() -> Dict[str, Any]:
    """
    Configura todas as dependências do módulo Client.
    
    Returns:
        Dicionário com todas as dependências configuradas
    """
    return {
        'repository': get_client_repository(),
        'use_cases': client_module.get_use_cases(),
        'controller': get_client_controller()
    }
