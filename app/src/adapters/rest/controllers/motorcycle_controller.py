"""
Controller para gerenciamento de motocicletas - Adapters Layer

Aplicando Clean Architecture e SOLID Principles
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.application.dtos.motorcycle_dto import (
    MotorcycleCreateDto,
    MotorcycleUpdateDto,
    MotorcycleSearchDto
)
from src.application.use_cases.vehicles import (
    CreateMotorcycleUseCase,
    GetMotorcycleUseCase,
    SearchMotorcyclesUseCase,
    UpdateMotorcycleUseCase,
    DeleteMotorcycleUseCase,
)
from src.adapters.rest.presenters.motorcycle_presenter import MotorcyclePresenter
from src.domain.exceptions import ValidationError, NotFoundError, BusinessRuleError


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
        delete_use_case: DeleteMotorcycleUseCase,
        search_use_case: SearchMotorcyclesUseCase,
        motorcycle_presenter: MotorcyclePresenter
    ):
        self._create_use_case = create_use_case
        self._get_use_case = get_use_case
        self._update_use_case = update_use_case
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
            response_data = self._presenter.present_motorcycle(motorcycle)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Motocicleta criada com sucesso",
                    "data": response_data
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

    async def get_motorcycle_by_id(self, motorcycle_id: UUID) -> JSONResponse:
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
            motorcycle = await self._get_use_case.execute(motorcycle_id)
            response_data = self._presenter.present_motorcycle(motorcycle)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Motocicleta encontrada com sucesso",
                    "data": response_data
                }
            )
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
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
            result = await self._search_use_case.execute(search_dto)
            response_data = self._presenter.present_motorcycle_list(result)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Busca realizada com sucesso",
                    "data": response_data
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def update_motorcycle(self, motorcycle_id: UUID, motorcycle_data: MotorcycleUpdateDto) -> JSONResponse:
        """
        Atualiza uma motocicleta existente.
        
        Args:
            motorcycle_id: ID da motocicleta a ser atualizada
            motorcycle_data: Dados para atualização
            
        Returns:
            JSONResponse com dados da motocicleta atualizada
        """
        try:
            motorcycle = await self._update_use_case.execute(motorcycle_id, motorcycle_data)
            response_data = self._presenter.present_motorcycle(motorcycle)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Motocicleta atualizada com sucesso",
                    "data": response_data
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

    async def delete_motorcycle(self, motorcycle_id: UUID) -> JSONResponse:
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
