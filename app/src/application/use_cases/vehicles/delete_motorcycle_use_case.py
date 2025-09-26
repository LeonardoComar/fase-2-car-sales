from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.domain.exceptions import NotFoundError, BusinessRuleError


class DeleteMotorcycleUseCase:
    """
    Use case para exclusão de motocicletas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela exclusão de motocicletas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração MotorcycleRepository, não da implementação.
    """
    
    def __init__(self, motorcycle_repository: MotorcycleRepository):
        self.motorcycle_repository = motorcycle_repository
    
    async def execute(self, motorcycle_id: int) -> None:
        """
        Executa a exclusão de uma motocicleta.
        
        Args:
            motorcycle_id: ID da motocicleta a ser excluída
            
        Raises:
            NotFoundError: Se a motocicleta não for encontrada
            BusinessRuleError: Se as regras de negócio não permitirem a exclusão
        """
        # Buscar a motocicleta existente
        existing_motorcycle = await self.motorcycle_repository.find_by_id(motorcycle_id)
        
        if not existing_motorcycle:
            raise NotFoundError("Motocicleta", str(motorcycle_id))
        
        # Validar regras de negócio para exclusão
        await self._validate_business_rules(existing_motorcycle)
        
        # Excluir do repositório
        await self.motorcycle_repository.delete(motorcycle_id)
    
    async def _validate_business_rules(self, motorcycle) -> None:
        """
        Valida regras de negócio para exclusão.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio impedir a exclusão
        """
        # Regra: Não permitir exclusão de motocicletas vendidas
        if motorcycle.motor_vehicle.status == "Vendido":
            raise BusinessRuleError(
                "Não é possível excluir motocicleta vendida. "
                "Motocicletas vendidas devem ser mantidas para histórico.",
                "cannot_delete_sold_motorcycle"
            )
        
        # Regra: Não permitir exclusão de motocicletas reservadas
        if motorcycle.motor_vehicle.status == "Reservado":
            raise BusinessRuleError(
                "Não é possível excluir motocicleta reservada. "
                "Cancele a reserva antes de excluir.",
                "cannot_delete_reserved_motorcycle"
            )
        
        # Regra: Validar se a motocicleta pode ser excluída
        if not self._can_be_deleted(motorcycle):
            raise BusinessRuleError(
                "Motocicleta não pode ser excluída no momento",
                "motorcycle_cannot_be_deleted"
            )
    
    def _can_be_deleted(self, motorcycle) -> bool:
        """
        Verifica se a motocicleta pode ser excluída.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Returns:
            bool: True se pode ser excluída
        """
        # Permitir exclusão apenas para status específicos
        deletable_statuses = ["Ativo", "Inativo", "Em Manutenção"]
        return motorcycle.motor_vehicle.status in deletable_statuses
