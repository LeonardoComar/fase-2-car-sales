from typing import Optional
from src.application.dtos.motorcycle_dto import MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.domain.exceptions import NotFoundError


class GetMotorcycleUseCase:
    """
    Use case para buscar motocicleta por ID.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de motocicleta por ID.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração MotorcycleRepository, não da implementação.
    """
    
    def __init__(self, motorcycle_repository: MotorcycleRepository):
        self.motorcycle_repository = motorcycle_repository
    
    async def execute(self, motorcycle_id: int) -> MotorcycleResponseDto:
        """
        Executa a busca de uma motocicleta por ID.
        
        Args:
            motorcycle_id: ID da motocicleta a ser buscada
            
        Returns:
            MotorcycleResponseDto: Dados da motocicleta encontrada
            
        Raises:
            NotFoundError: Se a motocicleta não for encontrada
        """
        # Buscar a motocicleta no repositório
        motorcycle = await self.motorcycle_repository.find_by_id(motorcycle_id)
        
        if not motorcycle:
            raise NotFoundError("Motocicleta", str(motorcycle_id))
        
        # Converter para DTO de resposta
        return self._to_response_dto(motorcycle)
    
    def _to_response_dto(self, motorcycle: Motorcycle) -> MotorcycleResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Returns:
            MotorcycleResponseDto: DTO de resposta
        """
        return MotorcycleResponseDto(
            id=motorcycle.id,
            # Dados do MotorVehicle
            brand=motorcycle.motor_vehicle.brand,
            model=motorcycle.motor_vehicle.model,
            year=motorcycle.motor_vehicle.year,
            price=motorcycle.motor_vehicle.price,
            mileage=motorcycle.motor_vehicle.mileage,
            fuel_type=motorcycle.motor_vehicle.fuel_type,
            engine_power=motorcycle.motor_vehicle.engine_power,
            color=motorcycle.motor_vehicle.color,
            status=motorcycle.motor_vehicle.status,
            description=motorcycle.motor_vehicle.description,
            # Dados específicos da Motorcycle
            motorcycle_type=motorcycle.motorcycle_type,
            cylinder_capacity=motorcycle.cylinder_capacity,
            has_abs=motorcycle.has_abs,
            has_traction_control=motorcycle.has_traction_control,
            seat_height=motorcycle.seat_height,
            dry_weight=motorcycle.dry_weight,
            fuel_capacity=motorcycle.fuel_capacity,
            # Dados calculados
            is_high_performance=motorcycle.is_high_performance(),
            power_to_weight_ratio=motorcycle.get_power_to_weight_ratio(),
            display_name=motorcycle.get_display_name(),
            # Auditoria
            created_at=motorcycle.created_at,
            updated_at=motorcycle.updated_at
        )
