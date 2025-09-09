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
        from datetime import datetime
        
        return MotorcycleResponseDto(
            id=motorcycle.id,
            # Dados do MotorVehicle
            model=motorcycle.motor_vehicle.model,
            year=motorcycle.motor_vehicle.year,
            price=float(motorcycle.motor_vehicle.price),
            mileage=motorcycle.motor_vehicle.mileage,
            fuel_type=motorcycle.motor_vehicle.fuel_type,
            color=motorcycle.motor_vehicle.color,
            city=motorcycle.motor_vehicle.city,
            additional_description=motorcycle.motor_vehicle.additional_description,
            status=motorcycle.motor_vehicle.status,
            # Dados específicos da Motorcycle
            starter=motorcycle.starter,
            fuel_system=motorcycle.fuel_system,
            engine_displacement=motorcycle.engine_displacement,
            cooling=motorcycle.cooling,
            style=motorcycle.style,
            engine_type=motorcycle.engine_type,
            gears=motorcycle.gears,
            front_rear_brake=motorcycle.front_rear_brake,
            # Dados calculados
            display_name=f"{motorcycle.motor_vehicle.model} ({motorcycle.motor_vehicle.year})",
            # Auditoria - usando valores padrão se None
            created_at=motorcycle.motor_vehicle.created_at or datetime.now(),
            updated_at=motorcycle.updated_at or motorcycle.motor_vehicle.updated_at or datetime.now()
        )
