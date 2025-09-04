"""
Implementação Mock do MotorcycleRepository - Infrastructure Layer

Simula operações de persistência para motocicletas em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de motocicletas
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4
from datetime import datetime
import asyncio

from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository


class MockMotorcycleRepository(MotorcycleRepository):
    """
    Implementação mock do repositório de motocicletas.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados em memória."""
        self._motorcycles: Dict[UUID, Motorcycle] = {}
        self._license_plate_index: Dict[str, UUID] = {}
        self._next_id = 1
        
        # Simular algumas motocicletas para desenvolvimento
        self._seed_data()
    
    def _seed_data(self):
        """Popula dados iniciais para desenvolvimento."""
        motorcycles_data = [
            {
                "license_plate": "MOT1A23",
                "brand": "Honda",
                "model": "CB 600F Hornet",
                "year": 2023,
                "color": "Vermelha",
                "price": 45000.00,
                "mileage": 5000,
                "fuel_type": "Gasolina",
                "engine": "600cc",
                "cylinder_capacity": 600,
                "motorcycle_type": "Street",
                "status": "Disponível",
                "description": "Naked esportiva, ágil e potente"
            },
            {
                "license_plate": "MOT2B45",
                "brand": "Yamaha",
                "model": "MT-07",
                "year": 2022,
                "color": "Azul",
                "price": 42000.00,
                "mileage": 12000,
                "fuel_type": "Gasolina",
                "engine": "689cc",
                "cylinder_capacity": 689,
                "motorcycle_type": "Naked",
                "status": "Disponível",
                "description": "Bicilíndrica versátil para uso urbano e estrada"
            },
            {
                "license_plate": "MOT3C67",
                "brand": "Kawasaki",
                "model": "Ninja 400",
                "year": 2021,
                "color": "Verde",
                "price": 35000.00,
                "mileage": 18000,
                "fuel_type": "Gasolina",
                "engine": "399cc",
                "cylinder_capacity": 399,
                "motorcycle_type": "Sport",
                "status": "Vendida",
                "description": "Esportiva de entrada ideal para iniciantes"
            }
        ]
        
        for data in motorcycles_data:
            motorcycle = Motorcycle.create_motorcycle(**data)
            self._motorcycles[motorcycle.id] = motorcycle
            self._license_plate_index[motorcycle.license_plate] = motorcycle.id
    
    async def save(self, motorcycle: Motorcycle) -> Motorcycle:
        """
        Salva uma motocicleta no repositório.
        
        Args:
            motorcycle: Motocicleta a ser salva
            
        Returns:
            Motocicleta salva com timestamps atualizados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Atualizar timestamp
        if motorcycle.id not in self._motorcycles:
            motorcycle.created_at = datetime.now()
        motorcycle.updated_at = datetime.now()
        
        # Salvar
        self._motorcycles[motorcycle.id] = motorcycle
        
        # Atualizar índice
        self._license_plate_index[motorcycle.license_plate] = motorcycle.id
        
        return motorcycle
    
    async def find_by_id(self, motorcycle_id: UUID) -> Optional[Motorcycle]:
        """
        Busca uma motocicleta por ID.
        
        Args:
            motorcycle_id: ID da motocicleta
            
        Returns:
            Motocicleta encontrada ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        return self._motorcycles.get(motorcycle_id)
    
    async def find_by_license_plate(self, license_plate: str) -> Optional[Motorcycle]:
        """
        Busca uma motocicleta por placa.
        
        Args:
            license_plate: Placa da motocicleta
            
        Returns:
            Motocicleta encontrada ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Normalizar placa (maiúscula e sem espaços)
        clean_plate = license_plate.upper().replace(" ", "").replace("-", "")
        
        motorcycle_id = self._license_plate_index.get(clean_plate)
        if motorcycle_id:
            return self._motorcycles.get(motorcycle_id)
        
        return None
    
    async def find_all(self) -> List[Motorcycle]:
        """
        Busca todas as motocicletas.
        
        Returns:
            Lista de todas as motocicletas
        """
        await asyncio.sleep(0.01)  # Simular latência
        return list(self._motorcycles.values())
    
    async def find_by_brand(self, brand: str) -> List[Motorcycle]:
        """
        Busca motocicletas por marca.
        
        Args:
            brand: Marca das motocicletas
            
        Returns:
            Lista de motocicletas da marca especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if motorcycle.brand.lower() == brand.lower()
        ]
    
    async def find_by_status(self, status: str) -> List[Motorcycle]:
        """
        Busca motocicletas por status.
        
        Args:
            status: Status das motocicletas
            
        Returns:
            Lista de motocicletas com o status especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if motorcycle.status == status
        ]
    
    async def find_by_type(self, motorcycle_type: str) -> List[Motorcycle]:
        """
        Busca motocicletas por tipo.
        
        Args:
            motorcycle_type: Tipo da motocicleta
            
        Returns:
            Lista de motocicletas do tipo especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if motorcycle.motorcycle_type.lower() == motorcycle_type.lower()
        ]
    
    async def find_by_price_range(self, min_price: float, max_price: float) -> List[Motorcycle]:
        """
        Busca motocicletas por faixa de preço.
        
        Args:
            min_price: Preço mínimo
            max_price: Preço máximo
            
        Returns:
            Lista de motocicletas na faixa de preço especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if min_price <= motorcycle.price <= max_price
        ]
    
    async def find_by_cylinder_capacity_range(self, min_cc: int, max_cc: int) -> List[Motorcycle]:
        """
        Busca motocicletas por faixa de cilindrada.
        
        Args:
            min_cc: Cilindrada mínima
            max_cc: Cilindrada máxima
            
        Returns:
            Lista de motocicletas na faixa de cilindrada especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if min_cc <= motorcycle.cylinder_capacity <= max_cc
        ]
    
    async def find_available(self) -> List[Motorcycle]:
        """
        Busca motocicletas disponíveis para venda.
        
        Returns:
            Lista de motocicletas disponíveis
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if motorcycle.status == "Disponível"
        ]
    
    async def search_motorcycles(self, search_term: str) -> List[Motorcycle]:
        """
        Busca motocicletas por termo de busca (marca, modelo, tipo).
        
        Args:
            search_term: Termo de busca
            
        Returns:
            Lista de motocicletas que correspondem ao termo
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        search_lower = search_term.lower()
        
        return [
            motorcycle for motorcycle in self._motorcycles.values()
            if (search_lower in motorcycle.brand.lower() or
                search_lower in motorcycle.model.lower() or
                search_lower in motorcycle.motorcycle_type.lower() or
                search_lower in motorcycle.color.lower() or
                search_lower in motorcycle.fuel_type.lower())
        ]
    
    async def find_with_filters(
        self,
        filters: Dict[str, Any],
        order_by: str = "created_at",
        order_direction: str = "desc",
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Motorcycle], int]:
        """
        Busca motocicletas com filtros e paginação.
        
        Args:
            filters: Filtros a aplicar
            order_by: Campo para ordenação
            order_direction: Direção da ordenação
            skip: Registros a pular
            limit: Limite de registros
            
        Returns:
            Tupla com lista de motocicletas e total
        """
        await asyncio.sleep(0.02)  # Simular latência de query complexa
        
        # Aplicar filtros
        filtered_motorcycles = list(self._motorcycles.values())
        
        if 'brand' in filters and filters['brand']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.brand.lower() == filters['brand'].lower()
            ]
        
        if 'model' in filters and filters['model']:
            model_filter = filters['model'].lower()
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if model_filter in motorcycle.model.lower()
            ]
        
        if 'status' in filters and filters['status']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.status == filters['status']
            ]
        
        if 'motorcycle_type' in filters and filters['motorcycle_type']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.motorcycle_type.lower() == filters['motorcycle_type'].lower()
            ]
        
        if 'fuel_type' in filters and filters['fuel_type']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.fuel_type == filters['fuel_type']
            ]
        
        if 'min_price' in filters and filters['min_price']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.price >= filters['min_price']
            ]
        
        if 'max_price' in filters and filters['max_price']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.price <= filters['max_price']
            ]
        
        if 'min_year' in filters and filters['min_year']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.year >= filters['min_year']
            ]
        
        if 'max_year' in filters and filters['max_year']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.year <= filters['max_year']
            ]
        
        if 'min_cylinder_capacity' in filters and filters['min_cylinder_capacity']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.cylinder_capacity >= filters['min_cylinder_capacity']
            ]
        
        if 'max_cylinder_capacity' in filters and filters['max_cylinder_capacity']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.cylinder_capacity <= filters['max_cylinder_capacity']
            ]
        
        if 'color' in filters and filters['color']:
            filtered_motorcycles = [
                motorcycle for motorcycle in filtered_motorcycles
                if motorcycle.color.lower() == filters['color'].lower()
            ]
        
        total = len(filtered_motorcycles)
        
        # Aplicar ordenação
        if order_by == "brand":
            filtered_motorcycles.sort(key=lambda m: m.brand, reverse=(order_direction == "desc"))
        elif order_by == "model":
            filtered_motorcycles.sort(key=lambda m: m.model, reverse=(order_direction == "desc"))
        elif order_by == "year":
            filtered_motorcycles.sort(key=lambda m: m.year, reverse=(order_direction == "desc"))
        elif order_by == "price":
            filtered_motorcycles.sort(key=lambda m: m.price, reverse=(order_direction == "desc"))
        elif order_by == "cylinder_capacity":
            filtered_motorcycles.sort(key=lambda m: m.cylinder_capacity, reverse=(order_direction == "desc"))
        elif order_by == "created_at":
            filtered_motorcycles.sort(key=lambda m: m.created_at, reverse=(order_direction == "desc"))
        elif order_by == "updated_at":
            filtered_motorcycles.sort(key=lambda m: m.updated_at, reverse=(order_direction == "desc"))
        
        # Aplicar paginação
        paginated_motorcycles = filtered_motorcycles[skip:skip + limit]
        
        return paginated_motorcycles, total
    
    async def count_all(self) -> int:
        """
        Conta total de motocicletas.
        
        Returns:
            Número total de motocicletas
        """
        await asyncio.sleep(0.01)  # Simular latência
        return len(self._motorcycles)
    
    async def count_by_status(self, status: str) -> int:
        """
        Conta motocicletas por status.
        
        Args:
            status: Status das motocicletas
            
        Returns:
            Número de motocicletas com o status especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return sum(
            1 for motorcycle in self._motorcycles.values()
            if motorcycle.status == status
        )
    
    async def count_by_brand(self, brand: str) -> int:
        """
        Conta motocicletas por marca.
        
        Args:
            brand: Marca das motocicletas
            
        Returns:
            Número de motocicletas da marca especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return sum(
            1 for motorcycle in self._motorcycles.values()
            if motorcycle.brand.lower() == brand.lower()
        )
    
    async def count_by_type(self, motorcycle_type: str) -> int:
        """
        Conta motocicletas por tipo.
        
        Args:
            motorcycle_type: Tipo das motocicletas
            
        Returns:
            Número de motocicletas do tipo especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return sum(
            1 for motorcycle in self._motorcycles.values()
            if motorcycle.motorcycle_type.lower() == motorcycle_type.lower()
        )
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas das motocicletas.
        
        Returns:
            Dicionário com estatísticas
        """
        await asyncio.sleep(0.05)  # Simular query complexa
        
        total_motorcycles = len(self._motorcycles)
        
        if total_motorcycles == 0:
            return {
                "total_motorcycles": 0,
                "available_motorcycles": 0,
                "sold_motorcycles": 0,
                "average_price": 0,
                "average_cylinder_capacity": 0,
                "motorcycles_by_brand": {},
                "motorcycles_by_type": {},
                "motorcycles_by_year": {}
            }
        
        # Contar por status
        available_motorcycles = sum(1 for m in self._motorcycles.values() if m.status == "Disponível")
        sold_motorcycles = sum(1 for m in self._motorcycles.values() if m.status == "Vendida")
        
        # Calcular médias
        total_price = sum(m.price for m in self._motorcycles.values())
        average_price = total_price / total_motorcycles
        
        total_cc = sum(m.cylinder_capacity for m in self._motorcycles.values())
        average_cc = total_cc / total_motorcycles
        
        # Distribuição por marca
        motorcycles_by_brand = {}
        for motorcycle in self._motorcycles.values():
            motorcycles_by_brand[motorcycle.brand] = motorcycles_by_brand.get(motorcycle.brand, 0) + 1
        
        # Distribuição por tipo
        motorcycles_by_type = {}
        for motorcycle in self._motorcycles.values():
            motorcycles_by_type[motorcycle.motorcycle_type] = motorcycles_by_type.get(motorcycle.motorcycle_type, 0) + 1
        
        # Distribuição por ano
        motorcycles_by_year = {}
        for motorcycle in self._motorcycles.values():
            motorcycles_by_year[motorcycle.year] = motorcycles_by_year.get(motorcycle.year, 0) + 1
        
        return {
            "total_motorcycles": total_motorcycles,
            "available_motorcycles": available_motorcycles,
            "sold_motorcycles": sold_motorcycles,
            "average_price": round(average_price, 2),
            "average_cylinder_capacity": round(average_cc, 0),
            "motorcycles_by_brand": motorcycles_by_brand,
            "motorcycles_by_type": motorcycles_by_type,
            "motorcycles_by_year": motorcycles_by_year
        }
    
    async def delete(self, motorcycle_id: UUID) -> bool:
        """
        Exclui uma motocicleta.
        
        Args:
            motorcycle_id: ID da motocicleta
            
        Returns:
            True se excluída com sucesso
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        if motorcycle_id not in self._motorcycles:
            return False
        
        motorcycle = self._motorcycles[motorcycle_id]
        
        # Remover do índice
        if motorcycle.license_plate in self._license_plate_index:
            del self._license_plate_index[motorcycle.license_plate]
        
        # Remover motocicleta
        del self._motorcycles[motorcycle_id]
        
        return True
    
    async def exists(self, motorcycle_id: UUID) -> bool:
        """
        Verifica se uma motocicleta existe.
        
        Args:
            motorcycle_id: ID da motocicleta
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return motorcycle_id in self._motorcycles
    
    async def license_plate_exists(self, license_plate: str) -> bool:
        """
        Verifica se uma placa já está em uso.
        
        Args:
            license_plate: Placa a verificar
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Normalizar placa
        clean_plate = license_plate.upper().replace(" ", "").replace("-", "")
        return clean_plate in self._license_plate_index
    
    async def bulk_update_status(self, motorcycle_ids: List[UUID], status: str) -> int:
        """
        Atualiza status de múltiplas motocicletas.
        
        Args:
            motorcycle_ids: Lista de IDs das motocicletas
            status: Novo status
            
        Returns:
            Número de motocicletas atualizadas
        """
        await asyncio.sleep(0.02)  # Simular operação em lote
        
        updated_count = 0
        
        for motorcycle_id in motorcycle_ids:
            if motorcycle_id in self._motorcycles:
                motorcycle = self._motorcycles[motorcycle_id]
                motorcycle.update_status(status)
                motorcycle.updated_at = datetime.now()
                updated_count += 1
        
        return updated_count
