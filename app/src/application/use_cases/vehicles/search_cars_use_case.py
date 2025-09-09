from typing import List
from src.domain.ports.car_repository import CarRepository
from src.application.dtos.car_dto import CarSearchDto, CarListResponseDto, CarSummaryDto
from src.domain.entities.car import Car
import logging

logger = logging.getLogger(__name__)


class SearchCarsUseCase:
    """
    Caso de uso para busca de carros com filtros.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca filtrada de carros.
    """
    
    def __init__(self, car_repository: CarRepository):
        self._car_repository = car_repository
    
    async def execute(self, search_params: CarSearchDto) -> CarListResponseDto:
        """
        Executa o caso de uso de busca de carros com filtros.
        
        Args:
            search_params: Parâmetros de busca
            
        Returns:
            CarListResponseDto: Lista de carros encontrados
            
        Raises:
            ValueError: Se parâmetros forem inválidos
            Exception: Para outros erros
        """
        try:
            # Validar parâmetros de busca
            if search_params.skip < 0:
                raise ValueError("Parâmetro 'skip' deve ser maior ou igual a zero")
            
            if search_params.limit <= 0 or search_params.limit > 1000:
                raise ValueError("Parâmetro 'limit' deve estar entre 1 e 1000")
            
            # Executar busca no repositório
            cars = await self._car_repository.search_cars(
                model=search_params.model,
                year=search_params.year,
                bodywork=search_params.bodywork,
                transmission=search_params.transmission,
                fuel_type=search_params.fuel_type,
                city=search_params.city,
                min_price=float(search_params.min_price) if search_params.min_price else None,
                max_price=float(search_params.max_price) if search_params.max_price else None,
                status=search_params.status,
                order_by_price=search_params.order_by_price,
                skip=search_params.skip,
                limit=search_params.limit
            )
            
            # Converter para DTOs de resumo
            car_summaries = [self._car_to_summary_dto(car) for car in cars]
            
            # Para simplificar, retornamos o número de carros encontrados como total
            # Em uma implementação real, você faria uma consulta separada para contar o total
            total = len(car_summaries)
            
            return CarListResponseDto(
                cars=car_summaries,
                total=total,
                skip=search_params.skip,
                limit=search_params.limit
            )
            
        except ValueError as e:
            logger.error(f"Erro de validação na busca de carros: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro na busca de carros: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
    
    def _car_to_summary_dto(self, car: Car) -> CarSummaryDto:
        """
        Converte entidade Car para DTO de resumo.
        
        Args:
            car: Entidade Car
            
        Returns:
            CarSummaryDto: DTO de resumo
        """
        return CarSummaryDto(
            id=car.id,
            model=car.motor_vehicle.model if car.motor_vehicle else "",
            year=car.motor_vehicle.year if car.motor_vehicle else "",
            bodywork=car.bodywork,
            transmission=car.transmission,
            price=car.motor_vehicle.price if car.motor_vehicle else 0,
            city=car.motor_vehicle.city if car.motor_vehicle else "",
            status=car.motor_vehicle.status if car.motor_vehicle else "",
            mileage=car.motor_vehicle.mileage if car.motor_vehicle else 0,
            fuel_type=car.motor_vehicle.fuel_type if car.motor_vehicle else "",
            color=car.motor_vehicle.color if car.motor_vehicle else ""
        )
