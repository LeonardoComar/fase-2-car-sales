"""
Use Case para Atualização de Status de Cliente - Application Layer

Responsável por atualizar status de clientes (funcionalidade futura).

Aplicando princípios SOLID:
- SRP: Responsável apenas pela atualização de status de clientes
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para atualização de status
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.client import Client
from src.domain.entities.address import Address
from src.domain.ports.client_repository import ClientRepository
from src.application.dtos.client_dto import ClientResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class UpdateClientStatusUseCase:
    """
    Use Case para atualização de status de clientes.
    
    Nota: Atualmente clientes não possuem campo status,
    mas mantido para compatibilidade com arquitetura.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            client_repository: Repositório de clientes
        """
        self._client_repository = client_repository
    
    async def execute(self, client_id: int, status: str) -> Optional[ClientResponseDto]:
        """
        Executa a atualização de status de um cliente.
        
        Args:
            client_id: ID do cliente
            status: Novo status (funcionalidade não implementada para clientes)
            
        Returns:
            Optional[ClientResponseDto]: Dados do cliente ou None se não encontrado
            
        Raises:
            NotImplementedError: Clientes não possuem campo status
        """
        # Funcionalidade não implementada para clientes
        # Mantido apenas para compatibilidade com estrutura
        raise NotImplementedError("Clientes não possuem campo status atualmente")
    
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
