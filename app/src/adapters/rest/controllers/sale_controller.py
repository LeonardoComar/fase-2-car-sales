from typing import Optional
from uuid import UUID
from datetime import date

from src.application.use_cases.sales import (
    CreateSaleUseCase,
    GetSaleByIdUseCase,
    UpdateSaleUseCase,
    DeleteSaleUseCase,
    ListSalesUseCase,
    UpdateSaleStatusUseCase,
    GetSalesStatisticsUseCase,
)
from src.application.dtos.sale_dto import (
    SaleCreateDto, SaleUpdateDto, SaleSearchDto, SaleStatusUpdateDto
)
from src.adapters.rest.presenters.sale_presenter import SalePresenter
from src.domain.exceptions import ValidationError


class SaleController:
    """
    Controlador REST para operações de vendas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por coordenar operações HTTP de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende de abstrações (use cases) e não de implementações concretas.
    """
    
    def __init__(
        self,
        create_sale_use_case: CreateSaleUseCase,
        get_sale_by_id_use_case: GetSaleByIdUseCase,
        update_sale_use_case: UpdateSaleUseCase,
        delete_sale_use_case: DeleteSaleUseCase,
        list_sales_use_case: ListSalesUseCase,
        update_sale_status_use_case: UpdateSaleStatusUseCase,
        get_sales_statistics_use_case: GetSalesStatisticsUseCase,
        sale_presenter: SalePresenter
    ):
        self._create_sale_use_case = create_sale_use_case
        self._get_sale_by_id_use_case = get_sale_by_id_use_case
        self._update_sale_use_case = update_sale_use_case
        self._delete_sale_use_case = delete_sale_use_case
        self._list_sales_use_case = list_sales_use_case
        self._update_sale_status_use_case = update_sale_status_use_case
        self._get_sales_statistics_use_case = get_sales_statistics_use_case
        self._presenter = sale_presenter
    
    async def create_sale(self, sale_data: SaleCreateDto) -> tuple[dict, int]:
        """
        Cria uma nova venda.
        
        Args:
            sale_data: Dados da venda a ser criada
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            sale_dto = await self._create_sale_use_case.execute(sale_data)
            return self._presenter.present_sale_created(sale_dto), 201
        
        except ValidationError as e:
            return self._presenter.present_validation_error(str(e)), 400
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def get_sale_by_id(self, sale_id: UUID) -> tuple[dict, int]:
        """
        Busca uma venda por ID.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            sale_dto = await self._get_sale_by_id_use_case.execute(sale_id)
            
            if not sale_dto:
                return self._presenter.present_sale_not_found(), 404
            
            return self._presenter.present_sale(sale_dto), 200
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def update_sale(self, sale_id: UUID, sale_data: SaleUpdateDto) -> tuple[dict, int]:
        """
        Atualiza uma venda.
        
        Args:
            sale_id: ID da venda
            sale_data: Dados de atualização
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            sale_dto = await self._update_sale_use_case.execute(sale_id, sale_data)
            
            if not sale_dto:
                return self._presenter.present_sale_not_found(), 404
            
            return self._presenter.present_sale_updated(sale_dto), 200
        
        except ValidationError as e:
            return self._presenter.present_business_error(str(e)), 400
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def delete_sale(self, sale_id: UUID) -> tuple[dict, int]:
        """
        Exclui uma venda.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            deleted = await self._delete_sale_use_case.execute(sale_id)
            
            if not deleted:
                return self._presenter.present_sale_not_found(), 404
            
            return self._presenter.present_sale_deleted(), 200
        
        except ValidationError as e:
            return self._presenter.present_business_error(str(e)), 400
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def list_sales(self, search_criteria: SaleSearchDto) -> tuple[dict, int]:
        """
        Lista vendas com critérios de busca.
        
        Args:
            search_criteria: Critérios de busca
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            sales_dto = await self._list_sales_use_case.execute(search_criteria)
            return self._presenter.present_sale_list(sales_dto), 200
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def update_sale_status(self, sale_id: UUID, status_data: SaleStatusUpdateDto) -> tuple[dict, int]:
        """
        Atualiza o status de uma venda.
        
        Args:
            sale_id: ID da venda
            status_data: Dados do novo status
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            sale_dto = await self._update_sale_status_use_case.execute(sale_id, status_data)
            
            if not sale_dto:
                return self._presenter.present_sale_not_found(), 404
            
            return self._presenter.present_sale_status_updated(sale_dto), 200
        
        except ValidationError as e:
            return self._presenter.present_business_error(str(e)), 400
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def get_sales_by_client(self, client_id: UUID, search_criteria: SaleSearchDto) -> tuple[dict, int]:
        """
        Busca vendas por cliente.
        
        Args:
            client_id: ID do cliente
            search_criteria: Critérios de busca
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            # Adicionar filtro por cliente
            search_criteria.client_id = client_id
            sales_dto = await self._list_sales_use_case.execute(search_criteria)
            return self._presenter.present_sales_by_client(sales_dto, str(client_id)), 200
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def get_sales_by_employee(self, employee_id: UUID, search_criteria: SaleSearchDto) -> tuple[dict, int]:
        """
        Busca vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            search_criteria: Critérios de busca
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            # Adicionar filtro por funcionário
            search_criteria.employee_id = employee_id
            sales_dto = await self._list_sales_use_case.execute(search_criteria)
            return self._presenter.present_sales_by_employee(sales_dto, str(employee_id)), 200
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
    
    async def get_sales_statistics(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> tuple[dict, int]:
        """
        Busca estatísticas de vendas.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            tuple[dict, int]: Resposta formatada e código HTTP
        """
        try:
            stats_dto = await self._get_sales_statistics_use_case.execute(start_date, end_date)
            return self._presenter.present_sales_statistics(stats_dto), 200
        
        except Exception as e:
            return {"error": "Erro interno do servidor"}, 500
