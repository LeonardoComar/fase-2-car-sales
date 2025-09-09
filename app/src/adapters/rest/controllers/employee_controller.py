"""
Controller de Funcionários - Adapter Layer

Responsável por coordenar as operações HTTP relacionadas a funcionários.
Faz a ponte entre a camada de apresentação (routers) e a camada de aplicação (use cases).

Aplicando princípios SOLID:
- SRP: Responsável apenas pela coordenação de operações de funcionários
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para operações de funcionários
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import Optional, List
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.application.use_cases.employees.create_employee_use_case import CreateEmployeeUseCase
from src.application.use_cases.employees.get_employee_use_case import GetEmployeeUseCase
from src.application.use_cases.employees.list_employees_use_case import ListEmployeesUseCase
from src.application.use_cases.employees.update_employee_use_case import UpdateEmployeeUseCase
from src.application.use_cases.employees.delete_employee_use_case import DeleteEmployeeUseCase
from src.application.use_cases.employees.update_employee_status_use_case import UpdateEmployeeStatusUseCase
from src.application.dtos.employee_dto import CreateEmployeeDto, UpdateEmployeeDto, EmployeeResponseDto, EmployeeListDto


class EmployeeController:
    """
    Controller para operações de funcionários.
    
    Coordena a execução de use cases e formatação de respostas HTTP.
    """
    
    def __init__(self,
                 create_employee_use_case: CreateEmployeeUseCase,
                 get_employee_use_case: GetEmployeeUseCase,
                 list_employees_use_case: ListEmployeesUseCase,
                 update_employee_use_case: UpdateEmployeeUseCase,
                 delete_employee_use_case: DeleteEmployeeUseCase,
                 update_employee_status_use_case: UpdateEmployeeStatusUseCase):
        """
        Inicializa o controller com os use cases necessários.
        
        Args:
            create_employee_use_case: Use case para criar funcionários
            get_employee_use_case: Use case para buscar funcionários
            list_employees_use_case: Use case para listar funcionários
            update_employee_use_case: Use case para atualizar funcionários
            delete_employee_use_case: Use case para excluir funcionários
            update_employee_status_use_case: Use case para atualizar status
        """
        self._create_employee_use_case = create_employee_use_case
        self._get_employee_use_case = get_employee_use_case
        self._list_employees_use_case = list_employees_use_case
        self._update_employee_use_case = update_employee_use_case
        self._delete_employee_use_case = delete_employee_use_case
        self._update_employee_status_use_case = update_employee_status_use_case
    
    async def create_employee(self, employee_data: CreateEmployeeDto) -> JSONResponse:
        """
        Cria um novo funcionário.
        
        Args:
            employee_data: Dados para criação do funcionário
            
        Returns:
            JSONResponse: Resposta com dados do funcionário criado
            
        Raises:
            HTTPException: Se houver erro na criação
        """
        try:
            employee = await self._create_employee_use_case.execute(employee_data)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Funcionário criado com sucesso",
                    "data": employee.dict()
                }
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
    
    async def get_employee(self, employee_id: int) -> JSONResponse:
        """
        Busca um funcionário por ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            JSONResponse: Resposta com dados do funcionário
            
        Raises:
            HTTPException: Se funcionário não encontrado ou erro na busca
        """
        try:
            employee = await self._get_employee_use_case.execute(employee_id)
            
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funcionário não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Funcionário encontrado com sucesso",
                    "data": employee.dict()
                }
            )
            
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
    
    async def list_employees(self, skip: int = 0, limit: int = 100,
                           name: Optional[str] = None, cpf: Optional[str] = None,
                           employee_status: Optional[str] = None) -> JSONResponse:
        """
        Lista funcionários com filtros opcionais.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            name: Nome ou parte do nome para filtrar (opcional)
            cpf: CPF exato para buscar (opcional)
            employee_status: Status para filtrar (opcional)
            
        Returns:
            JSONResponse: Resposta com lista de funcionários
            
        Raises:
            HTTPException: Se houver erro na listagem
        """
        try:
            employees = await self._list_employees_use_case.execute(
                skip=skip, limit=limit, name=name, cpf=cpf, status=employee_status
            )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Funcionários listados com sucesso",
                    "data": {
                        "employees": [emp.dict() for emp in employees],
                        "total": len(employees),
                        "skip": skip,
                        "limit": limit
                    }
                }
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
    
    async def update_employee(self, employee_id: int, employee_data: UpdateEmployeeDto) -> JSONResponse:
        """
        Atualiza um funcionário existente.
        
        Args:
            employee_id: ID do funcionário
            employee_data: Dados para atualização
            
        Returns:
            JSONResponse: Resposta com dados do funcionário atualizado
            
        Raises:
            HTTPException: Se funcionário não encontrado ou erro na atualização
        """
        try:
            employee = await self._update_employee_use_case.execute(employee_id, employee_data)
            
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funcionário não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Funcionário atualizado com sucesso",
                    "data": employee.dict()
                }
            )
            
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
    
    async def delete_employee(self, employee_id: int) -> JSONResponse:
        """
        Exclui um funcionário.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            JSONResponse: Resposta de confirmação
            
        Raises:
            HTTPException: Se funcionário não encontrado ou erro na exclusão
        """
        try:
            success = await self._delete_employee_use_case.execute(employee_id)
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funcionário não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Funcionário excluído com sucesso"
                }
            )
            
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
    
    async def activate_employee(self, employee_id: int) -> JSONResponse:
        """
        Ativa um funcionário (define status como 'Ativo').
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            JSONResponse: Resposta com dados do funcionário ativado
            
        Raises:
            HTTPException: Se funcionário não encontrado ou erro na ativação
        """
        try:
            employee = await self._update_employee_status_use_case.execute(employee_id, "Ativo")
            
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funcionário não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Funcionário ativado com sucesso",
                    "data": employee.dict()
                }
            )
            
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
    
    async def deactivate_employee(self, employee_id: int) -> JSONResponse:
        """
        Desativa um funcionário (define status como 'Inativo').
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            JSONResponse: Resposta com dados do funcionário desativado
            
        Raises:
            HTTPException: Se funcionário não encontrado ou erro na desativação
        """
        try:
            employee = await self._update_employee_status_use_case.execute(employee_id, "Inativo")
            
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funcionário não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Funcionário desativado com sucesso",
                    "data": employee.dict()
                }
            )
            
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )
