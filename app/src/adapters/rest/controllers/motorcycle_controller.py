"""
Controller para gerenciamento de motocicletas - Adapters Layer

Aplicando Clean Architecture e SOLID Principles
"""

from typing import List, Optional, Dict, Any
import logging
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.application.dtos.motorcycle_dto import (
    MotorcycleCreateDto,
    MotorcycleUpdateNestedDto,
    MotorcycleUpdateDto,
    MotorcycleSearchDto
)
from src.application.use_cases.vehicles import (
    CreateMotorcycleUseCase,
    GetMotorcycleUseCase,
    SearchMotorcyclesUseCase,
    UpdateMotorcycleUseCase,
    UpdateMotorcycleStatusUseCase,
    DeleteMotorcycleUseCase,
)
from src.adapters.rest.presenters.motorcycle_presenter import MotorcyclePresenter
from src.domain.exceptions import ValidationError, NotFoundError, BusinessRuleError

# Setup logging
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


class MotorcycleController:
    """
    Controller para gerenciamento de motocicletas - Adapters Layer
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por coordenar operações HTTP de motocicletas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende de abstrações (use cases) e não de implementações.
    """
    
    def __init__(
        self,
        create_use_case: CreateMotorcycleUseCase,
        get_use_case: GetMotorcycleUseCase,
        update_use_case: UpdateMotorcycleUseCase,
        update_status_use_case: UpdateMotorcycleStatusUseCase,
        delete_use_case: DeleteMotorcycleUseCase,
        search_use_case: SearchMotorcyclesUseCase,
        motorcycle_presenter: MotorcyclePresenter
    ):
        self._create_use_case = create_use_case
        self._get_use_case = get_use_case
        self._update_use_case = update_use_case
        self._update_status_use_case = update_status_use_case
        self._delete_use_case = delete_use_case
        self._search_use_case = search_use_case
        self._presenter = motorcycle_presenter

    async def create_motorcycle(self, motorcycle_data: MotorcycleCreateDto) -> JSONResponse:
        """
        Cria uma nova motocicleta.
        
        Args:
            motorcycle_data: Dados para criação da motocicleta
            
        Returns:
            JSONResponse com dados da motocicleta criada
            
        Raises:
            HTTPException: Em caso de erro de validação ou regra de negócio
        """
        try:
            motorcycle = await self._create_use_case.execute(motorcycle_data)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Use case retornou: {type(motorcycle)}")
            response_data = self._presenter.present(motorcycle)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Presenter retornou: {type(response_data)}")
            
            # Tentativa de serialização segura com modo JSON
            try:
                serialized_data = response_data.model_dump(mode='json') if hasattr(response_data, 'model_dump') else response_data
                logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados serializados com sucesso")
            except Exception as e:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro na serialização: {str(e)}")
                raise e
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Motocicleta criada com sucesso",
                    "data": serialized_data
                }
            )
            
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def get_motorcycle_by_id(self, motorcycle_id: int) -> JSONResponse:
        """
        Busca uma motocicleta pelo ID.
        
        Args:
            motorcycle_id: ID da motocicleta a ser buscada
            
        Returns:
            JSONResponse com dados da motocicleta
            
        Raises:
            HTTPException: Em caso de motocicleta não encontrada
        """
        try:
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Buscando motocicleta com ID: {motorcycle_id}")
            motorcycle = await self._get_use_case.execute(motorcycle_id)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Use case retornou: {type(motorcycle)}")
            
            response_data = self._presenter.present(motorcycle)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Presenter retornou: {type(response_data)}")
            
            # Tentativa de serialização segura com modo JSON
            try:
                serialized_data = response_data.model_dump(mode='json') if hasattr(response_data, 'model_dump') else response_data
                logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados serializados com sucesso")
            except Exception as e:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro na serialização: {str(e)}")
                raise e
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Motocicleta encontrada com sucesso",
                    "data": serialized_data
                }
            )
            
        except NotFoundError as e:
            logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Motocicleta não encontrada: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro interno: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )

    async def search_motorcycles(self, search_dto: MotorcycleSearchDto) -> JSONResponse:
        """
        Busca motocicletas com filtros.
        
        Args:
            search_dto: Filtros de busca
            
        Returns:
            JSONResponse com lista de motocicletas
        """
        try:
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Iniciando busca de motocicletas")
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] SearchDTO recebido: {search_dto}")
            
            logger.info("🔍 [MOTORCYCLE_CONTROLLER] Chamando use case execute...")
            result = await self._search_use_case.execute(search_dto)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Use case retornou {result.total if result else 0} resultados")
            
            logger.info("🔍 [MOTORCYCLE_CONTROLLER] Chamando presenter...")
            response_data = self._presenter.present_list(result)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Presenter processado com sucesso")
            
            logger.info("🔍 [MOTORCYCLE_CONTROLLER] Criando JSONResponse...")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Busca realizada com sucesso",
                    "data": response_data.model_dump(mode='json')  # Usando model_dump para melhor serialização JSON
                }
            )
            
        except Exception as e:
            logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro no search_motorcycles: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )

    async def update_motorcycle(self, motorcycle_id: int, motorcycle_data: MotorcycleUpdateNestedDto) -> JSONResponse:
        """
        Atualiza uma motocicleta existente.
        
        Args:
            motorcycle_id: ID da motocicleta a ser atualizada
            motorcycle_data: Dados para atualização
            
        Returns:
            JSONResponse com dados da motocicleta atualizada
        """
        try:
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Iniciando atualização da motocicleta ID: {motorcycle_id}")
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados recebidos: {motorcycle_data}")
            
            # Converter o DTO aninhado para o DTO flat esperado pelo use case
            flat_data = {
                "style": motorcycle_data.style,
                "starter": motorcycle_data.starter,
                "fuel_system": motorcycle_data.fuel_system,
                "engine_displacement": motorcycle_data.engine_displacement,
                "cooling": motorcycle_data.cooling,
                "engine_type": motorcycle_data.engine_type,
                "gears": motorcycle_data.gears,
                "front_rear_brake": motorcycle_data.front_rear_brake,
                "model": motorcycle_data.model,
                "year": motorcycle_data.year,
                "price": motorcycle_data.price,
                "mileage": motorcycle_data.mileage,
                "fuel_type": motorcycle_data.fuel_type,
                "engine_power": motorcycle_data.engine_power,
                "color": motorcycle_data.color,
                "city": motorcycle_data.city,
                "status": motorcycle_data.status,
                "description": motorcycle_data.description or motorcycle_data.additional_description
            }
            
            # Se tem motor_vehicle aninhado, usar os dados de lá (precedência)
            if motorcycle_data.motor_vehicle:
                mv = motorcycle_data.motor_vehicle
                flat_data.update({
                    "model": mv.model,
                    "year": mv.year,
                    "price": mv.price,
                    "mileage": mv.mileage,
                    "fuel_type": mv.fuel_type,
                    "engine_power": mv.engine_power,
                    "color": mv.color,
                    "status": mv.status,
                    "description": mv.description
                })
            
            # Filtrar valores None
            filtered_data = {k: v for k, v in flat_data.items() if v is not None}
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados filtrados: {filtered_data}")
            
            update_dto = MotorcycleUpdateDto(**filtered_data)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] UpdateDTO criado com sucesso")
            
            motorcycle = await self._update_use_case.execute(motorcycle_id, update_dto)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Use case executado com sucesso")
            response_data = self._presenter.present(motorcycle)
            
            # Tentativa de serialização segura com modo JSON
            try:
                serialized_data = response_data.model_dump(mode='json') if hasattr(response_data, 'model_dump') else response_data
                logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados de atualização serializados com sucesso")
            except Exception as e:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro na serialização de atualização: {str(e)}")
                raise e
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Motocicleta atualizada com sucesso",
                    "data": serialized_data
                }
            )
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def delete_motorcycle(self, motorcycle_id: int) -> JSONResponse:
        """
        Remove uma motocicleta do sistema.
        
        Args:
            motorcycle_id: ID da motocicleta a ser removida
            
        Returns:
            JSONResponse confirmando remoção
        """
        try:
            await self._delete_use_case.execute(motorcycle_id)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Motocicleta removida com sucesso"
                }
            )
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def deactivate_motorcycle(self, motorcycle_id: int) -> JSONResponse:
        """Desativa uma motorcycle."""
        try:
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Desativando motocicleta ID: {motorcycle_id}")
            motorcycle = await self._update_status_use_case.execute(motorcycle_id, "Inativo")
            
            if not motorcycle:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Motocicleta não encontrada: {motorcycle_id}")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motocicleta não encontrada")
            
            response_data = self._presenter.present(motorcycle)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Presenter executado com sucesso")
            
            # Tentativa de serialização segura com modo JSON
            try:
                serialized_data = response_data.model_dump(mode='json') if hasattr(response_data, 'model_dump') else response_data
                logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados de desativação serializados com sucesso")
            except Exception as e:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro na serialização de desativação: {str(e)}")
                raise e
            
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={
                    "message": "Motocicleta desativada com sucesso", 
                    "data": serialized_data
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro interno na desativação: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Erro interno do servidor: {str(e)}"
            )

    async def activate_motorcycle(self, motorcycle_id: int) -> JSONResponse:
        """Ativa uma motorcycle."""
        try:
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Ativando motocicleta ID: {motorcycle_id}")
            motorcycle = await self._update_status_use_case.execute(motorcycle_id, "Ativo")
            
            if not motorcycle:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Motocicleta não encontrada: {motorcycle_id}")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motocicleta não encontrada")
            
            response_data = self._presenter.present(motorcycle)
            logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Presenter executado com sucesso")
            
            # Tentativa de serialização segura com modo JSON
            try:
                serialized_data = response_data.model_dump(mode='json') if hasattr(response_data, 'model_dump') else response_data
                logger.info(f"🔍 [MOTORCYCLE_CONTROLLER] Dados de ativação serializados com sucesso")
            except Exception as e:
                logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro na serialização de ativação: {str(e)}")
                raise e
            
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={
                    "message": "Motocicleta ativada com sucesso", 
                    "data": serialized_data
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ [MOTORCYCLE_CONTROLLER] Erro interno na ativação: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Erro interno do servidor: {str(e)}"
            )
