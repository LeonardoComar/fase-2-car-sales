from typing import Optional
from src.domain.entities.car import Car
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.car_repository import CarRepository
from src.application.dtos.car_dto import CarCreateDto, CarResponseDto, MotorVehicleResponseDto
import logging

logger = logging.getLogger(__name__)


class CreateCarUseCase:
    """
    Caso de uso para criação de carro.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela criação de carros.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende de abstrações (CarRepository) e não de implementações concretas.
    """
    
    def __init__(self, car_repository: CarRepository):
        self._car_repository = car_repository
    
    async def execute(self, car_create: CarCreateDto) -> CarResponseDto:
        """
        Executa o caso de uso de criação de carro.
        
        Args:
            car_create: DTO com dados para criação do carro
            
        Returns:
            CarResponseDto: Dados do carro criado
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Para outros erros
        """
        try:
            # Validar dados específicos do carro
            if not Car.is_valid_bodywork(car_create.bodywork):
                raise ValueError(f"Tipo de carroceria inválido. Deve ser um de: {', '.join(Car.VALID_BODYWORK_TYPES)}")
            
            if not Car.is_valid_transmission(car_create.transmission):
                raise ValueError(f"Tipo de transmissão inválido. Deve ser um de: {', '.join(Car.VALID_TRANSMISSION_TYPES)}")
            
            # Validar dados do veículo motor
            if not MotorVehicle.is_valid_fuel_type(car_create.fuel_type):
                raise ValueError(f"Tipo de combustível inválido. Deve ser um de: {', '.join(MotorVehicle.VALID_FUEL_TYPES)}")
            
            # Criar o carro completo usando o método de domínio
            car = Car.create_complete_car(
                model=car_create.model,
                year=car_create.year,
                mileage=car_create.mileage,
                fuel_type=car_create.fuel_type,
                color=car_create.color,
                city=car_create.city,
                price=car_create.price,
                bodywork=car_create.bodywork,
                transmission=car_create.transmission,
                additional_description=car_create.additional_description
            )
            
            # Persistir o carro
            created_car = await self._car_repository.save(car)
            
            # Converter para DTO de resposta
            return self._car_to_response_dto(created_car)
            
        except ValueError as e:
            logger.error(f"Erro de validação ao criar carro: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao criar carro: {str(e)}")
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
