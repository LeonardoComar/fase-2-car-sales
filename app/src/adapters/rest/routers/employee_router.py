"""
Router de Funcionários - Adapter Layer

Define as rotas HTTP para operações relacionadas a funcionários.
Faz a ponte entre requisições HTTP e o controller de funcionários.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelo roteamento de funcionários
- OCP: Extensível para novas rotas sem modificar existentes
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para rotas de funcionários
- DIP: Depende de abstrações (controller) não de implementações
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, status
from fastapi.responses import JSONResponse

from src.adapters.rest.controllers.employee_controller import EmployeeController
from src.adapters.rest.dependencies import get_employee_controller
from src.application.dtos.employee_dto import CreateEmployeeDto, UpdateEmployeeDto
from src.adapters.rest.auth_dependencies import (
    get_current_user,
    get_current_admin_user
)
from src.domain.entities.user import User


# Criar roteador para funcionários
employee_router = APIRouter()


@employee_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar funcionário",
    description="Cria um novo funcionário no sistema. Requer autenticação: Administrador",
    response_description="Funcionário criado com sucesso"
)
async def create_employee(
    employee_data: CreateEmployeeDto,
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Cria um novo funcionário no sistema.
    
    - **name**: Nome completo do funcionário
    - **email**: Email único do funcionário  
    - **phone**: Telefone do funcionário (opcional)
    - **cpf**: CPF único do funcionário
    - **address**: Dados do endereço (opcional)
    
    O funcionário é criado com status "Ativo" por padrão.
    Requer autenticação: Administrador
    """
    return await controller.create_employee(employee_data)


@employee_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar funcionários",
    description="Lista funcionários com filtros e paginação. Requer autenticação: Administrador",
    response_description="Lista de funcionários"
)
async def list_employees(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros para retornar"),
    name: Optional[str] = Query(None, description="Buscar por nome (busca parcial)"),
    cpf: Optional[str] = Query(None, description="Buscar por CPF exato"),
    status: Optional[str] = Query(None, pattern="^(Ativo|Inativo)$", description="Filtrar por status"),
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Lista funcionários com opções de busca e paginação.
    
    ### Parâmetros de busca (mutuamente exclusivos):
    - **name**: Busca funcionários cujo nome contenha o termo especificado
    - **cpf**: Busca funcionário com CPF exato
    
    ### Parâmetros de filtro:
    - **status**: Filtra funcionários por status (Ativo/Inativo)
    
    ### Parâmetros de paginação:
    - **skip**: Número de registros para pular (padrão: 0)
    - **limit**: Número máximo de registros para retornar (padrão: 100, máximo: 500)
    
    **Nota**: Os parâmetros name e cpf não podem ser usados simultaneamente.
    Requer autenticação: Administrador
    """
    return await controller.list_employees(skip=skip, limit=limit, name=name, cpf=cpf, employee_status=status)


@employee_router.get(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar funcionário",
    description="Busca um funcionário específico pelo ID. Requer autenticação: Administrador",
    response_description="Dados do funcionário"
)
async def get_employee(
    employee_id: int = Path(..., gt=0, description="ID do funcionário"),
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Busca um funcionário específico pelo ID.
    
    - **employee_id**: ID único do funcionário
    
    Retorna todos os dados do funcionário incluindo endereço se cadastrado.
    Requer autenticação: Administrador
    """
    return await controller.get_employee(employee_id)


@employee_router.put(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar funcionário",
    description="Atualiza os dados de um funcionário existente. Requer autenticação: Administrador",
    response_description="Funcionário atualizado"
)
async def update_employee(
    employee_data: UpdateEmployeeDto,
    employee_id: int = Path(..., gt=0, description="ID do funcionário"),
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Atualiza os dados de um funcionário existente.
    
    - **employee_id**: ID único do funcionário
    - **name**: Nome completo do funcionário (opcional)
    - **email**: Email único do funcionário (opcional)
    - **phone**: Telefone do funcionário (opcional)
    - **cpf**: CPF único do funcionário (opcional)
    - **status**: Status do funcionário - Ativo/Inativo (opcional)
    - **address**: Dados do endereço (opcional)
    
    Apenas os campos fornecidos serão atualizados.
    Requer autenticação: Administrador
    """
    return await controller.update_employee(employee_id, employee_data)


@employee_router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Excluir funcionário",
    description="Remove um funcionário do sistema. Requer autenticação: Administrador",
    response_description="Funcionário excluído"
)
async def delete_employee(
    employee_id: int = Path(..., gt=0, description="ID do funcionário"),
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Remove um funcionário do sistema.
    
    - **employee_id**: ID único do funcionário a ser removido
    
    **Atenção**: Esta operação é irreversível. O funcionário será
    permanentemente removido do banco de dados.
    Requer autenticação: Administrador
    """
    return await controller.delete_employee(employee_id)


@employee_router.patch(
    "/{employee_id}/activate",
    status_code=status.HTTP_200_OK,
    summary="Ativar funcionário",
    description="Ativa um funcionário (define status como 'Ativo'). Requer autenticação: Administrador",
    response_description="Funcionário ativado"
)
async def activate_employee(
    employee_id: int = Path(..., gt=0, description="ID do funcionário"),
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Ativa um funcionário (define status como 'Ativo').
    
    - **employee_id**: ID único do funcionário
    
    Endpoint de conveniência para ativar funcionários rapidamente.
    Requer autenticação: Administrador
    """
    return await controller.activate_employee(employee_id)


@employee_router.patch(
    "/{employee_id}/deactivate", 
    status_code=status.HTTP_200_OK,
    summary="Desativar funcionário",
    description="Desativa um funcionário (define status como 'Inativo'). Requer autenticação: Administrador",
    response_description="Funcionário desativado"
)
async def deactivate_employee(
    employee_id: int = Path(..., gt=0, description="ID do funcionário"),
    controller: EmployeeController = Depends(get_employee_controller),
    current_user: User = Depends(get_current_admin_user)
) -> JSONResponse:
    """
    Desativa um funcionário (define status como 'Inativo').
    
    - **employee_id**: ID único do funcionário
    
    Endpoint de conveniência para desativar funcionários rapidamente.
    Requer autenticação: Administrador
    """
    return await controller.deactivate_employee(employee_id)
