from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.domain.entities.car import Car
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.car_repository import CarRepository
from src.infrastructure.database.models.car_model import CarModel, MotorVehicleModel
from src.infrastructure.database.connection import get_db_session
import logging

logger = logging.getLogger(__name__)


class CarGateway(CarRepository):
    """
    Gateway de persistência para carros.
    
    Implementa a interface CarRepository definida no domínio.
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a abstração definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência de dados de carros.
    """
    
    def __init__(self):
        pass
    
    async def save(self, car: Car) -> Car:
        """
        Salva um carro no banco de dados.
        
        Args:
            car: Entidade Car do domínio
            
        Returns:
            Car: Entidade Car salva com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        try:
            with get_db_session() as session:
                # Primeiro salva o motor_vehicle
                motor_vehicle_model = MotorVehicleModel(
                    model=car.motor_vehicle.model,
                    year=car.motor_vehicle.year,
                    price=float(car.motor_vehicle.price),
                    mileage=car.motor_vehicle.mileage,
                    fuel_type=car.motor_vehicle.fuel_type,
                    color=car.motor_vehicle.color,
                    city=car.motor_vehicle.city,
                    status=car.motor_vehicle.status,
                    additional_description=car.motor_vehicle.additional_description
                )
                
                session.add(motor_vehicle_model)
                session.flush()  # Para obter o ID
                
                # Agora salva o carro
                car_model = CarModel(
                    vehicle_id=motor_vehicle_model.id,
                    bodywork=car.bodywork,
                    transmission=car.transmission
                )
                
                session.add(car_model)
                session.commit()
                session.refresh(car_model)
                session.refresh(motor_vehicle_model)
                
                # Converter modelo de banco para entidade do domínio
                saved_car = self._model_to_entity(car_model, motor_vehicle_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(car_model)
                session.expunge(motor_vehicle_model)
                
                logger.info(f"Carro criado com sucesso. ID: {saved_car.id}")
                return saved_car
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao salvar carro: {str(e)}")
            raise Exception(f"Erro ao salvar carro: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao salvar carro: {str(e)}")
            raise Exception(f"Erro inesperado ao salvar carro: {str(e)}")
    
    async def update(self, car: Car) -> Car:
        """
        Atualiza um carro existente.
        
        Args:
            car: Entidade Car do domínio com dados atualizados
            
        Returns:
            Car: Entidade Car atualizada
        """
        try:
            with get_db_session() as session:
                # Buscar o carro existente
                car_model = session.query(CarModel).filter(CarModel.vehicle_id == car.id).first()
                if not car_model:
                    raise Exception(f"Carro com ID {car.id} não encontrado")
                
                # Buscar o motor_vehicle
                motor_vehicle_model = session.query(MotorVehicleModel).filter(
                    MotorVehicleModel.id == car_model.vehicle_id
                ).first()
                
                # Atualizar motor_vehicle
                motor_vehicle_model.model = car.motor_vehicle.model
                motor_vehicle_model.year = car.motor_vehicle.year
                motor_vehicle_model.price = float(car.motor_vehicle.price)
                motor_vehicle_model.mileage = car.motor_vehicle.mileage
                motor_vehicle_model.fuel_type = car.motor_vehicle.fuel_type
                motor_vehicle_model.color = car.motor_vehicle.color
                motor_vehicle_model.city = car.motor_vehicle.city
                motor_vehicle_model.status = car.motor_vehicle.status
                motor_vehicle_model.additional_description = car.motor_vehicle.additional_description
                
                # Atualizar carro
                car_model.bodywork = car.bodywork
                car_model.transmission = car.transmission
                
                session.commit()
                session.refresh(car_model)
                session.refresh(motor_vehicle_model)
                
                # Converter modelo de banco para entidade do domínio
                updated_car = self._model_to_entity(car_model, motor_vehicle_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(car_model)
                session.expunge(motor_vehicle_model)
                
                logger.info(f"Carro atualizado com sucesso. ID: {updated_car.id}")
                return updated_car
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar carro: {str(e)}")
            raise Exception(f"Erro ao atualizar carro: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar carro: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar carro: {str(e)}")
    
    async def find_by_id(self, car_id: int) -> Optional[Car]:
        """
        Busca um carro pelo ID.
        
        Args:
            car_id: ID do carro
            
        Returns:
            Optional[Car]: Entidade Car encontrada ou None
        """
        try:
            with get_db_session() as session:
                car_model = session.query(CarModel).filter(CarModel.vehicle_id == car_id).first()
                
                if car_model:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == car_model.vehicle_id
                    ).first()
                    
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(car_model)
                    session.expunge(motor_vehicle_model)
                    
                    return self._model_to_entity(car_model, motor_vehicle_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar carro por ID {car_id}: {str(e)}")
            raise Exception(f"Erro ao buscar carro: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar carro por ID {car_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar carro: {str(e)}")
    
    async def find_all(self) -> List[Car]:
        """
        Busca todos os carros.
        
        Returns:
            List[Car]: Lista de entidades Car
        """
        try:
            with get_db_session() as session:
                car_models = session.query(CarModel).join(MotorVehicleModel).all()
                
                cars = []
                for car_model in car_models:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == car_model.vehicle_id
                    ).first()
                    
                    session.expunge(car_model)
                    session.expunge(motor_vehicle_model)
                    cars.append(self._model_to_entity(car_model, motor_vehicle_model))
                
                return cars
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todos os carros: {str(e)}")
            raise Exception(f"Erro ao buscar carros: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar todos os carros: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar carros: {str(e)}")
    
    async def delete(self, car_id: int) -> bool:
        """
        Remove um carro pelo ID.
        
        Args:
            car_id: ID do carro
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            with get_db_session() as session:
                car_model = session.query(CarModel).filter(CarModel.vehicle_id == car_id).first()
                
                if not car_model:
                    return False
                
                # Buscar e remover o motor_vehicle associado
                motor_vehicle_model = session.query(MotorVehicleModel).filter(
                    MotorVehicleModel.id == car_model.vehicle_id
                ).first()
                
                session.delete(car_model)
                if motor_vehicle_model:
                    session.delete(motor_vehicle_model)
                
                session.commit()
                
                logger.info(f"Carro removido com sucesso. ID: {car_id}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao remover carro {car_id}: {str(e)}")
            raise Exception(f"Erro ao remover carro: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao remover carro {car_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao remover carro: {str(e)}")
    
    async def search_cars(
        self,
        model: str = None,
        year: str = None,
        bodywork: str = None,
        transmission: str = None,
        fuel_type: str = None,
        city: str = None,
        min_price: float = None,
        max_price: float = None,
        status: str = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Car]:
        """
        Busca carros por critérios específicos.
        
        Args:
            model: Modelo do carro
            year: Ano do carro
            bodywork: Tipo de carroceria
            transmission: Tipo de transmissão
            fuel_type: Tipo de combustível
            city: Cidade
            min_price: Preço mínimo
            max_price: Preço máximo
            status: Status do veículo
            skip: Número de registros para pular
            limit: Limite de registros
            
        Returns:
            Lista de carros que correspondem aos critérios
        """
        try:
            with get_db_session() as session:
                # Usar o relacionamento definido no modelo
                query = session.query(CarModel)
                
                # Aplicar filtros
                if model:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.model.ilike(f"%{model}%"))
                if year:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.year == year)
                if bodywork:
                    query = query.filter(CarModel.bodywork.ilike(f"%{bodywork}%"))
                if transmission:
                    query = query.filter(CarModel.transmission.ilike(f"%{transmission}%"))
                if fuel_type:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.fuel_type.ilike(f"%{fuel_type}%"))
                if city:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.city.ilike(f"%{city}%"))
                if status:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.status.ilike(f"%{status}%"))
                if min_price:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.price >= min_price)
                if max_price:
                    query = query.join(MotorVehicleModel).filter(MotorVehicleModel.price <= max_price)
                
                # Aplicar paginação
                query = query.offset(skip).limit(limit)
                
                results = query.all()
                cars = []
                
                for car_model in results:
                    motor_vehicle_model = car_model.motor_vehicle
                    session.expunge(car_model)
                    session.expunge(motor_vehicle_model)
                    cars.append(self._model_to_entity(car_model, motor_vehicle_model))
                
                return cars
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar carros: {str(e)}")
            raise Exception(f"Erro ao buscar carros: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar carros: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar carros: {str(e)}")

    async def find_by_criteria(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        transmission: Optional[str] = None,
        bodywork: Optional[str] = None,
        status: Optional[str] = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Car]:
        """
        Busca carros por critérios específicos.
        """
        try:
            with get_db_session() as session:
                query = session.query(CarModel).join(MotorVehicleModel)
                
                # Aplicar filtros
                if brand:
                    query = query.filter(MotorVehicleModel.brand.ilike(f"%{brand}%"))
                if model:
                    query = query.filter(MotorVehicleModel.model.ilike(f"%{model}%"))
                if year_min:
                    query = query.filter(MotorVehicleModel.year >= str(year_min))
                if year_max:
                    query = query.filter(MotorVehicleModel.year <= str(year_max))
                if price_min:
                    query = query.filter(MotorVehicleModel.price >= price_min)
                if price_max:
                    query = query.filter(MotorVehicleModel.price <= price_max)
                if mileage_max:
                    query = query.filter(MotorVehicleModel.mileage <= mileage_max)
                if fuel_type:
                    query = query.filter(MotorVehicleModel.fuel_type.ilike(f"%{fuel_type}%"))
                if transmission:
                    query = query.filter(CarModel.transmission.ilike(f"%{transmission}%"))
                if bodywork:
                    query = query.filter(CarModel.bodywork.ilike(f"%{bodywork}%"))
                if status:
                    query = query.filter(MotorVehicleModel.status.ilike(f"%{status}%"))
                if available_only:
                    query = query.filter(MotorVehicleModel.status == "Ativo")
                
                # Aplicar paginação
                query = query.offset(skip).limit(limit)
                
                results = query.all()
                cars = []
                
                for car_model in results:
                    motor_vehicle_model = car_model.motor_vehicle
                    session.expunge(car_model)
                    session.expunge(motor_vehicle_model)
                    cars.append(self._model_to_entity(car_model, motor_vehicle_model))
                
                return cars
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar carros por critérios: {str(e)}")
            raise Exception(f"Erro ao buscar carros: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar carros por critérios: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar carros: {str(e)}")

    async def count_by_criteria(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        transmission: Optional[str] = None,
        bodywork: Optional[str] = None,
        status: Optional[str] = None,
        available_only: bool = False
    ) -> int:
        """
        Conta carros por critérios específicos.
        """
        try:
            with get_db_session() as session:
                query = session.query(CarModel).join(MotorVehicleModel)
                
                # Aplicar os mesmos filtros
                if brand:
                    query = query.filter(MotorVehicleModel.brand.ilike(f"%{brand}%"))
                if model:
                    query = query.filter(MotorVehicleModel.model.ilike(f"%{model}%"))
                if year_min:
                    query = query.filter(MotorVehicleModel.year >= str(year_min))
                if year_max:
                    query = query.filter(MotorVehicleModel.year <= str(year_max))
                if price_min:
                    query = query.filter(MotorVehicleModel.price >= price_min)
                if price_max:
                    query = query.filter(MotorVehicleModel.price <= price_max)
                if mileage_max:
                    query = query.filter(MotorVehicleModel.mileage <= mileage_max)
                if fuel_type:
                    query = query.filter(MotorVehicleModel.fuel_type.ilike(f"%{fuel_type}%"))
                if transmission:
                    query = query.filter(CarModel.transmission.ilike(f"%{transmission}%"))
                if bodywork:
                    query = query.filter(CarModel.bodywork.ilike(f"%{bodywork}%"))
                if status:
                    query = query.filter(MotorVehicleModel.status.ilike(f"%{status}%"))
                if available_only:
                    query = query.filter(MotorVehicleModel.status == "Ativo")
                
                return query.count()
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar carros por critérios: {str(e)}")
            raise Exception(f"Erro ao contar carros: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao contar carros por critérios: {str(e)}")
            raise Exception(f"Erro inesperado ao contar carros: {str(e)}")

    async def search(self, filters: Dict[str, Any], limit: int = 50, offset: int = 0) -> Tuple[List[Car], int]:
        """
        Busca carros com filtros.
        
        Args:
            filters: Dicionário com filtros
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            Tuple[List[Car], int]: Lista de carros e total de registros
        """
        try:
            with get_db_session() as session:
                query = session.query(CarModel).join(MotorVehicleModel)
                
                # Aplicar filtros
                if filters.get('brand'):
                    query = query.filter(MotorVehicleModel.brand.ilike(f"%{filters['brand']}%"))
                if filters.get('model'):
                    query = query.filter(MotorVehicleModel.model.ilike(f"%{filters['model']}%"))
                if filters.get('year_min'):
                    query = query.filter(MotorVehicleModel.year >= filters['year_min'])
                if filters.get('year_max'):
                    query = query.filter(MotorVehicleModel.year <= filters['year_max'])
                if filters.get('price_min'):
                    query = query.filter(MotorVehicleModel.price >= filters['price_min'])
                if filters.get('price_max'):
                    query = query.filter(MotorVehicleModel.price <= filters['price_max'])
                if filters.get('fuel_type'):
                    query = query.filter(MotorVehicleModel.fuel_type == filters['fuel_type'])
                if filters.get('bodywork'):
                    query = query.filter(CarModel.bodywork == filters['bodywork'])
                if filters.get('transmission'):
                    query = query.filter(CarModel.transmission == filters['transmission'])
                if filters.get('status'):
                    query = query.filter(MotorVehicleModel.status == filters['status'])
                
                # Contar total
                total = query.count()
                
                # Aplicar paginação
                car_models = query.offset(offset).limit(limit).all()
                
                cars = []
                for car_model in car_models:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == car_model.vehicle_id
                    ).first()
                    
                    session.expunge(car_model)
                    session.expunge(motor_vehicle_model)
                    cars.append(self._model_to_entity(car_model, motor_vehicle_model))
                
                return cars, total
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar carros com filtros: {str(e)}")
            raise Exception(f"Erro ao buscar carros: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar carros com filtros: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar carros: {str(e)}")
    
    def _model_to_entity(self, car_model: CarModel, motor_vehicle_model: MotorVehicleModel) -> Car:
        """
        Converte modelo de banco para entidade do domínio.
        
        Args:
            car_model: Modelo SQLAlchemy do carro
            motor_vehicle_model: Modelo SQLAlchemy do motor vehicle
            
        Returns:
            Car: Entidade do domínio
        """
        # Criar entidade MotorVehicle
        motor_vehicle = MotorVehicle(
            id=motor_vehicle_model.id,
            model=motor_vehicle_model.model,
            year=motor_vehicle_model.year,
            price=motor_vehicle_model.price,
            mileage=motor_vehicle_model.mileage,
            fuel_type=motor_vehicle_model.fuel_type,
            color=motor_vehicle_model.color,
            city=motor_vehicle_model.city,
            status=motor_vehicle_model.status,
            additional_description=motor_vehicle_model.additional_description,
            created_at=motor_vehicle_model.created_at,
            updated_at=motor_vehicle_model.updated_at
        )
        
        # Criar entidade Car
        return Car(
            id=car_model.vehicle_id,
            motor_vehicle=motor_vehicle,
            bodywork=car_model.bodywork,
            transmission=car_model.transmission,
            updated_at=car_model.updated_at
        )
