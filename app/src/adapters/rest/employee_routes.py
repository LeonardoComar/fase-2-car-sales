from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.application.dtos.employee_dto import (
    EmployeeCreateDto, EmployeeUpdateDto, EmployeeSearchDto,
    EmployeeStatusUpdateDto, EmployeePromotionDto
)
from src.adapters.rest.controllers.employee_controller import EmployeeController
from src.adapters.rest.dependencies import get_employee_controller


# Criar router para funcionários
employee_router = APIRouter(
    tags=["Employees"],
    responses={
        404: {"description": "Funcionário não encontrado"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)


@employee_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar funcionário",
    description="Cria um novo funcionário no sistema"
)
async def create_employee(
    employee_data: EmployeeCreateDto,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Cria um novo funcionário.
    
    - **name**: Nome completo do funcionário
    - **email**: Email corporativo
    - **phone**: Telefone para contato
    - **cpf**: CPF válido brasileiro
    - **birth_date**: Data de nascimento
    - **position**: Cargo do funcionário
    - **department**: Departamento onde trabalha
    - **salary**: Salário em reais
    - **hire_date**: Data de contratação
    - **manager_id**: ID do gerente (opcional)
    - **employee_id**: ID interno da empresa (opcional)
    """
    result = await controller.create_employee(employee_data)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@employee_router.get(
    "/{employee_id}",
    summary="Buscar funcionário por ID",
    description="Busca um funcionário específico pelo ID"
)
async def get_employee_by_id(
    employee_id: UUID,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Busca funcionário por ID.
    
    Retorna todos os dados do funcionário incluindo:
    - Informações pessoais
    - Dados de emprego
    - Endereço
    - Contato de emergência
    - Atributos calculados
    """
    result = await controller.get_employee_by_id(employee_id)
    return JSONResponse(content=result)


@employee_router.put(
    "/{employee_id}",
    summary="Atualizar funcionário",
    description="Atualiza dados de um funcionário existente"
)
async def update_employee(
    employee_id: UUID,
    employee_data: EmployeeUpdateDto,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Atualiza um funcionário existente.
    
    Permite atualização parcial - apenas os campos fornecidos serão atualizados.
    Validações de negócio são aplicadas conforme as regras de RH.
    """
    result = await controller.update_employee(employee_id, employee_data)
    return JSONResponse(content=result)


@employee_router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Excluir funcionário",
    description="Exclui um funcionário do sistema"
)
async def delete_employee(
    employee_id: UUID,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Exclui um funcionário.
    
    **Restrições:**
    - Funcionário não pode ter subordinados
    - Funcionário não pode ter vendas associadas
    - Funcionário não pode ter transações pendentes
    """
    result = await controller.delete_employee(employee_id)
    return JSONResponse(content=result)


@employee_router.get(
    "",
    summary="Listar funcionários",
    description="Lista funcionários com filtros avançados e paginação"
)
async def list_employees(
    # Filtros de texto
    name: Optional[str] = Query(None, description="Nome do funcionário (busca parcial)"),
    email: Optional[str] = Query(None, description="Email do funcionário (busca parcial)"),
    phone: Optional[str] = Query(None, description="Telefone do funcionário"),
    cpf: Optional[str] = Query(None, description="CPF do funcionário"),
    position: Optional[str] = Query(None, description="Cargo do funcionário (busca parcial)"),
    department: Optional[str] = Query(None, description="Departamento"),
    employee_id: Optional[str] = Query(None, description="ID interno do funcionário"),
    
    # Filtros de localização
    city: Optional[str] = Query(None, description="Cidade"),
    state: Optional[str] = Query(None, description="Estado (UF)"),
    zip_code: Optional[str] = Query(None, description="CEP"),
    
    # Filtros hierárquicos
    manager_id: Optional[UUID] = Query(None, description="ID do gerente"),
    
    # Filtros de status
    status: Optional[str] = Query(None, description="Status do funcionário"),
    active_only: Optional[bool] = Query(None, description="Apenas funcionários ativos"),
    
    # Filtros de salário
    min_salary: Optional[float] = Query(None, description="Salário mínimo"),
    max_salary: Optional[float] = Query(None, description="Salário máximo"),
    
    # Filtros de tempo de serviço
    min_years_service: Optional[int] = Query(None, description="Anos mínimos de serviço"),
    max_years_service: Optional[int] = Query(None, description="Anos máximos de serviço"),
    
    # Filtros especiais
    managers_only: Optional[bool] = Query(None, description="Apenas gerentes"),
    
    # Paginação
    limit: Optional[int] = Query(50, description="Limite de resultados", le=1000),
    offset: Optional[int] = Query(0, description="Deslocamento para paginação", ge=0),
    
    # Ordenação
    order_by: Optional[str] = Query("name", description="Campo para ordenação"),
    order_direction: Optional[str] = Query("asc", description="Direção da ordenação"),
    
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Lista funcionários com filtros avançados.
    
    **Filtros disponíveis:**
    - Por dados pessoais (nome, email, CPF, telefone)
    - Por dados de emprego (cargo, departamento, gerente)
    - Por localização (cidade, estado, CEP)
    - Por status (ativo, inativo, suspenso, etc.)
    - Por faixa salarial
    - Por tempo de serviço
    - Apenas gerentes
    
    **Recursos:**
    - Paginação com limit/offset
    - Ordenação por qualquer campo
    - Busca parcial em campos de texto
    """
    search_criteria = EmployeeSearchDto(
        name=name,
        email=email,
        phone=phone,
        cpf=cpf,
        position=position,
        department=department,
        employee_id=employee_id,
        city=city,
        state=state,
        zip_code=zip_code,
        manager_id=manager_id,
        status=status,
        active_only=active_only,
        min_salary=min_salary,
        max_salary=max_salary,
        min_years_service=min_years_service,
        max_years_service=max_years_service,
        managers_only=managers_only,
        limit=limit,
        offset=offset,
        order_by=order_by,
        order_direction=order_direction
    )
    
    result = await controller.list_employees(search_criteria)
    return JSONResponse(content=result)


@employee_router.post(
    "/{employee_id}/promote",
    summary="Promover funcionário",
    description="Promove um funcionário para nova posição com aumento salarial"
)
async def promote_employee(
    employee_id: UUID,
    promotion_data: EmployeePromotionDto,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Promove um funcionário.
    
    **Regras de promoção:**
    - Funcionário deve estar ativo
    - Deve ter pelo menos 6 meses na empresa
    - Novo salário deve ser maior que o atual
    - Aumento não pode exceder 100% em uma única promoção
    - Nova posição deve ser diferente da atual
    
    **Dados necessários:**
    - **new_position**: Nova posição/cargo
    - **new_salary**: Novo salário (deve ser maior)
    - **new_department**: Novo departamento (opcional)
    - **notes**: Observações sobre a promoção (opcional)
    """
    result = await controller.promote_employee(employee_id, promotion_data)
    return JSONResponse(content=result)


@employee_router.patch(
    "/{employee_id}/status",
    summary="Atualizar status do funcionário",
    description="Atualiza o status de um funcionário"
)
async def update_employee_status(
    employee_id: UUID,
    status_data: EmployeeStatusUpdateDto,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Atualiza status do funcionário.
    
    **Status disponíveis:**
    - **active**: Funcionário ativo
    - **inactive**: Funcionário inativo
    - **suspended**: Funcionário suspenso
    - **terminated**: Funcionário terminado
    - **on_leave**: Funcionário em licença
    
    **Regras de transição:**
    - Funcionários com subordinados têm restrições especiais
    - Funcionários terminados requerem processo especial para reativação
    - Transições são validadas conforme regras de RH
    """
    result = await controller.update_employee_status(employee_id, status_data)
    return JSONResponse(content=result)


@employee_router.get(
    "/search/cpf/{cpf}",
    summary="Buscar funcionário por CPF",
    description="Busca um funcionário específico pelo CPF"
)
async def get_employee_by_cpf(
    cpf: str,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Busca funcionário por CPF.
    
    Aceita CPF com ou sem formatação (pontos e traços).
    """
    result = await controller.get_employee_by_cpf(cpf)
    return JSONResponse(content=result)


@employee_router.get(
    "/department/{department}",
    summary="Listar funcionários por departamento",
    description="Lista todos os funcionários de um departamento específico"
)
async def get_employees_by_department(
    department: str,
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Lista funcionários por departamento.
    
    Retorna estatísticas do departamento incluindo:
    - Número total de funcionários
    - Funcionários ativos
    - Número de gerentes
    - Folha de pagamento total
    - Salário médio
    - Tempo médio de serviço
    """
    result = await controller.get_employees_by_department(department)
    return JSONResponse(content=result)


@employee_router.get(
    "/managers",
    summary="Listar gerentes",
    description="Lista todos os gerentes ativos do sistema"
)
async def get_managers(
    controller: EmployeeController = Depends(get_employee_controller)
) -> JSONResponse:
    """
    Lista todos os gerentes.
    
    Retorna:
    - Lista completa de gerentes
    - Gerentes agrupados por departamento
    - Estatísticas de gerência
    """
    result = await controller.get_managers()
    return JSONResponse(content=result)
