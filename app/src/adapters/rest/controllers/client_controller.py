"""
Controller REST para Client - Adapters Layer

Implementa os endpoints da API para gerenciamento de clientes.
Aplica padrões REST e Clean Architecture, delegando para use cases.

Aplicando princípios SOLID:
- SRP: Cada controller tem responsabilidade específica
- OCP: Extensível para novos endpoints sem modificar existentes
- LSP: Controllers podem ser substituídos sem afetar comportamento
- ISP: Interfaces específicas para cada operação
- DIP: Dependem de abstrações (use cases), não de implementações
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, Query

from src.application.dtos.client_dto import (
    ClientCreateDto,
    ClientUpdateDto,
    ClientResponseDto,
    ClientSearchDto,
    ClientStatusUpdateDto
)
from src.application.use_cases.clients import (
    CreateClientUseCase,
    GetClientByIdUseCase,
    GetClientByCpfUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase,
    ListClientsUseCase,
    UpdateClientStatusUseCase,
)


class ClientController:
    """
    Controller para operações de clientes.
    
    Centraliza todos os endpoints relacionados ao gerenciamento
    de clientes, aplicando validações e tratamento de erros.
    """
    
    def __init__(
        self,
        create_use_case: CreateClientUseCase,
        get_by_id_use_case: GetClientByIdUseCase,
        get_by_cpf_use_case: GetClientByCpfUseCase,
        update_use_case: UpdateClientUseCase,
        delete_use_case: DeleteClientUseCase,
        list_use_case: ListClientsUseCase,
        update_status_use_case: UpdateClientStatusUseCase
    ):
        self._create_use_case = create_use_case
        self._get_by_id_use_case = get_by_id_use_case
        self._get_by_cpf_use_case = get_by_cpf_use_case
        self._update_use_case = update_use_case
        self._delete_use_case = delete_use_case
        self._list_use_case = list_use_case
        self._update_status_use_case = update_status_use_case
    
    async def create_client(self, dto: ClientCreateDto) -> ClientResponseDto:
        """
        Cria um novo cliente.
        
        Args:
            dto: Dados do cliente
            
        Returns:
            Dados do cliente criado
        """
        try:
            return await self._create_use_case.execute(dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na criação do cliente"
            )
    
    async def get_client_by_id(self, client_id: UUID) -> ClientResponseDto:
        """
        Obtém um cliente por ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Dados do cliente
        """
        try:
            return await self._get_by_id_use_case.execute(client_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na obtenção do cliente"
            )
    
    async def get_client_by_cpf(self, cpf: str) -> ClientResponseDto:
        """
        Obtém um cliente por CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Dados do cliente
        """
        try:
            return await self._get_by_cpf_use_case.execute(cpf)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na obtenção do cliente"
            )
    
    async def update_client(
        self, 
        client_id: UUID, 
        dto: ClientUpdateDto
    ) -> ClientResponseDto:
        """
        Atualiza um cliente.
        
        Args:
            client_id: ID do cliente
            dto: Dados para atualização
            
        Returns:
            Dados do cliente atualizado
        """
        try:
            return await self._update_use_case.execute(client_id, dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na atualização do cliente"
            )
    
    async def delete_client(self, client_id: UUID) -> Dict[str, Any]:
        """
        Exclui um cliente.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Confirmação da exclusão
        """
        try:
            success = await self._delete_use_case.execute(client_id)
            
            if success:
                return {
                    "message": "Cliente excluído com sucesso",
                    "client_id": str(client_id)
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na exclusão do cliente"
            )
    
    async def list_clients(self, dto: ClientSearchDto) -> Dict[str, Any]:
        """
        Lista clientes com filtros.
        
        Args:
            dto: Critérios de busca
            
        Returns:
            Lista de clientes e metadados de paginação
        """
        try:
            clients, total = await self._list_use_case.execute(dto)
            
            return {
                "clients": clients,
                "pagination": {
                    "total": total,
                    "skip": dto.skip,
                    "limit": dto.limit,
                    "has_next": (dto.skip + dto.limit) < total,
                    "has_previous": dto.skip > 0
                }
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na listagem de clientes"
            )
    
    async def update_client_status(
        self, 
        client_id: UUID, 
        dto: ClientStatusUpdateDto
    ) -> ClientResponseDto:
        """
        Atualiza status de um cliente.
        
        Args:
            client_id: ID do cliente
            dto: Novo status
            
        Returns:
            Dados do cliente atualizado
        """
        try:
            return await self._update_status_use_case.execute(client_id, dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na atualização do status"
            )


def create_client_router(
    create_use_case: CreateClientUseCase,
    get_by_id_use_case: GetClientByIdUseCase,
    get_by_cpf_use_case: GetClientByCpfUseCase,
    update_use_case: UpdateClientUseCase,
    delete_use_case: DeleteClientUseCase,
    list_use_case: ListClientsUseCase,
    update_status_use_case: UpdateClientStatusUseCase
) -> APIRouter:
    """
    Factory para criar o router de clientes.
    
    Args:
        *_use_case: Injeção de dependência dos use cases
        
    Returns:
        Router configurado com todos os endpoints
    """
    
    router = APIRouter(prefix="/clients", tags=["Clients"])
    
    controller = ClientController(
        create_use_case=create_use_case,
        get_by_id_use_case=get_by_id_use_case,
        get_by_cpf_use_case=get_by_cpf_use_case,
        update_use_case=update_use_case,
        delete_use_case=delete_use_case,
        list_use_case=list_use_case,
        update_status_use_case=update_status_use_case
    )
    
    @router.post("/", 
                response_model=ClientResponseDto,
                status_code=status.HTTP_201_CREATED)
    async def create_client(dto: ClientCreateDto):
        """Cria um novo cliente."""
        return await controller.create_client(dto)
    
    @router.get("/{client_id}", response_model=ClientResponseDto)
    async def get_client_by_id(client_id: UUID):
        """Obtém um cliente por ID."""
        return await controller.get_client_by_id(client_id)
    
    @router.get("/cpf/{cpf}", response_model=ClientResponseDto)
    async def get_client_by_cpf(cpf: str):
        """Obtém um cliente por CPF."""
        return await controller.get_client_by_cpf(cpf)
    
    @router.put("/{client_id}", response_model=ClientResponseDto)
    async def update_client(client_id: UUID, dto: ClientUpdateDto):
        """Atualiza um cliente."""
        return await controller.update_client(client_id, dto)
    
    @router.delete("/{client_id}")
    async def delete_client(client_id: UUID):
        """Exclui um cliente."""
        return await controller.delete_client(client_id)
    
    @router.post("/search")
    async def list_clients(dto: ClientSearchDto):
        """Lista clientes com filtros."""
        return await controller.list_clients(dto)
    
    @router.patch("/{client_id}/status", response_model=ClientResponseDto)
    async def update_client_status(client_id: UUID, dto: ClientStatusUpdateDto):
        """Atualiza status de um cliente."""
        return await controller.update_client_status(client_id, dto)
    
    return router


# ==============================================
# PRESENTERS
# ==============================================

class ClientPresenter:
    """
    Presenter para formatação de respostas de clientes.
    
    Aplica formatações específicas para diferentes contextos
    de apresentação dos dados.
    """
    
    @staticmethod
    def format_client_response(client: ClientResponseDto) -> Dict[str, Any]:
        """
        Formata resposta de cliente com campos computados.
        
        Args:
            client: DTO do cliente
            
        Returns:
            Dados formatados para resposta
        """
        return {
            "id": str(client.id),
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "cpf": client.cpf,
            "birth_date": client.birth_date.isoformat() if client.birth_date else None,
            "address": {
                "street": client.address,
                "city": client.city,
                "state": client.state,
                "zip_code": client.zip_code,
                "full_address": client.full_address
            },
            "status": client.status,
            "notes": client.notes,
            "computed_fields": {
                "age": client.age,
                "formatted_cpf": client.formatted_cpf,
                "formatted_phone": client.formatted_phone,
                "formatted_zip_code": client.formatted_zip_code,
                "display_name": client.display_name,
                "is_vip": client.is_vip,
                "can_make_purchase": client.can_make_purchase
            },
            "timestamps": {
                "created_at": client.created_at.isoformat(),
                "updated_at": client.updated_at.isoformat()
            }
        }
    
    @staticmethod
    def format_client_list_response(clients: List[ClientResponseDto]) -> List[Dict[str, Any]]:
        """
        Formata lista de clientes para resposta.
        
        Args:
            clients: Lista de DTOs de clientes
            
        Returns:
            Lista formatada para resposta
        """
        return [
            ClientPresenter.format_client_response(client) 
            for client in clients
        ]
    
    @staticmethod
    def format_client_summary(client: ClientResponseDto) -> Dict[str, Any]:
        """
        Formata resumo de cliente (dados essenciais).
        
        Args:
            client: DTO do cliente
            
        Returns:
            Resumo formatado
        """
        return {
            "id": str(client.id),
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "cpf": client.formatted_cpf,
            "status": client.status,
            "display_name": client.display_name,
            "is_vip": client.is_vip,
            "city": client.city,
            "state": client.state
        }
