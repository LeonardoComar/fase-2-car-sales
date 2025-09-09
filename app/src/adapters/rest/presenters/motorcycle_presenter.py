from src.application.dtos.motorcycle_dto import MotorcycleResponseDto, MotorcycleListResponseDto, MotorcycleSummaryDto


class MotorcyclePresenter:
    """
    Presenter para formatação de dados de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela apresentação dos dados de motocicleta.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberto para extensão, fechado para modificação.
    """
    
    @staticmethod
    def present(motorcycle_response: MotorcycleResponseDto) -> MotorcycleResponseDto:
        """
        Apresenta os dados da motocicleta.
        
        Args:
            motorcycle_response: DTO com dados da motocicleta
            
        Returns:
            MotorcycleResponseDto: DTO formatado para apresentação
        """
        # Por enquanto apenas retorna o DTO, mas pode ser extendido
        # para formatação específica, ocultação de campos sensíveis, etc.
        return motorcycle_response
    
    @staticmethod
    def present_list(motorcycle_list_response: MotorcycleListResponseDto) -> MotorcycleListResponseDto:
        """
        Apresenta uma lista de motocicletas.
        
        Args:
            motorcycle_list_response: DTO com lista de motocicletas
            
        Returns:
            MotorcycleListResponseDto: DTO formatado para apresentação
        """
        return motorcycle_list_response
    
    @staticmethod
    def present_summary_list(motorcycle_summaries: list[MotorcycleSummaryDto]) -> list[MotorcycleSummaryDto]:
        """
        Apresenta uma lista de resumos de motocicletas.
        
        Args:
            motorcycle_summaries: Lista de DTOs de resumo
            
        Returns:
            list[MotorcycleSummaryDto]: Lista formatada para apresentação
        """
        return motorcycle_summaries
    
    @staticmethod
    def format_price(price: float) -> str:
        """
        Formata o preço para apresentação.
        
        Args:
            price: Preço da motocicleta
            
        Returns:
            str: Preço formatado
        """
        return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    @staticmethod
    def format_mileage(mileage: int) -> str:
        """
        Formata a quilometragem para apresentação.
        
        Args:
            mileage: Quilometragem da motocicleta
            
        Returns:
            str: Quilometragem formatada
        """
        return f"{mileage:,} km".replace(",", ".")
    
    @staticmethod
    def format_engine_displacement(engine_displacement: int) -> str:
        """
        Formata a cilindrada para apresentação.
        
        Args:
            engine_displacement: Cilindrada da motocicleta
            
        Returns:
            str: Cilindrada formatada
        """
        return f"{engine_displacement}cc"
    
    @staticmethod
    def get_motorcycle_type_display(motorcycle_type: str) -> str:
        """
        Retorna o nome de exibição do tipo de motocicleta.
        
        Args:
            motorcycle_type: Tipo de motocicleta
            
        Returns:
            str: Nome de exibição
        """
        type_map = {
            "Street": "Street",
            "Sport": "Esportiva",
            "Cruiser": "Cruiser",
            "Adventure": "Adventure",
            "Touring": "Touring",
            "Scooter": "Scooter",
            "Custom": "Custom",
            "Trail": "Trail"
        }
        return type_map.get(motorcycle_type, motorcycle_type)
    
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
            "Elétrico": "Elétrico"
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
    
    @staticmethod
    def format_performance_indicator(motorcycle: MotorcycleResponseDto) -> str:
        """
        Formata indicador de performance.
        
        Args:
            motorcycle: DTO da motocicleta
            
        Returns:
            str: Indicador formatado
        """
        indicators = []
        
        if motorcycle.is_high_performance:
            indicators.append("Alto Desempenho")
        
        if motorcycle.has_abs:
            indicators.append("ABS")
        
        if motorcycle.has_traction_control:
            indicators.append("Controle de Tração")
        
        if motorcycle.power_to_weight_ratio:
            indicators.append(f"Relação Peso/Potência: {motorcycle.power_to_weight_ratio}")
        
        return " | ".join(indicators) if indicators else "Padrão"
    
    @staticmethod
    def format_specifications(motorcycle: MotorcycleResponseDto) -> str:
        """
        Formata especificações técnicas.
        
        Args:
            motorcycle: DTO da motocicleta
            
        Returns:
            str: Especificações formatadas
        """
        specs = []
        
        if motorcycle.engine_displacement:
            specs.append(f"{motorcycle.engine_displacement}cc")
            
        if motorcycle.gears:
            specs.append(f"{motorcycle.gears} marchas")
        
        if motorcycle.engine_type:
            specs.append(motorcycle.engine_type)
            specs.append(f"Peso seco: {motorcycle.dry_weight}kg")
        
        if motorcycle.fuel_capacity:
            specs.append(f"Tanque: {motorcycle.fuel_capacity}L")
        
        return " | ".join(specs)
