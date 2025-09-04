"""
Implementação Mock do CarRepository - Infrastructure Layer

Simula operações de persistência para carros em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de carros
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import asyncio

from src.domain.entities.car import Car
from src.domain.ports.car_repository import CarRepository


class MockCarRepository(CarRepository):
    """
    Implementação mock do repositório de carros.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados em memória."""
        self._cars: Dict[int, Car] = {}
        self._license_plate_index: Dict[str, int] = {}
        self._next_id = 1
        
        # Simular alguns carros para desenvolvimento
        self._seed_data()
    
    def _seed_data(self):
        """Popula dados iniciais para desenvolvimento."""
        cars_data = [
            {
                "license_plate": "ABC1D23",
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2022,
                "color": "Branco",
                "price": 95000.00,
                "mileage": 15000,
                "fuel_type": "Flex",
                "transmission": "Automático",
                "engine": "1.8",
                "doors": 4,
                "status": "Ativo",
                "description": "Sedan compacto, econômico e confiável"
            },
            {
                "license_plate": "XYZ9W87",
                "brand": "Honda",
                "model": "Civic",
                "year": 2023,
                "color": "Preto",
                "price": 110000.00,
                "mileage": 8000,
                "fuel_type": "Flex",
                "transmission": "Manual",
                "engine": "2.0",
                "doors": 4,
                "status": "Ativo",
                "description": "Sedan esportivo com design moderno"
            },
            {
                "license_plate": "DEF4G56",
                "brand": "Volkswagen",
                "model": "Golf",
                "year": 2021,
                "color": "Azul",
                "price": 85000.00,
                "mileage": 25000,
                "fuel_type": "Gasolina",
                "transmission": "Automático",
                "engine": "1.4 Turbo",
                "doors": 5,
                "status": "Vendido",
                "description": "Hatch premium com tecnologia avançada"
            }
        ]
        
        for data in cars_data:
            # Convert the data to use create_complete_car method
            car_data = {
                "model": data["model"],
                "year": str(data["year"]),  # year should be string
                "mileage": data["mileage"],
                "fuel_type": data["fuel_type"],
                "color": data["color"],
                "city": "São Paulo",  # Default city
                "price": data["price"],
                "bodywork": "Sedan" if data["model"] in ["Corolla", "Civic"] else "Hatchback",
                "transmission": "Automatica" if data["transmission"] == "Automático" else "Manual",
                "additional_description": data["description"]
            }
            
            car = Car.create_complete_car(**car_data)
            # Generate auto-increment ID
            car_id = self._next_id
            self._next_id += 1
            
            car.id = car_id
            car.motor_vehicle.id = car_id
            
            self._cars[car_id] = car
            # Use license plate from data as an alternative index for now
            self._license_plate_index[data["license_plate"]] = car_id
    
    async def save(self, car: Car) -> Car:
        """
        Salva um carro no repositório.
        
        Args:
            car: Carro a ser salvo
            
        Returns:
            Carro salvo com timestamps atualizados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Atualizar timestamp
        if car.id not in self._cars:
            car.created_at = datetime.now()
        car.updated_at = datetime.now()
        
        # Salvar
        self._cars[car.id] = car
        
        # Atualizar índice
        self._license_plate_index[car.license_plate] = car.id
        
        return car
    
    async def find_by_id(self, car_id: int) -> Optional[Car]:
        """
        Busca um carro por ID.
        
        Args:
            car_id: ID do carro
            
        Returns:
            Carro encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        return self._cars.get(car_id)
    
    async def find_by_license_plate(self, license_plate: str) -> Optional[Car]:
        """
        Busca um carro por placa.
        
        Args:
            license_plate: Placa do carro
            
        Returns:
            Carro encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Normalizar placa (maiúscula e sem espaços)
        clean_plate = license_plate.upper().replace(" ", "").replace("-", "")
        
        car_id = self._license_plate_index.get(clean_plate)
        if car_id:
            return self._cars.get(car_id)
        
        return None
    
    async def find_all(self) -> List[Car]:
        """
        Busca todos os carros.
        
        Returns:
            Lista de todos os carros
        """
        await asyncio.sleep(0.01)  # Simular latência
        return list(self._cars.values())
    
    async def find_by_brand(self, brand: str) -> List[Car]:
        """
        Busca carros por marca.
        
        Args:
            brand: Marca dos carros
            
        Returns:
            Lista de carros da marca especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            car for car in self._cars.values()
            if car.brand.lower() == brand.lower()
        ]
    
    async def find_by_status(self, status: str) -> List[Car]:
        """
        Busca carros por status.
        
        Args:
            status: Status dos carros
            
        Returns:
            Lista de carros com o status especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            car for car in self._cars.values()
            if car.status == status
        ]
    
    async def find_by_price_range(self, min_price: float, max_price: float) -> List[Car]:
        """
        Busca carros por faixa de preço.
        
        Args:
            min_price: Preço mínimo
            max_price: Preço máximo
            
        Returns:
            Lista de carros na faixa de preço especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            car for car in self._cars.values()
            if min_price <= car.price <= max_price
        ]
    
    async def find_by_year_range(self, min_year: int, max_year: int) -> List[Car]:
        """
        Busca carros por faixa de ano.
        
        Args:
            min_year: Ano mínimo
            max_year: Ano máximo
            
        Returns:
            Lista de carros na faixa de ano especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            car for car in self._cars.values()
            if min_year <= car.year <= max_year
        ]
    
    async def find_available(self) -> List[Car]:
        """
        Busca carros disponíveis para venda.
        
        Returns:
            Lista de carros disponíveis
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return [
            car for car in self._cars.values()
            if car.status == "Disponível"
        ]
    
    async def search_cars(
        self,
        model: str = None,
        year: str = None,
        bodywork: str = None,
        transmission: str = None,
        fuel_type: str = None,
        city: str = None,
        min_price: float = None,
        max_price: float = None,
        status: str = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Car]:
        """
        Busca carros por critérios específicos.
        
        Args:
            model: Modelo do carro
            year: Ano do carro
            bodywork: Tipo de carroceria
            transmission: Tipo de transmissão
            fuel_type: Tipo de combustível
            city: Cidade
            min_price: Preço mínimo
            max_price: Preço máximo
            status: Status do veículo
            skip: Número de registros para pular
            limit: Limite de registros
            
        Returns:
            Lista de carros que correspondem aos critérios
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        cars = list(self._cars.values())
        
        # Aplicar filtros
        if model:
            cars = [car for car in cars if model.lower() in car.motor_vehicle.model.lower()]
        
        if year:
            cars = [car for car in cars if car.motor_vehicle.year == year]
        
        if bodywork:
            cars = [car for car in cars if car.bodywork.lower() == bodywork.lower()]
        
        if transmission:
            cars = [car for car in cars if car.transmission.lower() == transmission.lower()]
        
        if fuel_type:
            cars = [car for car in cars if car.motor_vehicle.fuel_type.lower() == fuel_type.lower()]
        
        if city:
            cars = [car for car in cars if car.motor_vehicle.city.lower() == city.lower()]
        
        if status:
            cars = [car for car in cars if car.motor_vehicle.status.lower() == status.lower()]
        
        if min_price:
            cars = [car for car in cars if float(car.motor_vehicle.price) >= min_price]
        
        if max_price:
            cars = [car for car in cars if float(car.motor_vehicle.price) <= max_price]
        
        # Aplicar paginação
        return cars[skip:skip + limit]

    async def find_with_filters(
        self,
        filters: Dict[str, Any],
        order_by: str = "created_at",
        order_direction: str = "desc",
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Car], int]:
        """
        Busca carros com filtros e paginação.
        
        Args:
            filters: Filtros a aplicar
            order_by: Campo para ordenação
            order_direction: Direção da ordenação
            skip: Registros a pular
            limit: Limite de registros
            
        Returns:
            Tupla com lista de carros e total
        """
        await asyncio.sleep(0.02)  # Simular latência de query complexa
        
        # Aplicar filtros
        filtered_cars = list(self._cars.values())
        
        if 'brand' in filters and filters['brand']:
            filtered_cars = [
                car for car in filtered_cars
                if car.brand.lower() == filters['brand'].lower()
            ]
        
        if 'model' in filters and filters['model']:
            model_filter = filters['model'].lower()
            filtered_cars = [
                car for car in filtered_cars
                if model_filter in car.model.lower()
            ]
        
        if 'status' in filters and filters['status']:
            filtered_cars = [
                car for car in filtered_cars
                if car.status == filters['status']
            ]
        
        if 'fuel_type' in filters and filters['fuel_type']:
            filtered_cars = [
                car for car in filtered_cars
                if car.fuel_type == filters['fuel_type']
            ]
        
        if 'transmission' in filters and filters['transmission']:
            filtered_cars = [
                car for car in filtered_cars
                if car.transmission == filters['transmission']
            ]
        
        if 'min_price' in filters and filters['min_price']:
            filtered_cars = [
                car for car in filtered_cars
                if car.price >= filters['min_price']
            ]
        
        if 'max_price' in filters and filters['max_price']:
            filtered_cars = [
                car for car in filtered_cars
                if car.price <= filters['max_price']
            ]
        
        if 'min_year' in filters and filters['min_year']:
            filtered_cars = [
                car for car in filtered_cars
                if car.year >= filters['min_year']
            ]
        
        if 'max_year' in filters and filters['max_year']:
            filtered_cars = [
                car for car in filtered_cars
                if car.year <= filters['max_year']
            ]
        
        if 'min_mileage' in filters and filters['min_mileage']:
            filtered_cars = [
                car for car in filtered_cars
                if car.mileage >= filters['min_mileage']
            ]
        
        if 'max_mileage' in filters and filters['max_mileage']:
            filtered_cars = [
                car for car in filtered_cars
                if car.mileage <= filters['max_mileage']
            ]
        
        if 'color' in filters and filters['color']:
            filtered_cars = [
                car for car in filtered_cars
                if car.color.lower() == filters['color'].lower()
            ]
        
        total = len(filtered_cars)
        
        # Aplicar ordenação
        if order_by == "brand":
            filtered_cars.sort(key=lambda c: c.brand, reverse=(order_direction == "desc"))
        elif order_by == "model":
            filtered_cars.sort(key=lambda c: c.model, reverse=(order_direction == "desc"))
        elif order_by == "year":
            filtered_cars.sort(key=lambda c: c.year, reverse=(order_direction == "desc"))
        elif order_by == "price":
            filtered_cars.sort(key=lambda c: c.price, reverse=(order_direction == "desc"))
        elif order_by == "mileage":
            filtered_cars.sort(key=lambda c: c.mileage, reverse=(order_direction == "desc"))
        elif order_by == "created_at":
            filtered_cars.sort(key=lambda c: c.created_at, reverse=(order_direction == "desc"))
        elif order_by == "updated_at":
            filtered_cars.sort(key=lambda c: c.updated_at, reverse=(order_direction == "desc"))
        
        # Aplicar paginação
        paginated_cars = filtered_cars[skip:skip + limit]
        
        return paginated_cars, total
    
    async def count_all(self) -> int:
        """
        Conta total de carros.
        
        Returns:
            Número total de carros
        """
        await asyncio.sleep(0.01)  # Simular latência
        return len(self._cars)
    
    async def count_by_status(self, status: str) -> int:
        """
        Conta carros por status.
        
        Args:
            status: Status dos carros
            
        Returns:
            Número de carros com o status especificado
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return sum(
            1 for car in self._cars.values()
            if car.status == status
        )
    
    async def count_by_brand(self, brand: str) -> int:
        """
        Conta carros por marca.
        
        Args:
            brand: Marca dos carros
            
        Returns:
            Número de carros da marca especificada
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        return sum(
            1 for car in self._cars.values()
            if car.brand.lower() == brand.lower()
        )
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas dos carros.
        
        Returns:
            Dicionário com estatísticas
        """
        await asyncio.sleep(0.05)  # Simular query complexa
        
        total_cars = len(self._cars)
        
        if total_cars == 0:
            return {
                "total_cars": 0,
                "available_cars": 0,
                "sold_cars": 0,
                "average_price": 0,
                "average_mileage": 0,
                "cars_by_brand": {},
                "cars_by_fuel_type": {},
                "cars_by_year": {}
            }
        
        # Contar por status
        available_cars = sum(1 for c in self._cars.values() if c.status == "Disponível")
        sold_cars = sum(1 for c in self._cars.values() if c.status == "Vendido")
        
        # Calcular médias
        total_price = sum(c.price for c in self._cars.values())
        average_price = total_price / total_cars
        
        total_mileage = sum(c.mileage for c in self._cars.values())
        average_mileage = total_mileage / total_cars
        
        # Distribuição por marca
        cars_by_brand = {}
        for car in self._cars.values():
            cars_by_brand[car.brand] = cars_by_brand.get(car.brand, 0) + 1
        
        # Distribuição por tipo de combustível
        cars_by_fuel_type = {}
        for car in self._cars.values():
            cars_by_fuel_type[car.fuel_type] = cars_by_fuel_type.get(car.fuel_type, 0) + 1
        
        # Distribuição por ano
        cars_by_year = {}
        for car in self._cars.values():
            cars_by_year[car.year] = cars_by_year.get(car.year, 0) + 1
        
        return {
            "total_cars": total_cars,
            "available_cars": available_cars,
            "sold_cars": sold_cars,
            "average_price": round(average_price, 2),
            "average_mileage": round(average_mileage, 0),
            "cars_by_brand": cars_by_brand,
            "cars_by_fuel_type": cars_by_fuel_type,
            "cars_by_year": cars_by_year
        }
    
    async def delete(self, car_id: int) -> bool:
        """
        Exclui um carro.
        
        Args:
            car_id: ID do carro
            
        Returns:
            True se excluído com sucesso
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        if car_id not in self._cars:
            return False
        
        car = self._cars[car_id]
        
        # Remover do índice
        if car.license_plate in self._license_plate_index:
            del self._license_plate_index[car.license_plate]
        
        # Remover carro
        del self._cars[car_id]
        
        return True
    
    async def exists(self, car_id: int) -> bool:
        """
        Verifica se um carro existe.
        
        Args:
            car_id: ID do carro
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return car_id in self._cars
    
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
    
    async def bulk_update_status(self, car_ids: List[int], status: str) -> int:
        """
        Atualiza status de múltiplos carros.
        
        Args:
            car_ids: Lista de IDs dos carros
            status: Novo status
            
        Returns:
            Número de carros atualizados
        """
        await asyncio.sleep(0.02)  # Simular operação em lote
        
        updated_count = 0
        
        for car_id in car_ids:
            if car_id in self._cars:
                car = self._cars[car_id]
                car.update_status(status)
                car.updated_at = datetime.now()
                updated_count += 1
        
        return updated_count

    async def update(self, car: Car) -> Car:
        """
        Atualiza um carro existente.
        
        Args:
            car: Carro com dados atualizados
            
        Returns:
            Carro atualizado
            
        Raises:
            ValueError: Se o carro não existir
        """
        await asyncio.sleep(0.01)
        
        if car.id not in self._cars:
            raise ValueError(f"Carro com ID {car.id} não encontrado")
        
        # Verificar se a placa já existe para outro carro
        existing_car_id = self._license_plate_index.get(car.license_plate)
        if existing_car_id and existing_car_id != car.id:
            raise ValueError(f"Placa {car.license_plate} já está em uso")
        
        # Atualizar índice de placa se necessário
        old_car = self._cars[car.id]
        if old_car.license_plate != car.license_plate:
            del self._license_plate_index[old_car.license_plate]
            self._license_plate_index[car.license_plate] = car.id
        
        # Atualizar carro
        car.updated_at = datetime.now()
        self._cars[car.id] = car
        
        return car

    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[Car]:
        """
        Busca carros por critérios específicos.
        
        Args:
            criteria: Dicionário com critérios de busca
            
        Returns:
            Lista de carros que atendem aos critérios
        """
        await asyncio.sleep(0.01)
        
        cars = list(self._cars.values())
        
        for key, value in criteria.items():
            if key == "brand" and value:
                cars = [car for car in cars if car.brand.lower() == value.lower()]
            elif key == "model" and value:
                cars = [car for car in cars if car.model.lower() == value.lower()]
            elif key == "year" and value:
                cars = [car for car in cars if car.year == value]
            elif key == "color" and value:
                cars = [car for car in cars if car.color.lower() == value.lower()]
            elif key == "status" and value:
                cars = [car for car in cars if car.status == value]
            elif key == "min_price" and value:
                cars = [car for car in cars if car.price >= value]
            elif key == "max_price" and value:
                cars = [car for car in cars if car.price <= value]
            elif key == "min_year" and value:
                cars = [car for car in cars if car.year >= value]
            elif key == "max_year" and value:
                cars = [car for car in cars if car.year <= value]
        
        return cars

    async def count_by_criteria(self, criteria: Dict[str, Any]) -> int:
        """
        Conta carros por critérios específicos.
        
        Args:
            criteria: Dicionário com critérios de busca
            
        Returns:
            Número de carros que atendem aos critérios
        """
        cars = await self.find_by_criteria(criteria)
        return len(cars)
