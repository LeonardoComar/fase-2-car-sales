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

from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4
from datetime import datetime, date
import asyncio

from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository


class MockClientRepository(ClientRepository):
    """
    Implementação mock do repositório de clientes.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados em memória."""
        self._clients: Dict[UUID, Client] = {}
        self._email_index: Dict[str, UUID] = {}
        self._cpf_index: Dict[str, UUID] = {}
        self._next_id = 1
        
        # Simular alguns clientes para desenvolvimento
        self._seed_data()
    
    def _seed_data(self):
        """Popula dados iniciais para desenvolvimento."""
        clients_data = [
            {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "11987654321",
                "cpf": "12345678901",
                "birth_date": date(1985, 3, 15),
                "address": "Rua das Flores, 123",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234567",
                "status": "Ativo",
                "notes": "Cliente VIP, comprador frequente"
            },
            {
                "name": "Maria Santos",
                "email": "maria.santos@email.com",
                "phone": "11976543210",
                "cpf": "98765432109",
                "birth_date": date(1990, 7, 22),
                "address": "Av. Principal, 456",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "zip_code": "20123456",
                "status": "Ativo",
                "notes": "Interessada em carros esportivos"
            },
            {
                "name": "Carlos Oliveira",
                "email": "carlos.oliveira@email.com",
                "phone": "11965432109",
                "cpf": "11122233344",
                "birth_date": date(1975, 12, 8),
                "address": "Rua Comercial, 789",
                "city": "Belo Horizonte",
                "state": "MG",
                "zip_code": "30123456",
                "status": "Inativo",
                "notes": "Cliente antigo, última compra em 2020"
            }
        ]
        
        for data in clients_data:
            client = Client.create_client(**data)
            self._clients[client.id] = client
            self._email_index[client.email] = client.id
            self._cpf_index[client.cpf] = client.id
    
    async def save(self, client: Client) -> Client:
        """
        Salva um cliente no repositório.
        
        Args:
            client: Cliente a ser salvo
            
        Returns:
            Cliente salvo com timestamps atualizados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Atualizar timestamp
        if client.id not in self._clients:
            client.created_at = datetime.now()
        client.updated_at = datetime.now()
        
        # Salvar
        self._clients[client.id] = client
        
        # Atualizar índices
        self._email_index[client.email] = client.id
        self._cpf_index[client.cpf] = client.id
        
        return client
    
    async def find_by_id(self, client_id: UUID) -> Optional[Client]:
        """
        Busca um cliente por ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Cliente encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        return self._clients.get(client_id)
    
    async def find_by_email(self, email: str) -> Optional[Client]:
        """
        Busca um cliente por email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Cliente encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        client_id = self._email_index.get(email)
        if client_id:
            return self._clients.get(client_id)
        
        return None
    
    async def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente por CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Cliente encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Limpar CPF (remover pontos e hífens)
        clean_cpf = ''.join(filter(str.isdigit, cpf))
        
        client_id = self._cpf_index.get(clean_cpf)
        if client_id:
            return self._clients.get(client_id)
        
        return None
    
    async def find_all(self) -> List[Client]:
        """
        Busca todos os clientes.
        
        Returns:
            Lista de todos os clientes
        """
        await asyncio.sleep(0.01)  # Simular latência
        return list(self._clients.values())
    
    async def find_by_status(self, status: str) -> List[Client]:
        """
        Busca clientes por status.
        
        Args:
            status: Status dos clientes
            
        Returns:
            Lista de clientes com o status especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            client for client in self._clients.values()
            if client.status == status
        ]
    
    async def find_by_city(self, city: str) -> List[Client]:
        """
        Busca clientes por cidade.
        
        Args:
            city: Cidade dos clientes
            
        Returns:
            Lista de clientes da cidade especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            client for client in self._clients.values()
            if client.city and client.city.lower() == city.lower()
        ]
    
    async def find_by_state(self, state: str) -> List[Client]:
        """
        Busca clientes por estado.
        
        Args:
            state: Estado dos clientes
            
        Returns:
            Lista de clientes do estado especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            client for client in self._clients.values()
            if client.state and client.state.upper() == state.upper()
        ]
    
    async def search_by_name(self, name: str) -> List[Client]:
        """
        Busca clientes por nome (busca parcial).
        
        Args:
            name: Nome ou parte do nome
            
        Returns:
            Lista de clientes que contêm o nome especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        name_lower = name.lower()
        
        return [
            client for client in self._clients.values()
            if name_lower in client.name.lower()
        ]
    
    async def find_vip_clients(self) -> List[Client]:
        """
        Busca clientes VIP.
        
        Returns:
            Lista de clientes VIP
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            client for client in self._clients.values()
            if client.is_vip()
        ]
    
    async def find_by_age_range(self, min_age: int, max_age: int) -> List[Client]:
        """
        Busca clientes por faixa etária.
        
        Args:
            min_age: Idade mínima
            max_age: Idade máxima
            
        Returns:
            Lista de clientes na faixa etária especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            client for client in self._clients.values()
            if client.birth_date and min_age <= client.get_age() <= max_age
        ]
    
    async def find_with_filters(
        self,
        filters: Dict[str, Any],
        order_by: str = "name",
        order_direction: str = "asc",
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Client], int]:
        """
        Busca clientes com filtros e paginação.
        
        Args:
            filters: Filtros a aplicar
            order_by: Campo para ordenação
            order_direction: Direção da ordenação
            skip: Registros a pular
            limit: Limite de registros
            
        Returns:
            Tupla com lista de clientes e total
        """
        await asyncio.sleep(0.02)  # Simular latência de query complexa
        
        # Aplicar filtros
        filtered_clients = list(self._clients.values())
        
        if 'name' in filters and filters['name']:
            name_filter = filters['name'].lower()
            filtered_clients = [
                client for client in filtered_clients
                if name_filter in client.name.lower()
            ]
        
        if 'email' in filters and filters['email']:
            email_filter = filters['email'].lower()
            filtered_clients = [
                client for client in filtered_clients
                if email_filter in client.email.lower()
            ]
        
        if 'status' in filters and filters['status']:
            filtered_clients = [
                client for client in filtered_clients
                if client.status == filters['status']
            ]
        
        if 'city' in filters and filters['city']:
            city_filter = filters['city'].lower()
            filtered_clients = [
                client for client in filtered_clients
                if client.city and city_filter in client.city.lower()
            ]
        
        if 'state' in filters and filters['state']:
            state_filter = filters['state'].upper()
            filtered_clients = [
                client for client in filtered_clients
                if client.state and client.state.upper() == state_filter
            ]
        
        if 'min_age' in filters and filters['min_age']:
            filtered_clients = [
                client for client in filtered_clients
                if client.birth_date and client.get_age() >= filters['min_age']
            ]
        
        if 'max_age' in filters and filters['max_age']:
            filtered_clients = [
                client for client in filtered_clients
                if client.birth_date and client.get_age() <= filters['max_age']
            ]
        
        if 'is_vip' in filters and filters['is_vip'] is not None:
            filtered_clients = [
                client for client in filtered_clients
                if client.is_vip() == filters['is_vip']
            ]
        
        total = len(filtered_clients)
        
        # Aplicar ordenação
        if order_by == "name":
            filtered_clients.sort(key=lambda c: c.name, reverse=(order_direction == "desc"))
        elif order_by == "email":
            filtered_clients.sort(key=lambda c: c.email, reverse=(order_direction == "desc"))
        elif order_by == "created_at":
            filtered_clients.sort(key=lambda c: c.created_at, reverse=(order_direction == "desc"))
        elif order_by == "updated_at":
            filtered_clients.sort(key=lambda c: c.updated_at, reverse=(order_direction == "desc"))
        elif order_by == "status":
            filtered_clients.sort(key=lambda c: c.status, reverse=(order_direction == "desc"))
        elif order_by == "city":
            filtered_clients.sort(key=lambda c: c.city or "", reverse=(order_direction == "desc"))
        elif order_by == "age":
            filtered_clients.sort(
                key=lambda c: c.get_age() if c.birth_date else 0, 
                reverse=(order_direction == "desc")
            )
        
        # Aplicar paginação
        paginated_clients = filtered_clients[skip:skip + limit]
        
        return paginated_clients, total
    
    async def count_all(self) -> int:
        """
        Conta total de clientes.
        
        Returns:
            Número total de clientes
        """
        await asyncio.sleep(0.01)  # Simular latência
        return len(self._clients)
    
    async def count_by_status(self, status: str) -> int:
        """
        Conta clientes por status.
        
        Args:
            status: Status dos clientes
            
        Returns:
            Número de clientes com o status especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return sum(
            1 for client in self._clients.values()
            if client.status == status
        )
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas dos clientes.
        
        Returns:
            Dicionário com estatísticas
        """
        await asyncio.sleep(0.05)  # Simular query complexa
        
        total_clients = len(self._clients)
        
        if total_clients == 0:
            return {
                "total_clients": 0,
                "active_clients": 0,
                "inactive_clients": 0,
                "vip_clients": 0,
                "average_age": 0,
                "clients_by_state": {},
                "clients_by_city": {},
                "age_distribution": {}
            }
        
        # Contar por status
        active_clients = sum(1 for c in self._clients.values() if c.status == "Ativo")
        inactive_clients = total_clients - active_clients
        
        # Contar VIPs
        vip_clients = sum(1 for c in self._clients.values() if c.is_vip())
        
        # Calcular idade média
        ages = [c.get_age() for c in self._clients.values() if c.birth_date]
        average_age = sum(ages) / len(ages) if ages else 0
        
        # Distribuição por estado
        clients_by_state = {}
        for client in self._clients.values():
            if client.state:
                clients_by_state[client.state] = clients_by_state.get(client.state, 0) + 1
        
        # Distribuição por cidade
        clients_by_city = {}
        for client in self._clients.values():
            if client.city:
                clients_by_city[client.city] = clients_by_city.get(client.city, 0) + 1
        
        # Distribuição por faixa etária
        age_distribution = {"18-25": 0, "26-35": 0, "36-45": 0, "46-55": 0, "56+": 0}
        for client in self._clients.values():
            if client.birth_date:
                age = client.get_age()
                if age <= 25:
                    age_distribution["18-25"] += 1
                elif age <= 35:
                    age_distribution["26-35"] += 1
                elif age <= 45:
                    age_distribution["36-45"] += 1
                elif age <= 55:
                    age_distribution["46-55"] += 1
                else:
                    age_distribution["56+"] += 1
        
        return {
            "total_clients": total_clients,
            "active_clients": active_clients,
            "inactive_clients": inactive_clients,
            "vip_clients": vip_clients,
            "average_age": round(average_age, 1),
            "clients_by_state": clients_by_state,
            "clients_by_city": clients_by_city,
            "age_distribution": age_distribution
        }
    
    async def delete(self, client_id: UUID) -> bool:
        """
        Exclui um cliente.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            True se excluído com sucesso
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        if client_id not in self._clients:
            return False
        
        client = self._clients[client_id]
        
        # Remover dos índices
        if client.email in self._email_index:
            del self._email_index[client.email]
        
        if client.cpf in self._cpf_index:
            del self._cpf_index[client.cpf]
        
        # Remover cliente
        del self._clients[client_id]
        
        return True
    
    async def exists(self, client_id: UUID) -> bool:
        """
        Verifica se um cliente existe.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return client_id in self._clients
    
    async def bulk_update_status(self, client_ids: List[UUID], status: str) -> int:
        """
        Atualiza status de múltiplos clientes.
        
        Args:
            client_ids: Lista de IDs dos clientes
            status: Novo status
            
        Returns:
            Número de clientes atualizados
        """
        await asyncio.sleep(0.02)  # Simular operação em lote
        
        updated_count = 0
        
        for client_id in client_ids:
            if client_id in self._clients:
                client = self._clients[client_id]
                client.update_status(status)
                client.updated_at = datetime.now()
                updated_count += 1
        
        return updated_count
