"""
Presenter para Client - Adapters Layer

Responsável por formatar dados de clientes para apresentação.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela formatação de apresentação de clientes
- OCP: Extensível para novos formatos sem modificar existentes
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para apresentação
- DIP: Depende de abstrações dos DTOs
"""

from typing import Dict, Any, List, Optional
from src.application.dtos.client_dto import ClientResponseDto, ClientListDto


class ClientPresenter:
    """
    Presenter para formatação de dados de cliente.
    
    Responsável por transformar DTOs em formatos específicos para apresentação.
    """
    
    @staticmethod
    def present_client(client: ClientResponseDto) -> Dict[str, Any]:
        """
        Apresenta os dados de um cliente.
        
        Args:
            client: DTO de resposta do cliente
            
        Returns:
            dict: Dados formatados do cliente
        """
        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "cpf": client.cpf,
            "address": client.address.dict() if client.address else None,
            "created_at": client.created_at,
            "updated_at": client.updated_at
        }
    
    @staticmethod
    def present_client_list(clients: List[ClientListDto]) -> Dict[str, Any]:
        """
        Apresenta uma lista de clientes.
        
        Args:
            clients: Lista de DTOs de clientes
            
        Returns:
            dict: Lista formatada de clientes
        """
        return {
            "clients": [
                {
                    "id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "phone": client.phone,
                    "cpf": client.cpf,
                    "city": client.city
                }
                for client in clients
            ],
            "total": len(clients)
        }
    
    @staticmethod
    def present_success(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Apresenta uma resposta de sucesso.
        
        Args:
            message: Mensagem de sucesso
            data: Dados adicionais (opcional)
            
        Returns:
            dict: Resposta formatada
        """
        response = {
            "success": True,
            "message": message
        }
        
        if data:
            response["data"] = data
            
        return response
    
    @staticmethod
    def present_error(message: str, error_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Apresenta uma resposta de erro.
        
        Args:
            message: Mensagem de erro
            error_code: Código do erro (opcional)
            
        Returns:
            dict: Resposta formatada de erro
        """
        response = {
            "success": False,
            "message": message
        }
        
        if error_code:
            response["error_code"] = error_code
            
        return response
