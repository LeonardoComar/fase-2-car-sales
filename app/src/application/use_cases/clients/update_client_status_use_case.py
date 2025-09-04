from uuid import UUID

from src.application.dtos.client_dto import ClientResponseDto
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import NotFoundError, BusinessRuleError, ValidationError


class UpdateClientStatusUseCase:
    """
    Use case para atualização de status de clientes.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de status de clientes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, client_id: UUID, new_status: str, reason: str = None) -> ClientResponseDto:
        """
        Executa a atualização de status de um cliente.
        
        Args:
            client_id: ID do cliente
            new_status: Novo status do cliente
            reason: Motivo da mudança de status (opcional)
            
        Returns:
            ClientResponseDto: Dados do cliente com status atualizado
            
        Raises:
            NotFoundError: Se o cliente não for encontrado
            ValidationError: Se o status for inválido
            BusinessRuleError: Se a mudança de status não for permitida
        """
        try:
            # Buscar cliente existente
            existing_client = await self.client_repository.find_by_id(client_id)
            if not existing_client:
                raise NotFoundError("Cliente", str(client_id))
            
            # Validar novo status
            self._validate_status(new_status)
            
            # Validar se a mudança de status é permitida
            await self._validate_status_change(existing_client, new_status)
            
            # Atualizar status
            existing_client.update_status(new_status)
            
            # Adicionar nota sobre mudança se fornecida
            if reason:
                self._add_status_change_note(existing_client, new_status, reason)
            
            # Salvar no repositório
            saved_client = await self.client_repository.save(existing_client)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_client)
            
        except NotFoundError:
            raise
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante atualização de status: {str(e)}")
    
    def _validate_status(self, status: str) -> None:
        """
        Valida se o status é válido.
        
        Args:
            status: Status a ser validado
            
        Raises:
            ValidationError: Se o status for inválido
        """
        valid_statuses = ["active", "inactive", "suspended", "blacklisted"]
        
        if status not in valid_statuses:
            raise ValidationError(
                f"Status '{status}' inválido. Status válidos: {', '.join(valid_statuses)}"
            )
    
    async def _validate_status_change(self, client: Client, new_status: str) -> None:
        """
        Valida se a mudança de status é permitida.
        
        Args:
            client: Cliente existente
            new_status: Novo status
            
        Raises:
            BusinessRuleError: Se a mudança não for permitida
        """
        current_status = client.status
        
        # Regra: Não permitir mudança desnecessária
        if current_status == new_status:
            raise BusinessRuleError(
                f"Cliente já possui status '{new_status}'",
                "status_unchanged"
            )
        
        # Regra: Cliente blacklisted não pode ser reativado facilmente
        if current_status == "blacklisted" and new_status == "active":
            raise BusinessRuleError(
                "Cliente na lista negra requer processo especial de reativação",
                "blacklisted_reactivation_restricted"
            )
        
        # Regra: Verificar se cliente tem transações pendentes antes de inativar
        if new_status in ["inactive", "suspended", "blacklisted"]:
            has_pending_transactions = await self.client_repository.has_pending_transactions(client.id)
            if has_pending_transactions:
                raise BusinessRuleError(
                    "Não é possível alterar status de cliente com transações pendentes",
                    "client_has_pending_transactions"
                )
        
        # Regra: Cliente suspenso por motivos específicos
        if new_status == "suspended":
            # Em um cenário real, poderia haver validações específicas
            # para suspensão (documentos pendentes, verificações, etc.)
            pass
    
    def _add_status_change_note(self, client: Client, new_status: str, reason: str) -> None:
        """
        Adiciona nota sobre mudança de status.
        
        Args:
            client: Cliente
            new_status: Novo status
            reason: Motivo da mudança
        """
        from datetime import datetime
        
        status_note = f"Status alterado para '{new_status}' em {datetime.now().strftime('%d/%m/%Y %H:%M')}. Motivo: {reason}"
        
        if client.notes:
            client.notes += f"\n{status_note}"
        else:
            client.notes = status_note
    
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
