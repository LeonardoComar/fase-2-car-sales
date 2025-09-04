"""
Presenter para Message - Adapters Layer

Responsável por formatar e apresentar dados de mensagens para a camada REST.
Aplicando Clean Architecture e princípios SOLID.
"""

from typing import List, Dict, Any
from datetime import datetime

from src.application.dtos.message_dto import (
    MessageResponseDto, 
    MessagesStatisticsDto
)


class MessagePresenter:
    """
    Presenter para formatação de dados de mensagens.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas pela apresentação de dados de mensagens
    - OCP: Extensível para novos formatos de apresentação
    - LSP: Pode ser substituído por outras implementações
    - ISP: Interface coesa com métodos específicos
    - DIP: Não depende de implementações concretas
    """
    
    @staticmethod
    def present_message(message_dto: MessageResponseDto) -> Dict[str, Any]:
        """
        Apresenta uma mensagem individual.
        
        Args:
            message_dto: DTO da mensagem
            
        Returns:
            Dict: Dados formatados para resposta
        """
        return {
            "id": str(message_dto.id),
            "responsible_id": str(message_dto.responsible_id) if message_dto.responsible_id else None,
            "vehicle_id": str(message_dto.vehicle_id) if message_dto.vehicle_id else None,
            "name": message_dto.name,
            "email": message_dto.email,
            "phone": message_dto.phone,
            "message": message_dto.message,
            "status": message_dto.status,
            "service_start_time": message_dto.service_start_time.isoformat() if message_dto.service_start_time else None,
            "service_duration_minutes": message_dto.service_duration_minutes,
            "created_at": message_dto.created_at.isoformat(),
            "updated_at": message_dto.updated_at.isoformat(),
            "metadata": {
                "is_pending": message_dto.is_pending,
                "is_in_service": message_dto.is_in_service,
                "is_finished": message_dto.is_finished,
                "is_cancelled": message_dto.is_cancelled,
                "has_responsible": message_dto.has_responsible,
                "has_vehicle": message_dto.has_vehicle
            }
        }
    
    @staticmethod
    def present_message_list(messages: List[MessageResponseDto], 
                           total_count: int = None) -> Dict[str, Any]:
        """
        Apresenta uma lista de mensagens.
        
        Args:
            messages: Lista de DTOs de mensagens
            total_count: Total de registros (para paginação)
            
        Returns:
            Dict: Lista formatada para resposta
        """
        return {
            "messages": [
                MessagePresenter.present_message(message) 
                for message in messages
            ],
            "metadata": {
                "count": len(messages),
                "total_count": total_count if total_count is not None else len(messages)
            }
        }
    
    @staticmethod
    def present_messages_statistics(stats_dto: MessagesStatisticsDto) -> Dict[str, Any]:
        """
        Apresenta estatísticas de mensagens.
        
        Args:
            stats_dto: DTO de estatísticas
            
        Returns:
            Dict: Estatísticas formatadas
        """
        return {
            "overview": {
                "total_messages": stats_dto.total_messages,
                "pending_messages": stats_dto.pending_messages,
                "in_service_messages": stats_dto.in_service_messages,
                "finished_messages": stats_dto.finished_messages,
                "cancelled_messages": stats_dto.cancelled_messages,
                "unassigned_messages": stats_dto.unassigned_messages
            },
            "performance": {
                "average_response_time_hours": stats_dto.average_response_time_hours,
                "average_service_time_minutes": stats_dto.average_service_time_minutes,
                "completion_rate": MessagePresenter._calculate_completion_rate(stats_dto),
                "cancellation_rate": MessagePresenter._calculate_cancellation_rate(stats_dto)
            },
            "distribution": {
                "by_status": stats_dto.messages_by_status,
                "by_day": stats_dto.messages_by_day
            },
            "rankings": {
                "top_performers": MessagePresenter._format_top_performers(stats_dto.top_performers),
                "vehicles_with_most_interest": MessagePresenter._format_vehicles_interest(stats_dto.vehicles_with_most_interest)
            },
            "metadata": {
                "generated_at": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def present_messages_by_vehicle(vehicle_id: str, 
                                   messages: List[MessageResponseDto]) -> Dict[str, Any]:
        """
        Apresenta mensagens relacionadas a um veículo específico.
        
        Args:
            vehicle_id: ID do veículo
            messages: Lista de mensagens
            
        Returns:
            Dict: Dados formatados para resposta
        """
        return {
            "vehicle_id": vehicle_id,
            "interest_count": len(messages),
            "messages": [
                MessagePresenter.present_message(message)
                for message in messages
            ],
            "statistics": {
                "pending": len([m for m in messages if m.is_pending]),
                "in_service": len([m for m in messages if m.is_in_service]),
                "finished": len([m for m in messages if m.is_finished]),
                "cancelled": len([m for m in messages if m.is_cancelled])
            }
        }
    
    @staticmethod
    def present_messages_by_responsible(responsible_id: str, 
                                      messages: List[MessageResponseDto]) -> Dict[str, Any]:
        """
        Apresenta mensagens de um responsável específico.
        
        Args:
            responsible_id: ID do responsável
            messages: Lista de mensagens
            
        Returns:
            Dict: Dados formatados para resposta
        """
        return {
            "responsible_id": responsible_id,
            "assigned_count": len(messages),
            "messages": [
                MessagePresenter.present_message(message)
                for message in messages
            ],
            "performance": {
                "finished_count": len([m for m in messages if m.is_finished]),
                "in_service_count": len([m for m in messages if m.is_in_service]),
                "average_service_time": MessagePresenter._calculate_average_service_time(messages)
            }
        }
    
    @staticmethod
    def present_pending_messages(messages: List[MessageResponseDto]) -> Dict[str, Any]:
        """
        Apresenta mensagens pendentes com informações de prioridade.
        
        Args:
            messages: Lista de mensagens pendentes
            
        Returns:
            Dict: Dados formatados para resposta
        """
        # Ordenar por data de criação (mais antigas primeiro)
        sorted_messages = sorted(messages, key=lambda m: m.created_at)
        
        return {
            "pending_messages": [
                {
                    **MessagePresenter.present_message(message),
                    "priority": MessagePresenter._calculate_priority(message)
                }
                for message in sorted_messages
            ],
            "summary": {
                "total_pending": len(messages),
                "high_priority": len([m for m in messages if MessagePresenter._calculate_priority(m) == "high"]),
                "medium_priority": len([m for m in messages if MessagePresenter._calculate_priority(m) == "medium"]),
                "low_priority": len([m for m in messages if MessagePresenter._calculate_priority(m) == "low"])
            }
        }
    
    @staticmethod
    def _calculate_completion_rate(stats_dto: MessagesStatisticsDto) -> float:
        """Calcula taxa de conclusão."""
        if stats_dto.total_messages == 0:
            return 0.0
        return round((stats_dto.finished_messages / stats_dto.total_messages) * 100, 2)
    
    @staticmethod
    def _calculate_cancellation_rate(stats_dto: MessagesStatisticsDto) -> float:
        """Calcula taxa de cancelamento."""
        if stats_dto.total_messages == 0:
            return 0.0
        return round((stats_dto.cancelled_messages / stats_dto.total_messages) * 100, 2)
    
    @staticmethod
    def _format_top_performers(performers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formata lista de top performers."""
        return [
            {
                "employee_id": str(performer.get("employee_id", "")),
                "messages_handled": performer.get("messages_handled", 0),
                "average_service_time_minutes": performer.get("average_service_time", 0),
                "completion_rate": performer.get("completion_rate", 0)
            }
            for performer in performers
        ]
    
    @staticmethod
    def _format_vehicles_interest(vehicles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formata lista de veículos com interesse."""
        return [
            {
                "vehicle_id": str(vehicle.get("vehicle_id", "")),
                "interest_count": vehicle.get("interest_count", 0),
                "conversion_rate": vehicle.get("conversion_rate", 0),
                "pending_messages": vehicle.get("pending_messages", 0)
            }
            for vehicle in vehicles
        ]
    
    @staticmethod
    def _calculate_average_service_time(messages: List[MessageResponseDto]) -> float:
        """Calcula tempo médio de atendimento."""
        service_times = [
            m.service_duration_minutes 
            for m in messages 
            if m.service_duration_minutes is not None
        ]
        
        if not service_times:
            return 0.0
        
        return round(sum(service_times) / len(service_times), 2)
    
    @staticmethod
    def _calculate_priority(message: MessageResponseDto) -> str:
        """Calcula prioridade baseada no tempo de espera."""
        if not message.created_at:
            return "low"
        
        now = datetime.utcnow()
        hours_waiting = (now - message.created_at).total_seconds() / 3600
        
        if hours_waiting >= 24:
            return "high"
        elif hours_waiting >= 8:
            return "medium"
        else:
            return "low"
