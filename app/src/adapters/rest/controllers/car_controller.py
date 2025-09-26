"""
Controller para gerenciamento de carros - Adapters Layer

Aplicando Clean Architecture e SOLID Principles
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.application.dtos.car_dto import (
    CarCreateDto,
    CarUpdateNestedDto,
    CarUpdateDto,
    CarSearchDto
)
from src.application.use_cases.vehicles import (
    CreateCarUseCase,
    GetCarUseCase,
    SearchCarsUseCase,
    UpdateCarUseCase,
    UpdateCarStatusUseCase,
    DeleteCarUseCase,
)
from src.adapters.rest.presenters.car_presenter import CarPresenter
from src.domain.exceptions import ValidationError, NotFoundError, BusinessRuleError


class CarController:
    """
    Controller para gerenciamento de carros - Adapters Layer
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por coordenar operações HTTP de carros.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende de abstrações (use cases) e não de implementações.
    """
    
    def __init__(
        self,
        create_use_case: CreateCarUseCase,
        get_use_case: GetCarUseCase,
        update_use_case: UpdateCarUseCase,
        update_status_use_case: UpdateCarStatusUseCase,
        delete_use_case: DeleteCarUseCase,
        search_use_case: SearchCarsUseCase,
        car_presenter: CarPresenter
    ):
        self._create_use_case = create_use_case
        self._get_use_case = get_use_case
        self._update_use_case = update_use_case
        self._update_status_use_case = update_status_use_case
        self._delete_use_case = delete_use_case
        self._search_use_case = search_use_case
        self._presenter = car_presenter

    async def create_car(self, car_data: CarCreateDto) -> JSONResponse:
        """
        Cria um novo carro.
        
        Args:
            car_data: Dados para criação do carro
            
        Returns:
            JSONResponse com dados do carro criado
            
        Raises:
            HTTPException: Em caso de erro de validação ou regra de negócio
        """
        try:
            car = await self._create_use_case.execute(car_data)
            response_data = self._presenter.present_car(car)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Carro criado com sucesso",
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

    async def get_car_by_id(self, car_id: int) -> JSONResponse:
        """
        Busca um carro pelo ID.
        
        Args:
            car_id: ID do carro a ser buscado
            
        Returns:
            JSONResponse com dados do carro
            
        Raises:
            HTTPException: Em caso de carro não encontrado
        """
        try:
            car = await self._get_use_case.execute(car_id)
            response_data = self._presenter.present_car(car)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Carro encontrado com sucesso",
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

    async def search_cars(self, search_dto: CarSearchDto) -> JSONResponse:
        """
        Busca carros com filtros.
        
        Args:
            search_dto: Filtros de busca
            
        Returns:
            JSONResponse com lista de carros
        """
        try:
            result = await self._search_use_case.execute(search_dto)
            response_data = self._presenter.present_car_list(result)
            
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

    async def update_car(self, car_id: int, car_data: CarUpdateNestedDto) -> JSONResponse:
        """
        Atualiza um carro existente.
        
        Args:
            car_id: ID do carro a ser atualizado
            car_data: Dados para atualização
            
        Returns:
            JSONResponse com dados do carro atualizado
        """
        try:
            # Converter o DTO aninhado para o DTO flat esperado pelo use case
            flat_data = {
                "bodywork": car_data.bodywork,
                "transmission": car_data.transmission,
                "model": car_data.model,
                "year": str(car_data.year) if car_data.year else None,
                "mileage": car_data.mileage,
                "fuel_type": car_data.fuel_type,
                "color": car_data.color,
                "city": car_data.city,
                "price": car_data.price,
                "additional_description": car_data.additional_description
            }
            
            # Se tem motor_vehicle aninhado, usar os dados de lá (precedência)
            if car_data.motor_vehicle:
                mv = car_data.motor_vehicle
                flat_data.update({
                    "model": mv.model,
                    "year": str(mv.year) if mv.year else None,
                    "mileage": mv.mileage,
                    "fuel_type": mv.fuel_type,
                    "color": mv.color,
                    "price": mv.price,
                    "additional_description": mv.description
                })
            
            # Filtrar valores None
            filtered_data = {k: v for k, v in flat_data.items() if v is not None}
            update_dto = CarUpdateDto(**filtered_data)
            
            car = await self._update_use_case.execute(car_id, update_dto)
            response_data = self._presenter.present_car(car)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Carro atualizado com sucesso",
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

    async def delete_car(self, car_id: int) -> JSONResponse:
        """
        Remove um carro do sistema.
        
        Args:
            car_id: ID do carro a ser removido
            
        Returns:
            JSONResponse confirmando remoção
        """
        try:
            await self._delete_use_case.execute(car_id)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Carro removido com sucesso"
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

    async def deactivate_car(self, car_id: int) -> JSONResponse:
        """Desativa um carro."""
        try:
            car = await self._update_status_use_case.execute(car_id, "Inativo")
            if not car:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")
            response_data = self._presenter.present_car(car)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Carro desativado com sucesso", "data": response_data})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

    async def activate_car(self, car_id: int) -> JSONResponse:
        """Ativa um carro."""
        try:
            car = await self._update_status_use_case.execute(car_id, "Ativo")
            if not car:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")
            response_data = self._presenter.present_car(car)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Carro ativado com sucesso", "data": response_data})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
