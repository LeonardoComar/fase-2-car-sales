"""
Controller de Clientes - Adapter Layer

Responsável por coordenar as operações HTTP relacionadas a clientes.
Faz a ponte entre a camada de apresentação (routers) e a camada de aplicação (use cases).

Aplicando princípios SOLID:
- SRP: Responsável apenas pela coordenação de operações de clientes
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para operações de clientes
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import Optional, List
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.application.use_cases.clients.create_client_use_case import CreateClientUseCase
from src.application.use_cases.clients.get_client_by_id_use_case import GetClientByIdUseCase
from src.application.use_cases.clients.get_client_by_cpf_use_case import GetClientByCpfUseCase
from src.application.use_cases.clients.update_client_use_case import UpdateClientUseCase
from src.application.use_cases.clients.delete_client_use_case import DeleteClientUseCase
from src.application.use_cases.clients.list_clients_use_case import ListClientsUseCase
from src.application.use_cases.clients.update_client_status_use_case import UpdateClientStatusUseCase
from src.application.dtos.client_dto import CreateClientDto, UpdateClientDto, ClientResponseDto, ClientListDto
from src.adapters.rest.presenters.client_presenter import ClientPresenter


class ClientController:
    """
    Controller para operações de clientes.
    
    Coordena a execução de use cases e formatação de respostas HTTP.
    """
    
    def __init__(self,
                 create_use_case: CreateClientUseCase,
                 get_by_id_use_case: GetClientByIdUseCase,
                 get_by_cpf_use_case: GetClientByCpfUseCase,
                 update_use_case: UpdateClientUseCase,
                 delete_use_case: DeleteClientUseCase,
                 list_use_case: ListClientsUseCase,
                 update_status_use_case: UpdateClientStatusUseCase,
                 client_presenter: ClientPresenter):
        """
        Inicializa o controller com os use cases necessários.
        
        Args:
            create_use_case: Use case para criar clientes
            get_by_id_use_case: Use case para buscar clientes por ID
            get_by_cpf_use_case: Use case para buscar clientes por CPF
            update_use_case: Use case para atualizar clientes
            delete_use_case: Use case para excluir clientes
            list_use_case: Use case para listar clientes
            update_status_use_case: Use case para atualizar status (não implementado)
            client_presenter: Presenter para formatação de respostas
        """
        self._create_use_case = create_use_case
        self._get_by_id_use_case = get_by_id_use_case
        self._get_by_cpf_use_case = get_by_cpf_use_case
        self._update_use_case = update_use_case
        self._delete_use_case = delete_use_case
        self._list_use_case = list_use_case
        self._update_status_use_case = update_status_use_case
        self._presenter = client_presenter
    
    async def create_client(self, client_data: CreateClientDto) -> JSONResponse:
        """
        Cria um novo cliente.
        
        Args:
            client_data: Dados para criação do cliente
            
        Returns:
            JSONResponse: Resposta com dados do cliente criado
            
        Raises:
            HTTPException: Se houver erro na criação
        """
        try:
            client = await self._create_use_case.execute(client_data)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=self._presenter.present_success(
                    "Cliente criado com sucesso",
                    self._presenter.present_client(client)
                )
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
    
    async def get_client_by_id(self, client_id: int) -> JSONResponse:
        """
        Busca um cliente por ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            JSONResponse: Resposta com dados do cliente
            
        Raises:
            HTTPException: Se cliente não encontrado ou erro interno
        """
        try:
            client = await self._get_by_id_use_case.execute(client_id)
            
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=self._presenter.present_success(
                    "Cliente encontrado",
                    self._presenter.present_client(client)
                )
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
    
    async def get_client_by_cpf(self, cpf: str) -> JSONResponse:
        """
        Busca um cliente por CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            JSONResponse: Resposta com dados do cliente
            
        Raises:
            HTTPException: Se cliente não encontrado ou erro interno
        """
        try:
            client = await self._get_by_cpf_use_case.execute(cpf)
            
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=self._presenter.present_success(
                    "Cliente encontrado",
                    self._presenter.present_client(client)
                )
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
    
    async def update_client(self, client_id: int, client_data: UpdateClientDto) -> JSONResponse:
        """
        Atualiza um cliente existente.
        
        Args:
            client_id: ID do cliente
            client_data: Dados para atualização
            
        Returns:
            JSONResponse: Resposta com dados do cliente atualizado
            
        Raises:
            HTTPException: Se cliente não encontrado ou erro interno
        """
        try:
            client = await self._update_use_case.execute(client_id, client_data)
            
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=self._presenter.present_success(
                    "Cliente atualizado com sucesso",
                    self._presenter.present_client(client)
                )
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
    
    async def delete_client(self, client_id: int) -> JSONResponse:
        """
        Remove um cliente.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            JSONResponse: Resposta de confirmação
            
        Raises:
            HTTPException: Se cliente não encontrado ou erro interno
        """
        try:
            deleted = await self._delete_use_case.execute(client_id)
            
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado"
                )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=self._presenter.present_success("Cliente removido com sucesso")
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
    
    async def list_clients(self, skip: int = 0, limit: int = 100,
                          name: Optional[str] = None, cpf: Optional[str] = None) -> JSONResponse:
        """
        Lista clientes com filtros e paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros
            name: Filtro por nome (opcional)
            cpf: Filtro por CPF (opcional)
            
        Returns:
            JSONResponse: Lista de clientes
            
        Raises:
            HTTPException: Se erro interno
        """
        try:
            clients = await self._list_use_case.execute(skip, limit, name, cpf)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=self._presenter.present_success(
                    "Lista de clientes recuperada com sucesso",
                    self._presenter.present_client_list(clients)
                )
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
