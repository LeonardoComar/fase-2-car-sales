from typing import Optional

from src.application.dtos.client_dto import ClientResponseDto
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import NotFoundError, ValidationError


class GetClientByCpfUseCase:
    """
    Use case para buscar cliente por CPF.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de cliente por CPF.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, cpf: str) -> ClientResponseDto:
        """
        Executa a busca de um cliente por CPF.
        
        Args:
            cpf: CPF do cliente a ser buscado (pode estar formatado ou não)
            
        Returns:
            ClientResponseDto: Dados do cliente encontrado
            
        Raises:
            ValidationError: Se o CPF for inválido
            NotFoundError: Se o cliente não for encontrado
        """
        try:
            # Limpar e validar o CPF
            clean_cpf = self._clean_cpf(cpf)
            self._validate_cpf_format(clean_cpf)
            
            # Buscar no repositório
            client = await self.client_repository.find_by_cpf(clean_cpf)
            
            if not client:
                raise NotFoundError("Cliente", f"CPF {cpf}")
            
            # Converter para DTO de resposta
            return self._to_response_dto(client)
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro ao buscar cliente por CPF: {str(e)}")
    
    def _clean_cpf(self, cpf: str) -> str:
        """
        Remove formatação do CPF.
        
        Args:
            cpf: CPF com ou sem formatação
            
        Returns:
            str: CPF apenas com números
        """
        return ''.join(filter(str.isdigit, cpf))
    
    def _validate_cpf_format(self, cpf: str) -> None:
        """
        Valida se o CPF tem o formato correto.
        
        Args:
            cpf: CPF apenas com números
            
        Raises:
            ValidationError: Se o CPF não tiver 11 dígitos
        """
        if len(cpf) != 11:
            raise ValidationError("CPF deve conter exatamente 11 dígitos")
        
        if not cpf.isdigit():
            raise ValidationError("CPF deve conter apenas números")
    
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
