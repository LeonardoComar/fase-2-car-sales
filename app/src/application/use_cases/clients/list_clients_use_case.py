"""
Use Case para Listar Clientes - Application Layer

Responsável por listar clientes com filtros e paginação.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela listagem de clientes
- OCP: Extensível para novos filtros sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para listagem
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import List, Optional
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.application.dtos.client_dto import ClientListDto


class ListClientsUseCase:
    """
    Use Case para listagem de clientes com filtros.
    
    Coordena a busca de clientes aplicando filtros e paginação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            client_repository: Repositório de clientes
        """
        self._client_repository = client_repository
    
    async def execute(self, skip: int = 0, limit: int = 100, 
                     name: Optional[str] = None, cpf: Optional[str] = None) -> List[ClientListDto]:
        """
        Executa a listagem de clientes com filtros.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            name: Nome ou parte do nome para filtrar (opcional)
            cpf: CPF exato para buscar (opcional)
            
        Returns:
            List[ClientListDto]: Lista de clientes
            
        Raises:
            ValueError: Se parâmetros inválidos forem fornecidos
            Exception: Se houver erro na busca
        """
        try:
            # Validar parâmetros
            if skip < 0:
                raise ValueError("Skip deve ser maior ou igual a zero")
            if limit <= 0 or limit > 500:
                raise ValueError("Limit deve estar entre 1 e 500")
            
            # Validar que apenas um tipo de busca seja usado
            search_params = [name, cpf]
            provided_params = [param for param in search_params if param is not None]
            if len(provided_params) > 1:
                raise ValueError("Não é possível usar name e cpf simultaneamente")
            
            clients = []
            
            # Aplicar filtros específicos
            if cpf:
                # Busca por CPF exato
                client = await self._client_repository.find_by_cpf(cpf)
                if client:
                    clients = [client]
                
            elif name:
                # Busca por nome
                clients = await self._client_repository.find_by_name(name, skip, limit)
            else:
                # Busca geral
                clients = await self._client_repository.find_all(skip, limit)
            
            # Converter para DTOs de listagem
            list_dtos = []
            for client in clients:
                list_dto = await self._convert_to_list_dto(client)
                list_dtos.append(list_dto)
            
            return list_dtos
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao listar clientes: {str(e)}")
    
    async def _convert_to_list_dto(self, client: Client) -> ClientListDto:
        """
        Converte entidade Client para DTO de listagem.
        
        Args:
            client: Entidade do cliente
            
        Returns:
            ClientListDto: DTO de listagem
        """
        # Buscar endereço para obter cidade se disponível
        city = None
        if client.address_id:
            address = await self._client_repository.get_address_by_id(client.address_id)
            if address:
                city = address.city
        
        return ClientListDto(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            cpf=client.cpf,
            city=city
        )
