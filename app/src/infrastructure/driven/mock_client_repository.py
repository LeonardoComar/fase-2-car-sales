"""
Implementação Mock do ClientRepository - Infrastructure Layer

Simula operações de persistência para clientes em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de clientes
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

from src.domain.entities.client import Client
from src.domain.entities.address import Address
from src.domain.ports.client_repository import ClientRepository


class MockClientRepository(ClientRepository):
    """
    Implementação mock do repositório de clientes.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório mock com dados em memória."""
        self._clients: Dict[int, Client] = {}
        self._addresses: Dict[int, Address] = {}
        self._next_client_id = 1
        self._next_address_id = 1
        
        # Dados iniciais para demonstração
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Inicializa dados mock para demonstração."""
        # Endereços mock
        address1 = Address(
            id=1,
            street="Rua das Flores, 123",
            city="São Paulo",
            state="SP",
            zip_code="01234-567",
            country="Brasil",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._addresses[1] = address1
        
        # Clientes mock
        client1 = Client(
            id=1,
            name="João Silva",
            email="joao.silva@email.com",
            phone="(11) 99999-9999",
            cpf="123.456.789-00",
            address_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._clients[1] = client1
        
        client2 = Client(
            id=2,
            name="Maria Santos",
            email="maria.santos@email.com",
            phone="(11) 88888-8888",
            cpf="987.654.321-00",
            address_id=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._clients[2] = client2
        
        self._next_client_id = 3
        self._next_address_id = 2
    
    async def create(self, client: Client, address: Optional[Address] = None) -> Client:
        """
        Cria um novo cliente no repositório mock.
        
        Args:
            client: Dados do cliente a ser criado
            address: Dados do endereço (opcional)
            
        Returns:
            Client: O cliente criado com ID gerado
        """
        # Simular latência de rede
        await asyncio.sleep(0.1)
        
        # Verificar se email já existe
        existing_email = await self.find_by_email(client.email)
        if existing_email:
            raise ValueError(f"Email '{client.email}' já está em uso")
        
        # Verificar se CPF já existe
        existing_cpf = await self.find_by_cpf(client.cpf)
        if existing_cpf:
            raise ValueError(f"CPF '{client.cpf}' já está em uso")
        
        # Criar endereço se fornecido
        address_id = None
        if address:
            address.id = self._next_address_id
            address.created_at = datetime.now()
            address.updated_at = datetime.now()
            self._addresses[self._next_address_id] = address
            address_id = self._next_address_id
            self._next_address_id += 1
        
        # Criar cliente
        client.id = self._next_client_id
        client.address_id = address_id
        client.created_at = datetime.now()
        client.updated_at = datetime.now()
        
        self._clients[self._next_client_id] = client
        self._next_client_id += 1
        
        return client
    
    async def find_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca um cliente pelo ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Optional[Client]: O cliente encontrado ou None
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        return self._clients.get(client_id)
    
    async def find_by_email(self, email: str) -> Optional[Client]:
        """
        Busca um cliente pelo email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Optional[Client]: O cliente encontrado ou None
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        email_lower = email.lower()
        for client in self._clients.values():
            if client.email.lower() == email_lower:
                return client
        return None
    
    async def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente pelo CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Optional[Client]: O cliente encontrado ou None
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        for client in self._clients.values():
            if client.cpf == cpf:
                return client
        return None
    
    async def update(self, client_id: int, client: Client, address: Optional[Address] = None) -> Optional[Client]:
        """
        Atualiza um cliente existente.
        
        Args:
            client_id: ID do cliente
            client: Dados atualizados do cliente
            address: Dados atualizados do endereço (opcional)
            
        Returns:
            Optional[Client]: O cliente atualizado ou None se não encontrado
        """
        # Simular latência de rede
        await asyncio.sleep(0.1)
        
        if client_id not in self._clients:
            return None
        
        existing_client = self._clients[client_id]
        
        # Verificar conflitos de email (se email foi alterado)
        if client.email != existing_client.email:
            existing_email = await self.find_by_email(client.email)
            if existing_email:
                raise ValueError(f"Email '{client.email}' já está em uso")
        
        # Verificar conflitos de CPF (se CPF foi alterado)
        if client.cpf != existing_client.cpf:
            existing_cpf = await self.find_by_cpf(client.cpf)
            if existing_cpf:
                raise ValueError(f"CPF '{client.cpf}' já está em uso")
        
        # Atualizar endereço se fornecido
        if address:
            if existing_client.address_id:
                # Atualizar endereço existente
                address.id = existing_client.address_id
                address.updated_at = datetime.now()
                # Manter created_at original se existir
                if existing_client.address_id in self._addresses:
                    address.created_at = self._addresses[existing_client.address_id].created_at
                else:
                    address.created_at = datetime.now()
                self._addresses[existing_client.address_id] = address
            else:
                # Criar novo endereço
                address.id = self._next_address_id
                address.created_at = datetime.now()
                address.updated_at = datetime.now()
                self._addresses[self._next_address_id] = address
                client.address_id = self._next_address_id
                self._next_address_id += 1
        
        # Atualizar cliente
        client.id = client_id
        client.updated_at = datetime.now()
        # Manter created_at original
        client.created_at = existing_client.created_at
        
        self._clients[client_id] = client
        
        return client
    
    async def delete(self, client_id: int) -> bool:
        """
        Remove um cliente do banco de dados.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        # Simular latência de rede
        await asyncio.sleep(0.1)
        
        if client_id in self._clients:
            client = self._clients[client_id]
            
            # Remover endereço associado se existir
            if client.address_id and client.address_id in self._addresses:
                del self._addresses[client.address_id]
            
            # Remover cliente
            del self._clients[client_id]
            return True
        
        return False
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca todos os clientes com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Client]: Lista de clientes encontrados
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        all_clients = list(self._clients.values())
        # Ordenar por ID para consistência
        all_clients.sort(key=lambda x: x.id or 0)
        
        # Aplicar paginação
        end_index = skip + limit
        return all_clients[skip:end_index]
    
    async def find_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca clientes por nome (busca parcial).
        
        Args:
            name: Nome ou parte do nome para buscar
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Client]: Lista de clientes encontrados
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        name_lower = name.lower()
        matching_clients = []
        
        for client in self._clients.values():
            if name_lower in client.name.lower():
                matching_clients.append(client)
        
        # Ordenar por ID para consistência
        matching_clients.sort(key=lambda x: x.id or 0)
        
        # Aplicar paginação
        end_index = skip + limit
        return matching_clients[skip:end_index]
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """
        Busca um endereço pelo ID (método auxiliar).
        
        Args:
            address_id: ID do endereço
            
        Returns:
            Optional[Address]: O endereço encontrado ou None
        """
        return self._addresses.get(address_id)
