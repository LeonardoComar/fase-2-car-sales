from typing import Optional, List, Dict, Any, Tuple
from decimal import Decimal
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, select
from src.domain.entities.motorcycle import Motorcycle
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.infrastructure.database.models.motorcycle_model import MotorcycleModel
from src.infrastructure.database.models.motor_vehicle_model import MotorVehicleModel
from src.infrastructure.database.connection import get_db_session

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
            logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Iniciando salvamento de motocicleta: {motorcycle.motor_vehicle.model}")
            
            with get_db_session() as session:
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Criando MotorVehicleModel...")
                # Primeiro salva o motor_vehicle
                motor_vehicle_model = MotorVehicleModel(
                    model=motorcycle.motor_vehicle.model,
                    year=motorcycle.motor_vehicle.year,
                    price=float(motorcycle.motor_vehicle.price),
                    mileage=motorcycle.motor_vehicle.mileage,
                    fuel_type=motorcycle.motor_vehicle.fuel_type,
                    color=motorcycle.motor_vehicle.color,
                    city=motorcycle.motor_vehicle.city,
                    additional_description=motorcycle.motor_vehicle.additional_description,
                    status=motorcycle.motor_vehicle.status
                )
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Salvando MotorVehicleModel...")
                session.add(motor_vehicle_model)
                session.flush()  # Para obter o ID
                logger.info(f"🔍 [MOTORCYCLE_GATEWAY] MotorVehicleModel salvo com ID: {motor_vehicle_model.id}")
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Criando MotorcycleModel...")
                # Agora salva a motocicleta
                motorcycle_model = MotorcycleModel(
                    vehicle_id=motor_vehicle_model.id,
                    starter=motorcycle.starter or "Elétrico",
                    fuel_system=motorcycle.fuel_system or "Injeção eletrônica",
                    engine_displacement=motorcycle.engine_displacement,
                    cooling=motorcycle.cooling or "Líquido",
                    style=motorcycle.style,
                    engine_type=motorcycle.engine_type or "4 tempos",
                    gears=motorcycle.gears or 6,
                    front_rear_brake=motorcycle.front_rear_brake or "Disco/Disco"
                )
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Salvando MotorcycleModel...")
                session.add(motorcycle_model)
                session.commit()
                session.refresh(motorcycle_model)
                session.refresh(motor_vehicle_model)
                logger.info(f"🔍 [MOTORCYCLE_GATEWAY] MotorcycleModel salvo com vehicle_id: {motorcycle_model.vehicle_id}")
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Convertendo para entidade...")
                # Converter modelo de banco para entidade do domínio
                saved_motorcycle = self._model_to_entity(motorcycle_model, motor_vehicle_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(motorcycle_model)
                session.expunge(motor_vehicle_model)
                
                logger.info(f"✅ [MOTORCYCLE_GATEWAY] Motocicleta criada com sucesso. ID: {saved_motorcycle.id}")
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
                motorcycle_model = session.query(MotorcycleModel).filter(MotorcycleModel.vehicle_id == motorcycle.id).first()
                if not motorcycle_model:
                    raise Exception(f"Motocicleta com ID {motorcycle.id} não encontrada")
                
                # Buscar o motor_vehicle
                motor_vehicle_model = session.query(MotorVehicleModel).filter(
                    MotorVehicleModel.id == motorcycle_model.vehicle_id
                ).first()
                
                # Atualizar motor_vehicle
                motor_vehicle_model.model = motorcycle.motor_vehicle.model
                motor_vehicle_model.year = motorcycle.motor_vehicle.year
                motor_vehicle_model.price = float(motorcycle.motor_vehicle.price)
                motor_vehicle_model.mileage = motorcycle.motor_vehicle.mileage
                motor_vehicle_model.fuel_type = motorcycle.motor_vehicle.fuel_type
                motor_vehicle_model.color = motorcycle.motor_vehicle.color
                motor_vehicle_model.city = motorcycle.motor_vehicle.city
                motor_vehicle_model.additional_description = motorcycle.motor_vehicle.additional_description
                motor_vehicle_model.status = motorcycle.motor_vehicle.status
                
                # Atualizar motocicleta
                motorcycle_model.starter = motorcycle.starter
                motorcycle_model.fuel_system = motorcycle.fuel_system
                motorcycle_model.engine_displacement = motorcycle.engine_displacement
                motorcycle_model.cooling = motorcycle.cooling
                motorcycle_model.style = motorcycle.style
                motorcycle_model.engine_type = motorcycle.engine_type
                motorcycle_model.gears = motorcycle.gears
                motorcycle_model.front_rear_brake = motorcycle.front_rear_brake
                
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
                motorcycle_model = session.query(MotorcycleModel).filter(MotorcycleModel.vehicle_id == motorcycle_id).first()
                
                if motorcycle_model:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == motorcycle_model.vehicle_id
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
                        MotorVehicleModel.id == motorcycle_model.vehicle_id
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
                motorcycle_model = session.query(MotorcycleModel).filter(MotorcycleModel.vehicle_id == motorcycle_id).first()
                
                if not motorcycle_model:
                    return False
                
                # Buscar e remover o motor_vehicle associado
                motor_vehicle_model = session.query(MotorVehicleModel).filter(
                    MotorVehicleModel.id == motorcycle_model.vehicle_id
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
                
                # Aplicar filtros (removendo campos inexistentes)
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
                if filters.get('style'):  # Usar 'style' em vez de 'motorcycle_type'
                    query = query.filter(MotorcycleModel.style == filters['style'])
                if filters.get('engine_displacement_min'):  # Usar 'engine_displacement' em vez de 'cylinder_capacity'
                    query = query.filter(MotorcycleModel.engine_displacement >= filters['engine_displacement_min'])
                if filters.get('engine_displacement_max'):  # Usar 'engine_displacement' em vez de 'cylinder_capacity'
                    query = query.filter(MotorcycleModel.engine_displacement <= filters['engine_displacement_max'])
                if filters.get('status'):
                    query = query.filter(MotorVehicleModel.status == filters['status'])
                
                # Contar total
                total = query.count()
                
                # Aplicar paginação
                motorcycle_models = query.offset(offset).limit(limit).all()
                
                motorcycles = []
                for motorcycle_model in motorcycle_models:
                    motor_vehicle_model = session.query(MotorVehicleModel).filter(
                        MotorVehicleModel.id == motorcycle_model.vehicle_id
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
            model=motor_vehicle_model.model or "",
            year=motor_vehicle_model.year or "",
            price=Decimal(str(motor_vehicle_model.price)) if motor_vehicle_model.price else Decimal('0.00'),
            mileage=motor_vehicle_model.mileage or 0,
            fuel_type=motor_vehicle_model.fuel_type or "",
            color=motor_vehicle_model.color or "",
            city=motor_vehicle_model.city or "",
            additional_description=motor_vehicle_model.additional_description,
            status=motor_vehicle_model.status or MotorVehicle.STATUS_ATIVO,
            created_at=motor_vehicle_model.created_at,
            updated_at=motor_vehicle_model.updated_at
        )
        
        # Criar entidade Motorcycle
        return Motorcycle(
            id=motorcycle_model.vehicle_id,
            motor_vehicle=motor_vehicle,
            starter=motorcycle_model.starter,
            fuel_system=motorcycle_model.fuel_system,
            engine_displacement=motorcycle_model.engine_displacement,
            cooling=motorcycle_model.cooling,
            style=motorcycle_model.style,
            engine_type=motorcycle_model.engine_type,
            gears=motorcycle_model.gears,
            front_rear_brake=motorcycle_model.front_rear_brake,
            created_at=motor_vehicle_model.created_at,  # Usando timestamps do MotorVehicle
            updated_at=motorcycle_model.updated_at or motor_vehicle_model.updated_at
        )

    async def find_by_criteria(
        self,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        style: Optional[str] = None,  # Mudança: motorcycle_type para style
        engine_displacement_min: Optional[int] = None,  # Mudança: cylinder_capacity_min para engine_displacement_min
        engine_displacement_max: Optional[int] = None,  # Mudança: cylinder_capacity_max para engine_displacement_max
        status: Optional[str] = None,
        available_only: bool = False,
        order_by_price: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Motorcycle]:
        """
        Busca motocicletas por critérios específicos.
        """
        try:
            logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Iniciando busca por critérios")
            logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Parâmetros: model={model}, status={status}, price_min={price_min}")
            logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Parâmetros: engine_displacement_min={engine_displacement_min}, skip={skip}, limit={limit}")
            
            logger.info("🔍 [MOTORCYCLE_GATEWAY] Abrindo sessão do banco...")
            with get_db_session() as session:
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Sessão aberta, criando query...")
                
                # TESTE: vamos primeiro ver se conseguimos listar os modelos
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Testando acesso aos modelos...")
                try:
                    motor_vehicle_count = session.query(MotorVehicleModel).count()
                    motorcycle_count = session.query(MotorcycleModel).count()
                    logger.info(f"🔍 [MOTORCYCLE_GATEWAY] MotorVehicleModel count: {motor_vehicle_count}")
                    logger.info(f"🔍 [MOTORCYCLE_GATEWAY] MotorcycleModel count: {motorcycle_count}")
                except Exception as e:
                    logger.error(f"❌ [MOTORCYCLE_GATEWAY] Erro ao contar modelos: {str(e)}", exc_info=True)
                    raise e
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Criando query com JOIN...")
                try:
                    query = session.query(MotorcycleModel).join(MotorVehicleModel)
                    logger.info("🔍 [MOTORCYCLE_GATEWAY] Query com JOIN criada com sucesso")
                except Exception as e:
                    logger.error(f"❌ [MOTORCYCLE_GATEWAY] Erro ao criar query com JOIN: {str(e)}", exc_info=True)
                    raise e
                
                # Aplicar filtros
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Aplicando filtros...")
                if model:
                    query = query.filter(MotorVehicleModel.model.ilike(f"%{model}%"))
                    logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Filtro model aplicado: {model}")
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
                if status:
                    query = query.filter(MotorVehicleModel.status == status)
                    logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Filtro status aplicado: {status}")
                if available_only:
                    query = query.filter(MotorVehicleModel.status == "Ativo")
                
                # Filtros específicos de motocicleta (baseados na estrutura real da tabela)
                if engine_displacement_min:
                    query = query.filter(MotorcycleModel.engine_displacement >= engine_displacement_min)
                if engine_displacement_max:
                    query = query.filter(MotorcycleModel.engine_displacement <= engine_displacement_max)
                if style:
                    query = query.filter(MotorcycleModel.style.ilike(f"%{style}%"))
                
                # Aplicar ordenação por preço
                if order_by_price:
                    if order_by_price.lower() == 'asc':
                        query = query.order_by(MotorVehicleModel.price.asc())
                    elif order_by_price.lower() == 'desc':
                        query = query.order_by(MotorVehicleModel.price.desc())
                
                # Aplicar paginação
                logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Aplicando paginação: offset={skip}, limit={limit}")
                query = query.offset(skip).limit(limit)
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Executando query...")
                try:
                    results = query.all()
                    logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Query executada com sucesso. {len(results)} resultados encontrados")
                except Exception as e:
                    logger.error(f"❌ [MOTORCYCLE_GATEWAY] Erro ao executar query: {str(e)}", exc_info=True)
                    raise e
                
                motorcycles = []
                
                logger.info("🔍 [MOTORCYCLE_GATEWAY] Convertendo resultados para entidades...")
                for i, motorcycle_model in enumerate(results):
                    try:
                        logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Processando resultado {i+1}/{len(results)}")
                        motor_vehicle_model = motorcycle_model.motor_vehicle
                        session.expunge(motorcycle_model)
                        session.expunge(motor_vehicle_model)
                        entity = self._model_to_entity(motorcycle_model, motor_vehicle_model)
                        motorcycles.append(entity)
                        logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Resultado {i+1} convertido com sucesso")
                    except Exception as e:
                        logger.error(f"❌ [MOTORCYCLE_GATEWAY] Erro ao converter resultado {i+1}: {str(e)}", exc_info=True)
                        raise e
                
                logger.info(f"🔍 [MOTORCYCLE_GATEWAY] Busca concluída. {len(motorcycles)} motocicletas retornadas")
                return motorcycles
                
        except SQLAlchemyError as e:
            logger.error(f"❌ [MOTORCYCLE_GATEWAY] Erro SQLAlchemy ao buscar motocicletas por critérios: {str(e)}", exc_info=True)
            raise Exception(f"Erro ao buscar motocicletas: {str(e)}")
        except Exception as e:
            logger.error(f"❌ [MOTORCYCLE_GATEWAY] Erro inesperado ao buscar motocicletas por critérios: {str(e)}", exc_info=True)
            raise Exception(f"Erro inesperado ao buscar motocicletas: {str(e)}")

    async def count_by_criteria(
        self,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        style: Optional[str] = None,
        engine_displacement_min: Optional[int] = None,
        engine_displacement_max: Optional[int] = None,
        status: Optional[str] = None,
        available_only: bool = False
    ) -> int:
        """
        Conta motocicletas por critérios específicos.
        """
        try:
            with get_db_session() as session:
                # Buscar apenas na tabela motorcycles primeiro
                query = session.query(MotorcycleModel)
                
                # Se há filtros relacionados ao motor_vehicle, precisamos fazer um subquery
                motor_vehicle_filters = []
                if model:
                    motor_vehicle_filters.append(MotorVehicleModel.model.ilike(f"%{model}%"))
                if year_min:
                    motor_vehicle_filters.append(MotorVehicleModel.year >= str(year_min))
                if year_max:
                    motor_vehicle_filters.append(MotorVehicleModel.year <= str(year_max))
                if price_min:
                    motor_vehicle_filters.append(MotorVehicleModel.price >= price_min)
                if price_max:
                    motor_vehicle_filters.append(MotorVehicleModel.price <= price_max)
                if mileage_max:
                    motor_vehicle_filters.append(MotorVehicleModel.mileage <= mileage_max)
                if fuel_type:
                    motor_vehicle_filters.append(MotorVehicleModel.fuel_type.ilike(f"%{fuel_type}%"))
                if status:
                    motor_vehicle_filters.append(MotorVehicleModel.status.ilike(f"%{status}%"))
                if available_only:
                    motor_vehicle_filters.append(MotorVehicleModel.status == "Ativo")
                
                # Se há filtros de motor_vehicle, aplicar subquery
                if motor_vehicle_filters:
                    subquery = select(MotorVehicleModel.id).filter(and_(*motor_vehicle_filters))
                    query = query.filter(MotorcycleModel.vehicle_id.in_(subquery))
                
                # Aplicar filtros específicos da motorcycle
                if style:
                    query = query.filter(MotorcycleModel.style.ilike(f"%{style}%"))
                if engine_displacement_min:
                    query = query.filter(MotorcycleModel.engine_displacement >= engine_displacement_min)
                if engine_displacement_max:
                    query = query.filter(MotorcycleModel.engine_displacement <= engine_displacement_max)
                
                return query.count()
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar motocicletas por critérios: {str(e)}")
            raise Exception(f"Erro ao contar motocicletas: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao contar motocicletas por critérios: {str(e)}")
            raise Exception(f"Erro inesperado ao contar motocicletas: {str(e)}")
