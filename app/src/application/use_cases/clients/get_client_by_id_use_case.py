from typing import Optional
from uuid import UUID

from src.application.dtos.client_dto import ClientResponseDto
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import NotFoundError


class GetClientByIdUseCase:
    """
    Use case para buscar cliente por ID.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de cliente por ID.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, client_id: UUID) -> ClientResponseDto:
        """
        Executa a busca de um cliente por ID.
        
        Args:
            client_id: ID do cliente a ser buscado
            
        Returns:
            ClientResponseDto: Dados do cliente encontrado
            
        Raises:
            NotFoundError: Se o cliente não for encontrado
        """
        try:
            # Buscar no repositório
            client = await self.client_repository.find_by_id(client_id)
            
            if not client:
                raise NotFoundError("Cliente", str(client_id))
            
            # Converter para DTO de resposta
            return self._to_response_dto(client)
            
        except NotFoundError:
            raise
        except Exception as e:
            raise NotFoundError("Cliente", str(client_id))
    
    def _to_response_dto(self, client: Client) -> ClientResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            client: Entidade de cliente
            
        Returns:
            ClientResponseDto: DTO de resposta
        """
        return ClientResponseDto(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            cpf=client.cpf,
            birth_date=client.birth_date,
            address=client.address,
            city=client.city,
            state=client.state,
            zip_code=client.zip_code,
            status=client.status,
            notes=client.notes,
            # Dados calculados
            age=client.get_age(),
            formatted_cpf=client.get_formatted_cpf(),
            formatted_phone=client.get_formatted_phone(),
            formatted_zip_code=client.get_formatted_zip_code(),
            full_address=client.get_full_address(),
            display_name=client.get_display_name(),
            is_vip=client.is_vip(),
            can_make_purchase=client.can_make_purchase(),
            # Auditoria
            created_at=client.created_at,
            updated_at=client.updated_at
        )
