"""
Caso de uso para obter estatísticas de mensagens - Application Layer

Implementa a lógica de aplicação para gerar relatórios e estatísticas
sobre o atendimento de mensagens.
"""

from typing import Optional
from datetime import date

from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessagesStatisticsDto


class GetMessagesStatisticsUseCase:
    """
    Caso de uso para obter estatísticas de mensagens.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas por estatísticas de mensagens
    - OCP: Extensível para novas métricas
    - LSP: Pode ser substituído por outras implementações
    - ISP: Interface coesa
    - DIP: Depende de abstrações (MessageRepository)
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o caso de uso.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, start_date: Optional[date] = None, 
                     end_date: Optional[date] = None) -> MessagesStatisticsDto:
        """
        Executa a geração de estatísticas de mensagens.
        
        Args:
            start_date: Data inicial para filtro (opcional)
            end_date: Data final para filtro (opcional)
            
        Returns:
            MessagesStatisticsDto: Estatísticas das mensagens
        """
        # Obter estatísticas básicas
        stats = await self._message_repository.get_messages_statistics(start_date, end_date)
        
        # Obter estatísticas de tempo de resposta
        response_stats = await self._message_repository.get_response_time_statistics(start_date, end_date)
        
        # Obter top performers
        top_performers = await self._message_repository.get_top_performers(start_date, end_date, limit=5)
        
        # Obter veículos com mais interesse
        vehicles_interest = await self._message_repository.get_vehicles_with_most_interest(start_date, end_date, limit=5)
        
        # Contar por status
        total_messages = stats.get('total_messages', 0)
        pending_count = await self._message_repository.count_by_status("Pendente")
        in_service_count = await self._message_repository.count_by_status("Contato iniciado")
        finished_count = await self._message_repository.count_by_status("Finalizado")
        cancelled_count = await self._message_repository.count_by_status("Cancelado")
        unassigned_count = await self._message_repository.count_unassigned_messages()
        
        # Montar distribuição por status
        messages_by_status = {
            "Pendente": pending_count,
            "Contato iniciado": in_service_count,
            "Finalizado": finished_count,
            "Cancelado": cancelled_count
        }
        
        # Criar DTO de resposta
        return MessagesStatisticsDto(
            total_messages=total_messages,
            pending_messages=pending_count,
            in_service_messages=in_service_count,
            finished_messages=finished_count,
            cancelled_messages=cancelled_count,
            unassigned_messages=unassigned_count,
            average_response_time_hours=response_stats.get('average_response_time_hours'),
            average_service_time_minutes=response_stats.get('average_service_time_minutes'),
            messages_by_status=messages_by_status,
            messages_by_day=stats.get('messages_by_day', {}),
            top_performers=top_performers,
            vehicles_with_most_interest=vehicles_interest
        )
