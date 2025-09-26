from typing import Optional
from src.domain.entities.car import Car
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.car_repository import CarRepository
from src.application.dtos.car_dto import CarResponseDto, MotorVehicleResponseDto
import logging

logger = logging.getLogger(__name__)


class UpdateCarStatusUseCase:
    """
    Caso de uso para atualização de status de carro.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de status de carros.
    """
    
    def __init__(self, car_repository: CarRepository):
        self._car_repository = car_repository
    
    async def execute(self, car_id: int, new_status: str) -> Optional[CarResponseDto]:
        """
        Executa o caso de uso de atualização de status de carro.
        
        Args:
            car_id: ID do carro a ser atualizado
            new_status: Novo status do carro
            
        Returns:
            Optional[CarResponseDto]: Dados do carro atualizado ou None se não encontrado
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Para outros erros
        """
        try:
            if car_id <= 0:
                raise ValueError("ID do carro deve ser um número positivo")
            
            # Validar se o status é válido
            if not MotorVehicle.is_valid_status(new_status):
                raise ValueError(f"Status inválido. Deve ser um de: {', '.join(MotorVehicle.VALID_STATUSES)}")
            
            # Buscar o carro existente
            existing_car = await self._car_repository.find_by_id(car_id)
            if not existing_car:
                return None
            
            # Atualizar o status do motor vehicle
            if existing_car.motor_vehicle:
                existing_car.motor_vehicle.status = new_status
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
            
            # Persistir as alterações
            result_car = await self._car_repository.update(existing_car)
            
            if not result_car:
                return None
            
            return self._car_to_response_dto(result_car)
            
        except ValueError as e:
            logger.error(f"Erro de validação ao atualizar status do carro: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao atualizar status do carro: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
    
    def _car_to_response_dto(self, car: Car) -> CarResponseDto:
        """
        Converte entidade Car para DTO de resposta.
        
        Args:
            car: Entidade Car
            
        Returns:
            CarResponseDto: DTO de resposta
        """
        motor_vehicle_dto = None
        if car.motor_vehicle:
            motor_vehicle_dto = MotorVehicleResponseDto(
                id=car.motor_vehicle.id,
                model=car.motor_vehicle.model,
                year=car.motor_vehicle.year,
                mileage=car.motor_vehicle.mileage,
                fuel_type=car.motor_vehicle.fuel_type,
                color=car.motor_vehicle.color,
                city=car.motor_vehicle.city,
                price=car.motor_vehicle.price,
                additional_description=car.motor_vehicle.additional_description,
                status=car.motor_vehicle.status,
                created_at=car.motor_vehicle.created_at,
                updated_at=car.motor_vehicle.updated_at
            )
        
        return CarResponseDto(
            id=car.id,
            motor_vehicle=motor_vehicle_dto,
            bodywork=car.bodywork,
            transmission=car.transmission,
            updated_at=car.updated_at
        )
