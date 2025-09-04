"""
Presenter para Client - Adapters Layer

Responsável por formatar e apresentar dados de clientes para a camada REST.
Aplicando o padrão Presenter e princípios da Clean Architecture.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela apresentação de dados de clientes
- OCP: Extensível para novos formatos sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para apresentação de clientes
- DIP: Não depende de detalhes de implementação
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal
from datetime import datetime, date

from src.domain.entities.client import Client
from src.application.dtos.client_dto import ClientResponseDto


class ClientPresenter:
    """
    Presenter para formatação de dados de clientes.
    
    Converte entidades de domínio e dados de aplicação
    em formatos adequados para apresentação REST.
    """
    
    def present_client(self, client: Client) -> Dict[str, Any]:
        """
        Apresenta uma entidade Client como dicionário.
        
        Args:
            client: Entidade Client do domínio
            
        Returns:
            Dict: Dados formatados para apresentação
        """
        return {
            "id": str(client.id),
            "name": client.name,
            "email": client.email,
            "cpf": client.cpf,
            "phone": client.phone,
            "birth_date": client.birth_date.isoformat() if client.birth_date else None,
            "address": client.address,
            "city": client.city,
            "state": client.state,
            "zip_code": client.zip_code,
            "is_active": client.is_active,
            "preferred_contact": client.preferred_contact,
            "notes": client.notes,
            "credit_score": float(client.credit_score) if client.credit_score else None,
            "income": float(client.income) if client.income else None,
            "created_at": client.created_at.isoformat() if client.created_at else None,
            "updated_at": client.updated_at.isoformat() if client.updated_at else None
        }
    
    def present_client_list(self, clients: List[Client]) -> List[Dict[str, Any]]:
        """
        Apresenta uma lista de clientes.
        
        Args:
            clients: Lista de entidades Client
            
        Returns:
            List[Dict]: Lista formatada para apresentação
        """
        return [self.present_client(client) for client in clients]
    
    def present_client_summary(self, client: Client) -> Dict[str, Any]:
        """
        Apresenta um resumo do cliente (dados básicos).
        
        Args:
            client: Entidade Client do domínio
            
        Returns:
            Dict: Dados resumidos formatados
        """
        return {
            "id": str(client.id),
            "name": client.name,
            "email": client.email,
            "cpf": client.cpf,
            "phone": client.phone,
            "city": client.city,
            "is_active": client.is_active
        }
    
    def present_client_summaries(self, clients: List[Client]) -> List[Dict[str, Any]]:
        """
        Apresenta uma lista de resumos de clientes.
        
        Args:
            clients: Lista de entidades Client
            
        Returns:
            List[Dict]: Lista de resumos formatados
        """
        return [self.present_client_summary(client) for client in clients]
    
    def present_client_statistics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apresenta estatísticas de clientes.
        
        Args:
            stats: Dicionário com estatísticas
            
        Returns:
            Dict: Estatísticas formatadas
        """
        result = {}
        
        for key, value in stats.items():
            if isinstance(value, Decimal):
                result[key] = float(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, date):
                result[key] = value.isoformat()
            else:
                result[key] = value
        
        return result
    
    def present_search_results(self, clients: List[Client], 
                             total: int, 
                             page: int, 
                             page_size: int) -> Dict[str, Any]:
        """
        Apresenta resultados de busca paginados.
        
        Args:
            clients: Lista de clientes encontrados
            total: Total de clientes que atendem aos critérios
            page: Página atual
            page_size: Tamanho da página
            
        Returns:
            Dict: Resultados formatados com metadados de paginação
        """
        return {
            "data": self.present_client_list(clients),
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size,
                "has_next": page * page_size < total,
                "has_previous": page > 1
            }
        }
    
    def present_client_dto(self, dto: ClientResponseDto) -> Dict[str, Any]:
        """
        Apresenta um DTO de resposta de cliente.
        
        Args:
            dto: DTO de resposta do cliente
            
        Returns:
            Dict: Dados formatados para apresentação
        """
        return {
            "id": str(dto.id),
            "name": dto.name,
            "email": dto.email,
            "cpf": dto.cpf,
            "phone": dto.phone,
            "birth_date": dto.birth_date.isoformat() if dto.birth_date else None,
            "address": dto.address,
            "city": dto.city,
            "state": dto.state,
            "zip_code": dto.zip_code,
            "is_active": dto.is_active,
            "preferred_contact": dto.preferred_contact,
            "notes": dto.notes,
            "credit_score": float(dto.credit_score) if dto.credit_score else None,
            "income": float(dto.income) if dto.income else None,
            "created_at": dto.created_at.isoformat() if dto.created_at else None,
            "updated_at": dto.updated_at.isoformat() if dto.updated_at else None
        }
    
    def present_error(self, error_message: str, error_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Apresenta uma mensagem de erro.
        
        Args:
            error_message: Mensagem de erro
            error_code: Código do erro (opcional)
            
        Returns:
            Dict: Erro formatado para apresentação
        """
        error_data = {
            "error": True,
            "message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if error_code:
            error_data["code"] = error_code
        
        return error_data
    
    def present_success_message(self, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Apresenta uma mensagem de sucesso.
        
        Args:
            message: Mensagem de sucesso
            data: Dados adicionais (opcional)
            
        Returns:
            Dict: Resposta de sucesso formatada
        """
        result = {
            "success": True,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if data is not None:
            result["data"] = data
        
        return result
