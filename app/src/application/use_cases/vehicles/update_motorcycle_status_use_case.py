from typing import Optional
from src.domain.entities.motorcycle import Motorcycle
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.application.dtos.motorcycle_dto import MotorcycleResponseDto
import logging

logger = logging.getLogger(__name__)


class UpdateMotorcycleStatusUseCase:
    """
    Caso de uso para atualização de status de motorcycle.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de status de motorcycles.
    """
    
    def __init__(self, motorcycle_repository: MotorcycleRepository):
        self._motorcycle_repository = motorcycle_repository
    
    async def execute(self, motorcycle_id: int, new_status: str) -> Optional[MotorcycleResponseDto]:
        """
        Executa o caso de uso de atualização de status de motorcycle.
        
        Args:
            motorcycle_id: ID da motorcycle a ser atualizada
            new_status: Novo status da motorcycle
            
        Returns:
            Optional[MotorcycleResponseDto]: Dados da motorcycle atualizada ou None se não encontrada
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Para outros erros
        """
        try:
            if motorcycle_id <= 0:
                raise ValueError("ID da motorcycle deve ser um número positivo")
            
            # Validar se o status é válido
            if not MotorVehicle.is_valid_status(new_status):
                raise ValueError(f"Status inválido. Deve ser um de: {', '.join(MotorVehicle.VALID_STATUSES)}")
            
            # Buscar a motorcycle existente
            existing_motorcycle = await self._motorcycle_repository.find_by_id(motorcycle_id)
            if not existing_motorcycle:
                return None
            
            # Atualizar o status do motor vehicle
            if existing_motorcycle.motor_vehicle:
                existing_motorcycle.motor_vehicle.status = new_status
                existing_motorcycle.motor_vehicle.updated_at = existing_motorcycle.updated_at
            
            # Persistir as alterações
            result_motorcycle = await self._motorcycle_repository.update(existing_motorcycle)
            
            if not result_motorcycle:
                return None
            
            return self._motorcycle_to_response_dto(result_motorcycle)
            
        except ValueError as e:
            logger.error(f"Erro de validação ao atualizar status da motorcycle: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao atualizar status da motorcycle: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
    
    def _motorcycle_to_response_dto(self, motorcycle: Motorcycle) -> MotorcycleResponseDto:
        """
        Converte entidade Motorcycle para DTO de resposta.
        
        Args:
            motorcycle: Entidade Motorcycle
            
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
