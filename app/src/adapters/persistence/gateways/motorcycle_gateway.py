from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.domain.entities.motorcycle import Motorcycle
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.infrastructure.database.models.motorcycle_model import MotorcycleModel
from src.infrastructure.database.models.car_model import MotorVehicleModel
from src.infrastructure.database.connection import get_db_session
import logging

logger = logging.getLogger(__name__)


class MotorcycleGateway(MotorcycleRepository):
    """
    Gateway de persistência para motocicletas.
    
    Implementa a interface MotorcycleRepository definida no domínio.
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a abstração definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência de dados de motocicletas.
    """
    
    def __init__(self):
        pass
    
    async def save(self, motorcycle: Motorcycle) -> Motorcycle:
        """
        Salva uma motocicleta no banco de dados.
        
        Args:
            motorcycle: Entidade Motorcycle do domínio
            
        Returns:
            Motorcycle: Entidade Motorcycle salva com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        try:
            with get_db_session() as session:
                # Primeiro salva o motor_vehicle
                motor_vehicle_model = MotorVehicleModel(
                    brand=motorcycle.motor_vehicle.brand,
                    model=motorcycle.motor_vehicle.model,
                    year=motorcycle.motor_vehicle.year,
                    price=float(motorcycle.motor_vehicle.price),
                    mileage=motorcycle.motor_vehicle.mileage,
                    fuel_type=motorcycle.motor_vehicle.fuel_type,
                    engine_power=motorcycle.motor_vehicle.engine_power,
                    color=motorcycle.motor_vehicle.color,
                    status=motorcycle.motor_vehicle.status,
                    description=motorcycle.motor_vehicle.description
                )
                
                session.add(motor_vehicle_model)
                session.flush()  # Para obter o ID
                
                # Agora salva a motocicleta
                motorcycle_model = MotorcycleModel(
                    motor_vehicle_id=motor_vehicle_model.id,
                    motorcycle_type=motorcycle.motorcycle_type,
                    cylinder_capacity=motorcycle.cylinder_capacity,
                    has_abs=motorcycle.has_abs,
                    has_traction_control=motorcycle.has_traction_control,
                    seat_height=motorcycle.seat_height,
                    dry_weight=motorcycle.dry_weight,
                    fuel_capacity=motorcycle.fuel_capacity
                )
                
                session.add(motorcycle_model)
                session.commit()
                session.refresh(motorcycle_model)
                session.refresh(motor_vehicle_model)
                
                # Converter modelo de banco para entidade do domínio
                saved_motorcycle = self._model_to_entity(motorcycle_model, motor_vehicle_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(motorcycle_model)
                session.expunge(motor_vehicle_model)
                
                logger.info(f"Motocicleta criada com sucesso. ID: {saved_motorcycle.id}")
                return saved_motorcycle
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao salvar motocicleta: {str(e)}")
            raise Exception(f"Erro ao salvar motocicleta: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao salvar motocicleta: {str(e)}")
            raise Exception(f"Erro inesperado ao salvar motocicleta: {str(e)}")
    
    async def update(self, motorcycle: Motorcycle) -> Motorcycle:
        """
        Atualiza uma motocicleta existente.
        
        Args:
            motorcycle: Entidade Motorcycle do domínio com dados atualizados
            
        Returns:
            Motorcycle: Entidade Motorcycle atualizada
        """
        try:
            with get_db_session() as session:
                # Buscar a motocicleta existente
                motorcycle_model = session.query(MotorcycleModel).filter(MotorcycleModel.id == motorcycle.id).first()
                if not motorcycle_model:
                    raise Exception(f"Motocicleta com ID {motorcycle.id} não encontrada")
                
                # Buscar o motor_vehicle
                motor_vehicle_model = session.query(MotorVehicleModel).filter(
                    MotorVehicleModel.id == motorcycle_model.motor_vehicle_id
                ).first()
                
                # Atualizar motor_vehicle
                motor_vehicle_model.brand = motorcycle.motor_vehicle.brand
                motor_vehicle_model.model = motorcycle.motor_vehicle.model
                motor_vehicle_model.year = motorcycle.motor_vehicle.year
                motor_vehicle_model.price = float(motorcycle.motor_vehicle.price)
                motor_vehicle_model.mileage = motorcycle.motor_vehicle.mileage
                motor_vehicle_model.fuel_type = motorcycle.motor_vehicle.fuel_type
                motor_vehicle_model.engine_power = motorcycle.motor_vehicle.engine_power
                motor_vehicle_model.color = motorcycle.motor_vehicle.color
                motor_vehicle_model.status = motorcycle.motor_vehicle.status
                motor_vehicle_model.description = motorcycle.motor_vehicle.description
                
                # Atualizar motocicleta
                motorcycle_model.motorcycle_type = motorcycle.motorcycle_type
                motorcycle_model.cylinder_capacity = motorcycle.cylinder_capacity
                motorcycle_model.has_abs = motorcycle.has_abs
                motorcycle_model.has_traction_control = motorcycle.has_traction_control
                motorcycle_model.seat_height = motorcycle.seat_height
                motorcycle_model.dry_weight = motorcycle.dry_weight
                motorcycle_model.fuel_capacity = motorcycle.fuel_capacity
                
                session.commit()
                session.refresh(motorcycle_model)
                session.refresh(motor_vehicle_model)
                
                # Converter modelo de banco para entidade do domínio
                updated_motorcycle = self._model_to_entity(motorcycle_model, motor_vehicle_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(motorcycle_model)
                session.expunge(motor_vehicle_model)
                
                logger.info(f"Motocicleta atualizada com sucesso. ID: {updated_motorcycle.id}")
                return updated_motorcycle
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar motocicleta: {str(e)}")
            raise Exception(f"Erro ao atualizar motocicleta: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar motocicleta: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar motocicleta: {str(e)}")
    
    async def find_by_id(self, motorcycle_id: int) -> Optional[Motorcycle]:
        """
        Busca uma motocicleta pelo ID.
        
        Args:
            motorcycle_id: ID da motocicleta
            
        Returns:
            Optional[Motorcycle]: Entidade Motorcycle encontrada ou None
        """
        try:
            with get_db_session() as session:
                motorcycle_model = session.query(MotorcycleModel).filter(MotorcycleModel.id == motorcycle_id).first()
                
                if motorcycle_model:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == motorcycle_model.motor_vehicle_id
                    ).first()
                    
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(motorcycle_model)
                    session.expunge(motor_vehicle_model)
                    
                    return self._model_to_entity(motorcycle_model, motor_vehicle_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar motocicleta por ID {motorcycle_id}: {str(e)}")
            raise Exception(f"Erro ao buscar motocicleta: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar motocicleta por ID {motorcycle_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar motocicleta: {str(e)}")
    
    async def find_all(self) -> List[Motorcycle]:
        """
        Busca todas as motocicletas.
        
        Returns:
            List[Motorcycle]: Lista de entidades Motorcycle
        """
        try:
            with get_db_session() as session:
                motorcycle_models = session.query(MotorcycleModel).join(MotorVehicleModel).all()
                
                motorcycles = []
                for motorcycle_model in motorcycle_models:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == motorcycle_model.motor_vehicle_id
                    ).first()
                    
                    session.expunge(motorcycle_model)
                    session.expunge(motor_vehicle_model)
                    motorcycles.append(self._model_to_entity(motorcycle_model, motor_vehicle_model))
                
                return motorcycles
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todas as motocicletas: {str(e)}")
            raise Exception(f"Erro ao buscar motocicletas: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar todas as motocicletas: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar motocicletas: {str(e)}")
    
    async def delete(self, motorcycle_id: int) -> bool:
        """
        Remove uma motocicleta pelo ID.
        
        Args:
            motorcycle_id: ID da motocicleta
            
        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        try:
            with get_db_session() as session:
                motorcycle_model = session.query(MotorcycleModel).filter(MotorcycleModel.id == motorcycle_id).first()
                
                if not motorcycle_model:
                    return False
                
                # Buscar e remover o motor_vehicle associado
                motor_vehicle_model = session.query(MotorVehicleModel).filter(
                    MotorVehicleModel.id == motorcycle_model.motor_vehicle_id
                ).first()
                
                session.delete(motorcycle_model)
                if motor_vehicle_model:
                    session.delete(motor_vehicle_model)
                
                session.commit()
                
                logger.info(f"Motocicleta removida com sucesso. ID: {motorcycle_id}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao remover motocicleta {motorcycle_id}: {str(e)}")
            raise Exception(f"Erro ao remover motocicleta: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao remover motocicleta {motorcycle_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao remover motocicleta: {str(e)}")
    
    async def search(self, filters: Dict[str, Any], limit: int = 50, offset: int = 0) -> Tuple[List[Motorcycle], int]:
        """
        Busca motocicletas com filtros.
        
        Args:
            filters: Dicionário com filtros
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            Tuple[List[Motorcycle], int]: Lista de motocicletas e total de registros
        """
        try:
            with get_db_session() as session:
                query = session.query(MotorcycleModel).join(MotorVehicleModel)
                
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
                if filters.get('motorcycle_type'):
                    query = query.filter(MotorcycleModel.motorcycle_type == filters['motorcycle_type'])
                if filters.get('cylinder_capacity_min'):
                    query = query.filter(MotorcycleModel.cylinder_capacity >= filters['cylinder_capacity_min'])
                if filters.get('cylinder_capacity_max'):
                    query = query.filter(MotorcycleModel.cylinder_capacity <= filters['cylinder_capacity_max'])
                if filters.get('has_abs') is not None:
                    query = query.filter(MotorcycleModel.has_abs == filters['has_abs'])
                if filters.get('status'):
                    query = query.filter(MotorVehicleModel.status == filters['status'])
                
                # Contar total
                total = query.count()
                
                # Aplicar paginação
                motorcycle_models = query.offset(offset).limit(limit).all()
                
                motorcycles = []
                for motorcycle_model in motorcycle_models:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == motorcycle_model.motor_vehicle_id
                    ).first()
                    
                    session.expunge(motorcycle_model)
                    session.expunge(motor_vehicle_model)
                    motorcycles.append(self._model_to_entity(motorcycle_model, motor_vehicle_model))
                
                return motorcycles, total
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar motocicletas com filtros: {str(e)}")
            raise Exception(f"Erro ao buscar motocicletas: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar motocicletas com filtros: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar motocicletas: {str(e)}")
    
    def _model_to_entity(self, motorcycle_model: MotorcycleModel, motor_vehicle_model: MotorVehicleModel) -> Motorcycle:
        """
        Converte modelo de banco para entidade do domínio.
        
        Args:
            motorcycle_model: Modelo SQLAlchemy da motocicleta
            motor_vehicle_model: Modelo SQLAlchemy do motor vehicle
            
        Returns:
            Motorcycle: Entidade do domínio
        """
        # Criar entidade MotorVehicle
        motor_vehicle = MotorVehicle(
            id=motor_vehicle_model.id,
            brand=motor_vehicle_model.brand,
            model=motor_vehicle_model.model,
            year=motor_vehicle_model.year,
            price=motor_vehicle_model.price,
            mileage=motor_vehicle_model.mileage,
            fuel_type=motor_vehicle_model.fuel_type,
            engine_power=motor_vehicle_model.engine_power,
            color=motor_vehicle_model.color,
            status=motor_vehicle_model.status,
            description=motor_vehicle_model.description,
            created_at=motor_vehicle_model.created_at,
            updated_at=motor_vehicle_model.updated_at
        )
        
        # Criar entidade Motorcycle
        return Motorcycle(
            id=motorcycle_model.id,
            motor_vehicle=motor_vehicle,
            motorcycle_type=motorcycle_model.motorcycle_type,
            cylinder_capacity=motorcycle_model.cylinder_capacity,
            has_abs=motorcycle_model.has_abs,
            has_traction_control=motorcycle_model.has_traction_control,
            seat_height=motorcycle_model.seat_height,
            dry_weight=motorcycle_model.dry_weight,
            fuel_capacity=motorcycle_model.fuel_capacity,
            updated_at=motorcycle_model.updated_at
        )
