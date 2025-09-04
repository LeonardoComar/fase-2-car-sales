from src.application.dtos.car_dto import CarResponseDto, CarListResponseDto, CarSummaryDto
from src.domain.entities.car import Car


class CarPresenter:
    """
    Presenter para formatação de dados de carro.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela apresentação dos dados de carro.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberto para extensão, fechado para modificação.
    """
    
    @staticmethod
    def present_car(car: Car) -> dict:
        """
        Apresenta os dados de um carro.
        
        Args:
            car: Entidade de carro
            
        Returns:
            dict: Dados formatados do carro
        """
        return {
            "id": car.id,
            "model": car.motor_vehicle.model if car.motor_vehicle else "",
            "year": car.motor_vehicle.year if car.motor_vehicle else "",
            "bodywork": car.bodywork,
            "transmission": car.transmission,
            "price": float(car.motor_vehicle.price) if car.motor_vehicle else 0,
            "city": car.motor_vehicle.city if car.motor_vehicle else "",
            "status": car.motor_vehicle.status if car.motor_vehicle else "",
            "mileage": car.motor_vehicle.mileage if car.motor_vehicle else 0,
            "fuel_type": car.motor_vehicle.fuel_type if car.motor_vehicle else "",
            "color": car.motor_vehicle.color if car.motor_vehicle else "",
            "additional_description": car.motor_vehicle.additional_description if car.motor_vehicle else None,
            "created_at": car.motor_vehicle.created_at.isoformat() if car.motor_vehicle and car.motor_vehicle.created_at else None,
            "updated_at": car.updated_at.isoformat() if car.updated_at else None
        }
    
    @staticmethod
    def present_car_list(car_list_response: CarListResponseDto) -> dict:
        """
        Apresenta uma lista de carros.
        
        Args:
            car_list_response: DTO com lista de carros
            
        Returns:
            dict: Lista formatada de carros
        """
        return {
            "cars": [
                {
                    "id": car.id,
                    "model": car.model,
                    "year": car.year,
                    "bodywork": car.bodywork,
                    "transmission": car.transmission,
                    "price": float(car.price),
                    "city": car.city,
                    "status": car.status,
                    "mileage": car.mileage,
                    "fuel_type": car.fuel_type,
                    "color": car.color
                }
                for car in car_list_response.cars
            ],
            "total": car_list_response.total,
            "skip": car_list_response.skip,
            "limit": car_list_response.limit
        }
    
    @staticmethod
    def present(car_response: CarResponseDto) -> CarResponseDto:
        """
        Apresenta os dados do carro.
        
        Args:
            car_response: DTO com dados do carro
            
        Returns:
            CarResponseDto: DTO formatado para apresentação
        """
        # Por enquanto apenas retorna o DTO, mas pode ser extendido
        # para formatação específica, ocultação de campos sensíveis, etc.
        return car_response
    
    @staticmethod
    def present_list(car_list_response: CarListResponseDto) -> CarListResponseDto:
        """
        Apresenta uma lista de carros.
        
        Args:
            car_list_response: DTO com lista de carros
            
        Returns:
            CarListResponseDto: DTO formatado para apresentação
        """
        return car_list_response
    
    @staticmethod
    def present_summary_list(car_summaries: list[CarSummaryDto]) -> list[CarSummaryDto]:
        """
        Apresenta uma lista de resumos de carros.
        
        Args:
            car_summaries: Lista de DTOs de resumo
            
        Returns:
            list[CarSummaryDto]: Lista formatada para apresentação
        """
        return car_summaries
    
    @staticmethod
    def format_price(price: float) -> str:
        """
        Formata o preço para apresentação.
        
        Args:
            price: Preço do carro
            
        Returns:
            str: Preço formatado
        """
        return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    @staticmethod
    def format_mileage(mileage: int) -> str:
        """
        Formata a quilometragem para apresentação.
        
        Args:
            mileage: Quilometragem do carro
            
        Returns:
            str: Quilometragem formatada
        """
        return f"{mileage:,} km".replace(",", ".")
    
    @staticmethod
    def get_transmission_display(transmission: str) -> str:
        """
        Retorna o nome de exibição da transmissão.
        
        Args:
            transmission: Tipo de transmissão
            
        Returns:
            str: Nome de exibição
        """
        transmission_map = {
            "Manual": "Manual",
            "Automatica": "Automática",
            "Automatizada": "Automatizada",
            "CVT": "CVT"
        }
        return transmission_map.get(transmission, transmission)
    
    @staticmethod
    def get_bodywork_display(bodywork: str) -> str:
        """
        Retorna o nome de exibição da carroceria.
        
        Args:
            bodywork: Tipo de carroceria
            
        Returns:
            str: Nome de exibição
        """
        bodywork_map = {
            "Sedan": "Sedan",
            "Hatchback": "Hatchback",
            "SUV": "SUV",
            "Coupe": "Cupê",
            "Conversivel": "Conversível",
            "Station Wagon": "Perua",
            "Pickup": "Picape",
            "Van": "Van",
            "Minivan": "Minivan"
        }
        return bodywork_map.get(bodywork, bodywork)
    
    @staticmethod
    def get_fuel_type_display(fuel_type: str) -> str:
        """
        Retorna o nome de exibição do combustível.
        
        Args:
            fuel_type: Tipo de combustível
            
        Returns:
            str: Nome de exibição
        """
        fuel_map = {
            "Gasolina": "Gasolina",
            "Etanol": "Etanol",
            "Flex": "Flex",
            "Diesel": "Diesel",
            "GNV": "GNV",
            "Elétrico": "Elétrico",
            "Híbrido": "Híbrido"
        }
        return fuel_map.get(fuel_type, fuel_type)
    
    @staticmethod
    def get_status_display(status: str) -> str:
        """
        Retorna o nome de exibição do status.
        
        Args:
            status: Status do veículo
            
        Returns:
            str: Nome de exibição
        """
        status_map = {
            "Ativo": "Disponível",
            "Inativo": "Indisponível",
            "Vendido": "Vendido",
            "Reservado": "Reservado",
            "Em Manutenção": "Em Manutenção"
        }
        return status_map.get(status, status)
