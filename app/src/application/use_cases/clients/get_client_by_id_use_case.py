"""
Use Case para Obter Cliente - Application Layer

Responsável por buscar clientes por ID aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela busca de clientes
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para busca
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.client import Client
from src.domain.entities.address import Address
from src.domain.ports.client_repository import ClientRepository
from src.application.dtos.client_dto import ClientResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class GetClientByIdUseCase:
    """
    Use Case para busca de clientes por ID.
    
    Coordena a busca e conversão de dados de clientes.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            client_repository: Repositório de clientes
        """
        self._client_repository = client_repository
    
    async def execute(self, client_id: int) -> Optional[ClientResponseDto]:
        """
        Executa a busca de um cliente por ID.
        
        Args:
            client_id: ID do cliente a ser buscado
            
        Returns:
            Optional[ClientResponseDto]: Dados do cliente ou None se não encontrado
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na busca
        """
        try:
            if client_id <= 0:
                raise ValueError("ID do cliente deve ser maior que zero")
            
            # Buscar cliente no repositório
            client = await self._client_repository.find_by_id(client_id)
            
            if not client:
                return None
            
            # Buscar endereço se cliente tiver address_id
            address = None
            if client.address_id:
                address = await self._client_repository.get_address_by_id(client.address_id)
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(client, address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar cliente: {str(e)}")
    
    def _convert_to_response_dto(self, client: Client, address: Optional[Address] = None) -> ClientResponseDto:
        """
        Converte entidade Client para DTO de resposta.
        
        Args:
            client: Entidade do cliente
            address: Entidade do endereço (opcional)
            
        Returns:
            ClientResponseDto: DTO de resposta
        """
        address_dto = None
        if address and address.id is not None:
            address_dto = AddressResponseDto(
                id=address.id,
                street=address.street,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code,
                country=address.country,
                created_at=address.created_at.isoformat() if address.created_at else None,
                updated_at=address.updated_at.isoformat() if address.updated_at else None,
                full_address=address.get_full_address()
            )
        
        return ClientResponseDto(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            cpf=client.cpf,
            address=address_dto,
            created_at=client.created_at.isoformat() if client.created_at else None,
            updated_at=client.updated_at.isoformat() if client.updated_at else None
        )
