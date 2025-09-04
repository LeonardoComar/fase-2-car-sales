from typing import List
from uuid import UUID

from fastapi import HTTPException, status

from src.application.dtos.employee_dto import (
    EmployeeCreateDto, EmployeeUpdateDto, EmployeeResponseDto, 
    EmployeeSearchDto, EmployeeStatusUpdateDto, EmployeePromotionDto
)
from src.application.use_cases import (
    CreateEmployeeUseCase, GetEmployeeByIdUseCase, UpdateEmployeeUseCase,
    DeleteEmployeeUseCase, ListEmployeesUseCase, PromoteEmployeeUseCase,
    UpdateEmployeeStatusUseCase
)
from src.adapters.rest.presenters.employee_presenter import EmployeePresenter
from src.domain.exceptions import ValidationError, BusinessRuleError, NotFoundError, DuplicateError


class EmployeeController:
    """
    Controller para operações de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por gerenciar requisições HTTP relacionadas a funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende das abstrações dos use cases, não das implementações.
    """
    
    def __init__(
        self,
        create_employee_use_case: CreateEmployeeUseCase,
        get_employee_by_id_use_case: GetEmployeeByIdUseCase,
        update_employee_use_case: UpdateEmployeeUseCase,
        delete_employee_use_case: DeleteEmployeeUseCase,
        list_employees_use_case: ListEmployeesUseCase,
        promote_employee_use_case: PromoteEmployeeUseCase,
        update_employee_status_use_case: UpdateEmployeeStatusUseCase,
        employee_presenter: EmployeePresenter
    ):
        self.create_employee_use_case = create_employee_use_case
        self.get_employee_by_id_use_case = get_employee_by_id_use_case
        self.update_employee_use_case = update_employee_use_case
        self.delete_employee_use_case = delete_employee_use_case
        self.list_employees_use_case = list_employees_use_case
        self.promote_employee_use_case = promote_employee_use_case
        self.update_employee_status_use_case = update_employee_status_use_case
        self.employee_presenter = employee_presenter
    
    async def create_employee(self, employee_data: EmployeeCreateDto) -> dict:
        """
        Cria um novo funcionário.
        
        Args:
            employee_data: Dados do funcionário a ser criado
            
        Returns:
            dict: Funcionário criado formatado pelo presenter
            
        Raises:
            HTTPException: Se houver erro na criação
        """
        try:
            employee_response = await self.create_employee_use_case.execute(employee_data)
            return self.employee_presenter.present_employee(employee_response)
            
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {str(e)}"
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Regra de negócio violada: {str(e)}"
            )
        except DuplicateError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Conflito: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_employee_by_id(self, employee_id: UUID) -> dict:
        """
        Busca funcionário por ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            dict: Funcionário encontrado formatado pelo presenter
            
        Raises:
            HTTPException: Se funcionário não for encontrado
        """
        try:
            employee_response = await self.get_employee_by_id_use_case.execute(employee_id)
            return self.employee_presenter.present_employee(employee_response)
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def update_employee(self, employee_id: UUID, employee_data: EmployeeUpdateDto) -> dict:
        """
        Atualiza um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser atualizado
            employee_data: Dados para atualização
            
        Returns:
            dict: Funcionário atualizado formatado pelo presenter
            
        Raises:
            HTTPException: Se houver erro na atualização
        """
        try:
            employee_response = await self.update_employee_use_case.execute(employee_id, employee_data)
            return self.employee_presenter.present_employee(employee_response)
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {str(e)}"
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Regra de negócio violada: {str(e)}"
            )
        except DuplicateError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Conflito: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def delete_employee(self, employee_id: UUID) -> dict:
        """
        Exclui um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser excluído
            
        Returns:
            dict: Mensagem de sucesso
            
        Raises:
            HTTPException: Se houver erro na exclusão
        """
        try:
            await self.delete_employee_use_case.execute(employee_id)
            return self.employee_presenter.present_deletion_success("Funcionário")
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Não é possível excluir: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def list_employees(self, search_criteria: EmployeeSearchDto) -> dict:
        """
        Lista funcionários com filtros.
        
        Args:
            search_criteria: Critérios de busca
            
        Returns:
            dict: Lista de funcionários formatada pelo presenter
            
        Raises:
            HTTPException: Se houver erro na busca
        """
        try:
            employees_response = await self.list_employees_use_case.execute(search_criteria)
            return self.employee_presenter.present_employee_list(employees_response)
            
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Critérios de busca inválidos: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def promote_employee(self, employee_id: UUID, promotion_data: EmployeePromotionDto) -> dict:
        """
        Promove um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser promovido
            promotion_data: Dados da promoção
            
        Returns:
            dict: Funcionário promovido formatado pelo presenter
            
        Raises:
            HTTPException: Se houver erro na promoção
        """
        try:
            employee_response = await self.promote_employee_use_case.execute(employee_id, promotion_data)
            return self.employee_presenter.present_promotion_success(employee_response)
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados de promoção inválidos: {str(e)}"
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Promoção não permitida: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def update_employee_status(self, employee_id: UUID, status_data: EmployeeStatusUpdateDto) -> dict:
        """
        Atualiza status de um funcionário.
        
        Args:
            employee_id: ID do funcionário
            status_data: Dados de atualização de status
            
        Returns:
            dict: Funcionário com status atualizado formatado pelo presenter
            
        Raises:
            HTTPException: Se houver erro na atualização
        """
        try:
            employee_response = await self.update_employee_status_use_case.execute(employee_id, status_data)
            return self.employee_presenter.present_status_update_success(employee_response)
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados de status inválidos: {str(e)}"
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Mudança de status não permitida: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_employee_by_cpf(self, cpf: str) -> dict:
        """
        Busca funcionário por CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            dict: Funcionário encontrado formatado pelo presenter
            
        Raises:
            HTTPException: Se funcionário não for encontrado
        """
        try:
            # Buscar usando filtro
            search_criteria = EmployeeSearchDto(cpf=cpf, limit=1)
            employees_response = await self.list_employees_use_case.execute(search_criteria)
            
            if not employees_response:
                raise NotFoundError("Funcionário", f"CPF {cpf}")
            
            return self.employee_presenter.present_employee(employees_response[0])
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CPF inválido: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_employees_by_department(self, department: str) -> dict:
        """
        Lista funcionários por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            dict: Lista de funcionários do departamento
            
        Raises:
            HTTPException: Se houver erro na busca
        """
        try:
            search_criteria = EmployeeSearchDto(department=department, active_only=True)
            employees_response = await self.list_employees_use_case.execute(search_criteria)
            return self.employee_presenter.present_department_employees(employees_response, department)
            
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parâmetros inválidos: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_managers(self) -> dict:
        """
        Lista todos os gerentes.
        
        Returns:
            dict: Lista de gerentes
            
        Raises:
            HTTPException: Se houver erro na busca
        """
        try:
            search_criteria = EmployeeSearchDto(managers_only=True, active_only=True)
            managers_response = await self.list_employees_use_case.execute(search_criteria)
            return self.employee_presenter.present_managers_list(managers_response)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
