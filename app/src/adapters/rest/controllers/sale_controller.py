"""
Controller para Vendas - Adapter Layer

Responsável por coordenar as requisições HTTP relacionadas a vendas.

Aplicando princípios SOLID:
- SRP: Responsável apenas por coordenar operações de vendas
- OCP: Extensível para novas operações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para operações de vendas
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import List, Optional
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from decimal import Decimal
from src.application.use_cases.sales.create_sale_use_case import CreateSaleUseCase
from src.application.use_cases.sales.get_sale_by_id_use_case import GetSaleByIdUseCase
from src.application.use_cases.sales.update_sale_use_case import UpdateSaleUseCase
from src.application.use_cases.sales.delete_sale_use_case import DeleteSaleUseCase
from src.application.use_cases.sales.list_sales_use_case import ListSalesUseCase
from src.application.use_cases.sales.sale_statistics_use_case import SaleStatisticsUseCase
from src.application.use_cases.sales.confirm_sale_use_case import ConfirmSaleUseCase
from src.application.dtos.sale_dto import (
    CreateSaleRequest,
    UpdateSaleRequest,
    SaleResponse,
    SaleStatisticsResponse,
    SalesListResponse
)


class SaleController:
    """
    Controller para gerenciamento de vendas.
    
    Coordena as operações CRUD e consultas relacionadas a vendas,
    delegando a lógica de negócio para os use cases apropriados.
    """
    
    def __init__(
        self,
        create_sale_use_case: CreateSaleUseCase,
        get_sale_by_id_use_case: GetSaleByIdUseCase,
        update_sale_use_case: UpdateSaleUseCase,
        delete_sale_use_case: DeleteSaleUseCase,
        list_sales_use_case: ListSalesUseCase,
        sale_statistics_use_case: SaleStatisticsUseCase,
        confirm_sale_use_case: ConfirmSaleUseCase
    ):
        """
        Inicializa o controller com todos os use cases necessários.
        
        Args:
            create_sale_use_case: Use case para criação de vendas
            get_sale_by_id_use_case: Use case para busca por ID
            update_sale_use_case: Use case para atualização
            delete_sale_use_case: Use case para exclusão
            list_sales_use_case: Use case para listagem
            sale_statistics_use_case: Use case para estatísticas
            confirm_sale_use_case: Use case para confirmação de vendas
        """
        self._create_sale_use_case = create_sale_use_case
        self._get_sale_by_id_use_case = get_sale_by_id_use_case
        self._update_sale_use_case = update_sale_use_case
        self._delete_sale_use_case = delete_sale_use_case
        self._list_sales_use_case = list_sales_use_case
        self._sale_statistics_use_case = sale_statistics_use_case
        self._confirm_sale_use_case = confirm_sale_use_case
    
    def _convert_decimals_to_float(self, obj):
        """
        Recursively converts all Decimal objects to float for JSON serialization.
        
        Args:
            obj: Object to convert (can be dict, list, or any other type)
            
        Returns:
            Object with Decimal values converted to float
        """
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: self._convert_decimals_to_float(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_decimals_to_float(item) for item in obj]
        else:
            return obj
    
    def _sale_to_dict(self, sale: SaleResponse) -> dict:
        """
        Converte SaleResponse para dict serializável, convertendo Decimal para float.
        
        Args:
            sale: Objeto SaleResponse
            
        Returns:
            dict: Dicionário serializável
        """
        sale_dict = sale.dict()
        return self._convert_decimals_to_float(sale_dict)
    
    async def create_sale(self, sale_data: CreateSaleRequest) -> SaleResponse:
        """
        Cria uma nova venda.
        
        Args:
            sale_data: Dados da venda a ser criada
            
        Returns:
            SaleResponse: Dados da venda criada
            
        Raises:
            HTTPException: Se houver erro na criação
        """
        try:
            result = await self._create_sale_use_case.execute(sale_data)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def get_sale_by_id(self, sale_id: int) -> SaleResponse:
        """
        Busca uma venda por ID.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            SaleResponse: Dados da venda encontrada
            
        Raises:
            HTTPException: Se venda não encontrada ou erro na busca
        """
        try:
            result = await self._get_sale_by_id_use_case.execute(sale_id)
            if not result:
                raise HTTPException(status_code=404, detail="Venda não encontrada")
            return result
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def update_sale(self, sale_id: int, sale_data: UpdateSaleRequest) -> SaleResponse:
        """
        Atualiza uma venda existente.
        
        Args:
            sale_id: ID da venda a ser atualizada
            sale_data: Dados para atualização
            
        Returns:
            SaleResponse: Dados da venda atualizada
            
        Raises:
            HTTPException: Se venda não encontrada ou erro na atualização
        """
        try:
            result = await self._update_sale_use_case.execute(sale_id, sale_data)
            if not result:
                raise HTTPException(status_code=404, detail="Venda não encontrada")
            return result
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def delete_sale(self, sale_id: int) -> dict:
        """
        Exclui uma venda.
        
        Args:
            sale_id: ID da venda a ser excluída
            
        Returns:
            dict: Confirmação da exclusão
            
        Raises:
            HTTPException: Se venda não encontrada ou erro na exclusão
        """
        try:
            result = await self._delete_sale_use_case.execute(sale_id)
            if not result:
                raise HTTPException(status_code=404, detail="Venda não encontrada")
            return {"message": "Venda excluída com sucesso"}
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def confirm_sale(self, sale_id: int) -> SaleResponse:
        """
        Confirma uma venda.
        
        Args:
            sale_id: ID da venda a ser confirmada
            
        Returns:
            SaleResponse: Dados da venda confirmada
            
        Raises:
            HTTPException: Se venda não encontrada ou erro na confirmação
        """
        try:
            result = await self._confirm_sale_use_case.execute(sale_id)
            if not result:
                raise HTTPException(status_code=404, detail="Venda não encontrada")
            return result
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def list_sales(
        self,
        client_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        payment_method: Optional[str] = None,
        order_by_value: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> JSONResponse:
        """
        Lista vendas com filtros opcionais.
        
        Args:
            client_id: Filtro por cliente
            employee_id: Filtro por funcionário
            status: Filtro por status
            start_date: Data inicial
            end_date: Data final
            payment_method: Filtro por método de pagamento
            order_by_value: Ordenação por valor - 'asc' ou 'desc'
            skip: Registros para pular (paginação)
            limit: Limite de registros
            
        Returns:
            JSONResponse: Resposta formatada com lista de vendas
            
        Raises:
            HTTPException: Se erro na busca
        """
        try:
            result = await self._list_sales_use_case.execute(
                client_id=client_id,
                employee_id=employee_id,
                status=status,
                start_date=start_date,
                end_date=end_date,
                payment_method=payment_method,
                order_by_value=order_by_value,
                skip=skip,
                limit=limit
            )
            
            # Criar resposta seguindo o padrão de carros
            response_data = {
                "sales": [self._sale_to_dict(sale) for sale in result] if result else [],
                "total": len(result) if result else 0,
                "skip": skip,
                "limit": limit
            }
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Busca realizada com sucesso",
                    "data": response_data
                }
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def get_sales_by_client(
        self,
        client_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[SaleResponse]:
        """
        Busca vendas por cliente.
        
        Args:
            client_id: ID do cliente
            skip: Registros para pular
            limit: Limite de registros
            
        Returns:
            List[SaleResponse]: Lista de vendas do cliente
        """
        try:
            result = await self._list_sales_use_case.get_sales_by_client(
                client_id=client_id,
                skip=skip,
                limit=limit
            )
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def get_sales_by_employee(
        self,
        employee_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[SaleResponse]:
        """
        Busca vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            skip: Registros para pular
            limit: Limite de registros
            
        Returns:
            List[SaleResponse]: Lista de vendas do funcionário
        """
        try:
            result = await self._list_sales_use_case.get_sales_by_employee(
                employee_id=employee_id,
                skip=skip,
                limit=limit
            )
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def get_sales_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        employee_id: Optional[int] = None
    ) -> SaleStatisticsResponse:
        """
        Busca estatísticas de vendas.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            employee_id: Filtro por funcionário
            
        Returns:
            SaleStatisticsResponse: Estatísticas das vendas
        """
        try:
            result = await self._sale_statistics_use_case.execute(
                start_date=start_date,
                end_date=end_date,
                employee_id=employee_id
            )
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
