from typing import Optional
from src.domain.ports.car_repository import CarRepository
from src.application.dtos.car_dto import CarResponseDto, MotorVehicleResponseDto
from src.domain.entities.car import Car
from src.domain.exceptions import NotFoundError
import logging

logger = logging.getLogger(__name__)


class GetCarUseCase:
    """
    Caso de uso para buscar carro por ID.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de carros por ID.
    """
    
    def __init__(self, car_repository: CarRepository):
        self._car_repository = car_repository
    
    async def execute(self, car_id: int) -> CarResponseDto:
        """
        Executa o caso de uso de busca de carro por ID.
        
        Args:
            car_id: ID do carro a ser buscado
            
        Returns:
            CarResponseDto: Dados do carro encontrado
            
        Raises:
            NotFoundError: Se o carro não for encontrado
            ValueError: Se car_id for inválido
            Exception: Para outros erros
        """
        try:
            if car_id <= 0:
                raise ValueError("ID do carro deve ser um número positivo")
            
            car = await self._car_repository.find_by_id(car_id)
            
            if not car:
                raise NotFoundError("Carro", str(car_id))
            
            return self._car_to_response_dto(car)
            
        except ValueError as e:
            logger.error(f"Erro de validação ao buscar carro: {str(e)}")
            raise e
        except NotFoundError as e:
            logger.error(f"Carro não encontrado: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao buscar carro: {str(e)}")
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
