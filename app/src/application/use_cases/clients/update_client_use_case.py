"""
Use Case para Atualização de Cliente - Application Layer

Responsável por atualizar clientes aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela atualização de clientes
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para atualização
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.client import Client
from src.domain.entities.address import Address
from src.domain.ports.client_repository import ClientRepository
from src.application.dtos.client_dto import UpdateClientDto, ClientResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class UpdateClientUseCase:
    """
    Use Case para atualização de clientes.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e atualização de clientes no sistema.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            client_repository: Repositório de clientes
        """
        self._client_repository = client_repository
    
    async def execute(self, client_id: int, client_data: UpdateClientDto) -> Optional[ClientResponseDto]:
        """
        Executa a atualização de um cliente.
        
        Args:
            client_id: ID do cliente a ser atualizado
            client_data: Dados para atualização do cliente
            
        Returns:
            Optional[ClientResponseDto]: Dados do cliente atualizado ou None se não encontrado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na atualização
        """
        try:
            if client_id <= 0:
                raise ValueError("ID do cliente deve ser maior que zero")
            
            # Buscar cliente existente
            existing_client = await self._client_repository.find_by_id(client_id)
            if not existing_client:
                return None
            
            # Criar entidade de endereço se dados forem fornecidos
            address = None
            if any([client_data.street, client_data.city, client_data.state, 
                   client_data.zip_code, client_data.country]):
                address = Address(
                    street=client_data.street or "",
                    city=client_data.city or "",
                    state=client_data.state or "",
                    zip_code=client_data.zip_code or "",
                    country=client_data.country or "Brasil"
                )
            
            # Criar cópia do cliente para atualização
            updated_client = Client(
                id=existing_client.id,
                name=existing_client.name,
                email=existing_client.email,
                phone=existing_client.phone,
                cpf=existing_client.cpf,
                address_id=existing_client.address_id,
                created_at=existing_client.created_at,
                updated_at=existing_client.updated_at
            )
            
            # Aplicar atualizações usando método de domínio
            updated_client.update_fields(
                name=client_data.name,
                email=client_data.email,
                phone=client_data.phone,
                cpf=client_data.cpf
            )
            
            # Persistir no repositório
            result_client = await self._client_repository.update(client_id, updated_client, address)
            
            if not result_client:
                return None
            
            # Buscar endereço atualizado
            updated_address = None
            if result_client.address_id:
                updated_address = await self._client_repository.get_address_by_id(result_client.address_id)
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(result_client, updated_address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao atualizar cliente: {str(e)}")
    
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
