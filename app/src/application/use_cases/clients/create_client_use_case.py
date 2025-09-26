"""
Use Case para Criação de Cliente - Application Layer

Responsável por coordenar a criação de clientes aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela criação de clientes
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para criação
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.client import Client
from src.domain.entities.address import Address
from src.domain.ports.client_repository import ClientRepository
from src.application.dtos.client_dto import CreateClientDto, ClientResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class CreateClientUseCase:
    """
    Use Case para criação de clientes.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e persistência de clientes no sistema.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            client_repository: Repositório de clientes
        """
        self._client_repository = client_repository
    
    async def execute(self, client_data: CreateClientDto) -> ClientResponseDto:
        """
        Executa a criação de um cliente.
        
        Args:
            client_data: Dados para criação do cliente
            
        Returns:
            ClientResponseDto: Dados do cliente criado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na criação
        """
        try:
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
            
            # Criar entidade de cliente
            client = Client.create_client(
                name=client_data.name,
                email=client_data.email,
                cpf=client_data.cpf,
                phone=client_data.phone
            )
            
            # Persistir no repositório
            created_client = await self._client_repository.create(client, address)
            
            # Buscar o endereço criado se houver address_id
            created_address = None
            if created_client.address_id:
                created_address = await self._client_repository.get_address_by_id(created_client.address_id)
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(created_client, created_address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao criar cliente: {str(e)}")
    
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
