from uuid import UUID

from src.application.dtos.client_dto import ClientUpdateDto, ClientResponseDto
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import ValidationError, BusinessRuleError, NotFoundError, DuplicateError


class UpdateClientUseCase:
    """
    Use case para atualização de clientes.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de clientes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, client_id: UUID, client_data: ClientUpdateDto) -> ClientResponseDto:
        """
        Executa a atualização de um cliente.
        
        Args:
            client_id: ID do cliente a ser atualizado
            client_data: Dados para atualização
            
        Returns:
            ClientResponseDto: Dados do cliente atualizado
            
        Raises:
            NotFoundError: Se o cliente não for encontrado
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
            DuplicateError: Se houver conflito com CPF ou email
        """
        try:
            # Buscar cliente existente
            existing_client = await self.client_repository.find_by_id(client_id)
            if not existing_client:
                raise NotFoundError("Cliente", str(client_id))
            
            # Validar mudanças de CPF e email
            await self._validate_unique_fields(existing_client, client_data)
            
            # Aplicar atualizações
            updated_client = self._apply_updates(existing_client, client_data)
            
            # Validações adicionais de negócio
            await self._validate_business_rules(updated_client)
            
            # Salvar no repositório
            saved_client = await self.client_repository.save(updated_client)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_client)
            
        except NotFoundError:
            raise
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except DuplicateError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante atualização do cliente: {str(e)}")
    
    async def _validate_unique_fields(self, existing_client: Client, client_data: ClientUpdateDto) -> None:
        """
        Valida se os campos únicos não conflitam com outros clientes.
        
        Args:
            existing_client: Cliente existente
            client_data: Dados de atualização
            
        Raises:
            DuplicateError: Se houver conflito
        """
        # Validar CPF se foi alterado
        if client_data.cpf and client_data.cpf != existing_client.cpf:
            other_client = await self.client_repository.find_by_cpf(client_data.cpf)
            if other_client and other_client.id != existing_client.id:
                raise DuplicateError("Cliente", "CPF", client_data.cpf)
        
        # Validar email se foi alterado
        if client_data.email and client_data.email != existing_client.email:
            other_client = await self.client_repository.find_by_email(client_data.email)
            if other_client and other_client.id != existing_client.id:
                raise DuplicateError("Cliente", "email", client_data.email)
    
    def _apply_updates(self, existing_client: Client, client_data: ClientUpdateDto) -> Client:
        """
        Aplica as atualizações ao cliente existente.
        
        Args:
            existing_client: Cliente existente
            client_data: Dados de atualização
            
        Returns:
            Client: Cliente atualizado
        """
        # Preparar dados para atualização
        update_data = {}
        
        if client_data.name is not None:
            update_data['name'] = client_data.name
        
        if client_data.email is not None:
            update_data['email'] = client_data.email
        
        if client_data.phone is not None:
            update_data['phone'] = client_data.phone
        
        if client_data.cpf is not None:
            update_data['cpf'] = client_data.cpf
        
        if client_data.birth_date is not None:
            update_data['birth_date'] = client_data.birth_date
        
        if client_data.address is not None:
            update_data['address'] = client_data.address
        
        if client_data.city is not None:
            update_data['city'] = client_data.city
        
        if client_data.state is not None:
            update_data['state'] = client_data.state
        
        if client_data.zip_code is not None:
            update_data['zip_code'] = client_data.zip_code
        
        if client_data.status is not None:
            update_data['status'] = client_data.status
        
        if client_data.notes is not None:
            update_data['notes'] = client_data.notes
        
        # Atualizar cliente
        existing_client.update(**update_data)
        
        return existing_client
    
    async def _validate_business_rules(self, client: Client) -> None:
        """
        Valida regras de negócio específicas para atualização.
        
        Args:
            client: Entidade de cliente a ser validada
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Cliente inativo não pode ser atualizado para certas operações críticas
        if client.status == "inactive":
            # Apenas validação de exemplo - pode ser expandida conforme necessário
            pass
        
        # Regra: Validar padrões regionais se endereço foi alterado
        await self._validate_regional_patterns(client)
    
    async def _validate_regional_patterns(self, client: Client) -> None:
        """
        Valida padrões regionais específicos.
        
        Args:
            client: Entidade de cliente
            
        Raises:
            BusinessRuleError: Se houver inconsistência regional
        """
        # Regra: Validar CEP com estado
        if client.zip_code and client.state:
            cep_prefix = client.zip_code[:2]
            state_cep_map = {
                "SP": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
                "RJ": ["20", "21", "22", "23", "24", "25", "26", "27", "28"],
                "MG": ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39"],
                # Adicionar mais estados conforme necessário
            }
            
            if client.state in state_cep_map:
                valid_prefixes = state_cep_map[client.state]
                if cep_prefix not in valid_prefixes:
                    raise BusinessRuleError(
                        f"CEP {client.get_formatted_zip_code()} não é válido para o estado {client.state}",
                        "invalid_cep_state_combination"
                    )
    
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
