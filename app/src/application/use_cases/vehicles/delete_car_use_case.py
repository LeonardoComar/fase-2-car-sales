from src.domain.ports.car_repository import CarRepository
import logging

logger = logging.getLogger(__name__)


class DeleteCarUseCase:
    """
    Caso de uso para remoção de carro.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela remoção de carros.
    """
    
    def __init__(self, car_repository: CarRepository):
        self._car_repository = car_repository
    
    async def execute(self, car_id: int) -> bool:
        """
        Executa o caso de uso de remoção de carro.
        
        Args:
            car_id: ID do carro a ser removido
            
        Returns:
            bool: True se removido com sucesso, False se não encontrado
            
        Raises:
            ValueError: Se car_id for inválido
            Exception: Para outros erros
        """
        try:
            if car_id <= 0:
                raise ValueError("ID do carro deve ser um número positivo")
            
            # Verificar se o carro existe antes de tentar remover
            existing_car = await self._car_repository.find_by_id(car_id)
            if not existing_car:
                return False
            
            # Verificar se o carro pode ser removido (regras de negócio)
            if existing_car.motor_vehicle and existing_car.motor_vehicle.is_sold():
                raise ValueError("Não é possível remover um carro que já foi vendido")
            
            # Remover o carro
            result = await self._car_repository.delete(car_id)
            
            if result:
                logger.info(f"Carro removido com sucesso. ID: {car_id}")
            
            return result
            
        except ValueError as e:
            logger.error(f"Erro de validação ao remover carro: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao remover carro: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
