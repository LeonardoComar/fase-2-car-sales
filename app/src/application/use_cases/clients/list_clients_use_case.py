from typing import List, Optional

from src.application.dtos.client_dto import ClientSearchDto, ClientResponseDto
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import ValidationError


class ListClientsUseCase:
    """
    Use case para listagem de clientes com filtros e paginação.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela listagem e busca de clientes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, search_criteria: ClientSearchDto) -> List[ClientResponseDto]:
        """
        Executa a listagem de clientes com filtros.
        
        Args:
            search_criteria: Critérios de busca e filtros
            
        Returns:
            List[ClientResponseDto]: Lista de clientes encontrados
            
        Raises:
            ValidationError: Se os critérios de busca forem inválidos
        """
        try:
            # Validar critérios de busca
            self._validate_search_criteria(search_criteria)
            
            # Preparar parâmetros de busca
            search_params = self._prepare_search_params(search_criteria)
            
            # Buscar no repositório
            clients = await self.client_repository.find_by_criteria(**search_params)
            
            # Converter para DTOs de resposta
            return [self._to_response_dto(client) for client in clients]
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro durante busca de clientes: {str(e)}")
    
    def _validate_search_criteria(self, search_criteria: ClientSearchDto) -> None:
        """
        Valida os critérios de busca.
        
        Args:
            search_criteria: Critérios de busca
            
        Raises:
            ValidationError: Se os critérios forem inválidos
        """
        # Validar limite de resultados
        if search_criteria.limit and search_criteria.limit > 1000:
            raise ValidationError("Limite máximo de 1000 resultados por consulta")
        
        # Validar offset
        if search_criteria.offset and search_criteria.offset < 0:
            raise ValidationError("Offset não pode ser negativo")
        
        # Validar idade mínima e máxima
        if search_criteria.min_age and search_criteria.min_age < 0:
            raise ValidationError("Idade mínima não pode ser negativa")
        
        if search_criteria.max_age and search_criteria.max_age > 120:
            raise ValidationError("Idade máxima não pode ser superior a 120 anos")
        
        if (search_criteria.min_age and search_criteria.max_age and 
            search_criteria.min_age > search_criteria.max_age):
            raise ValidationError("Idade mínima não pode ser maior que idade máxima")
    
    def _prepare_search_params(self, search_criteria: ClientSearchDto) -> dict:
        """
        Prepara os parâmetros para busca no repositório.
        
        Args:
            search_criteria: Critérios de busca
            
        Returns:
            dict: Parâmetros preparados para o repositório
        """
        params = {}
        
        # Filtros de texto
        if search_criteria.name:
            params['name'] = search_criteria.name
        
        if search_criteria.email:
            params['email'] = search_criteria.email
        
        if search_criteria.phone:
            params['phone'] = search_criteria.phone
        
        if search_criteria.cpf:
            params['cpf'] = self._clean_cpf(search_criteria.cpf)
        
        # Filtros de localização
        if search_criteria.city:
            params['city'] = search_criteria.city
        
        if search_criteria.state:
            params['state'] = search_criteria.state
        
        if search_criteria.zip_code:
            params['zip_code'] = self._clean_zip_code(search_criteria.zip_code)
        
        # Filtros de status
        if search_criteria.status:
            params['status'] = search_criteria.status
        
        if search_criteria.active_only is not None:
            params['active_only'] = search_criteria.active_only
        
        # Filtros de idade
        if search_criteria.min_age is not None:
            params['min_age'] = search_criteria.min_age
        
        if search_criteria.max_age is not None:
            params['max_age'] = search_criteria.max_age
        
        # Filtros especiais
        if search_criteria.vip_only is not None:
            params['vip_only'] = search_criteria.vip_only
        
        # Paginação
        if search_criteria.limit is not None:
            params['limit'] = search_criteria.limit
        
        if search_criteria.offset is not None:
            params['offset'] = search_criteria.offset
        
        # Ordenação
        if search_criteria.order_by:
            params['order_by'] = search_criteria.order_by
        
        if search_criteria.order_direction:
            params['order_direction'] = search_criteria.order_direction
        
        return params
    
    def _clean_cpf(self, cpf: str) -> str:
        """
        Remove formatação do CPF.
        
        Args:
            cpf: CPF com ou sem formatação
            
        Returns:
            str: CPF apenas com números
        """
        return ''.join(filter(str.isdigit, cpf))
    
    def _clean_zip_code(self, zip_code: str) -> str:
        """
        Remove formatação do CEP.
        
        Args:
            zip_code: CEP com ou sem formatação
            
        Returns:
            str: CEP apenas com números
        """
        return ''.join(filter(str.isdigit, zip_code))
    
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
