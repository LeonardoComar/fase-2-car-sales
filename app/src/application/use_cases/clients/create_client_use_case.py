from src.application.dtos.client_dto import ClientCreateDto, ClientResponseDto
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import ValidationError, BusinessRuleError, DuplicateError


class CreateClientUseCase:
    """
    Use case para criação de clientes.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela criação de clientes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, client_data: ClientCreateDto) -> ClientResponseDto:
        """
        Executa a criação de um novo cliente.
        
        Args:
            client_data: Dados do cliente a ser criado
            
        Returns:
            ClientResponseDto: Dados do cliente criado
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
            DuplicateError: Se já existir cliente com CPF ou email
        """
        try:
            # Validar se CPF já existe
            await self._validate_unique_cpf(client_data.cpf)
            
            # Validar se email já existe
            await self._validate_unique_email(client_data.email)
            
            # Criar a entidade de domínio
            client = Client.create_client(
                name=client_data.name,
                email=client_data.email,
                phone=client_data.phone,
                cpf=client_data.cpf,
                birth_date=client_data.birth_date,
                address=client_data.address,
                city=client_data.city,
                state=client_data.state,
                zip_code=client_data.zip_code,
                notes=client_data.notes
            )
            
            # Validações adicionais de negócio
            await self._validate_business_rules(client)
            
            # Salvar no repositório
            saved_client = await self.client_repository.save(client)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_client)
            
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except DuplicateError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante criação do cliente: {str(e)}")
    
    async def _validate_unique_cpf(self, cpf: str) -> None:
        """
        Valida se o CPF é único.
        
        Args:
            cpf: CPF a ser validado
            
        Raises:
            DuplicateError: Se CPF já existir
        """
        existing_client = await self.client_repository.find_by_cpf(cpf)
        if existing_client:
            raise DuplicateError("Cliente", "CPF", cpf)
    
    async def _validate_unique_email(self, email: str) -> None:
        """
        Valida se o email é único.
        
        Args:
            email: Email a ser validado
            
        Raises:
            DuplicateError: Se email já existir
        """
        existing_client = await self.client_repository.find_by_email(email)
        if existing_client:
            raise DuplicateError("Cliente", "email", email)
    
    async def _validate_business_rules(self, client: Client) -> None:
        """
        Valida regras de negócio específicas para criação.
        
        Args:
            client: Entidade de cliente a ser validada
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Verificar se há muitos clientes da mesma cidade (limite por região)
        clients_same_city = await self.client_repository.find_by_criteria(
            city=client.city,
            state=client.state,
            active_only=True,
            limit=1000
        )
        
        if len(clients_same_city) > 500:
            # Apenas um aviso para cidades com muitos clientes
            pass
        
        # Regra: Validar padrões regionais
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
