from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, date

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository


class MockMessageRepository(MessageRepository):
    """
    Implementação mock do repositório de mensagens para desenvolvimento e testes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a interface abstrata definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela simulação de persistência de mensagens.
    """
    
    def __init__(self):
        # Armazenamento em memória para simulação
        self._messages: Dict[UUID, Message] = {}
        
        # Dados iniciais para demonstração
        self._seed_initial_data()
    
    def _seed_initial_data(self):
        """Adiciona dados iniciais para demonstração."""
        # IDs fictícios para relações
        responsible_id_1 = uuid4()
        responsible_id_2 = uuid4()
        vehicle_id_1 = uuid4()
        vehicle_id_2 = uuid4()
        
        # Mensagem 1 - Pendente
        message1 = Message(
            id=uuid4(),
            responsible_id=None,
            vehicle_id=vehicle_id_1,
            name="João Silva",
            email="joao.silva@email.com",
            phone="(11) 99999-9999",
            message="Tenho interesse no veículo anunciado. Gostaria de mais informações sobre financiamento e valores.",
            status=Message.STATUS_PENDENTE,
            created_at=datetime(2024, 1, 15, 10, 30)
        )
        self._messages[message1.id] = message1
        
        # Mensagem 2 - Em atendimento
        message2 = Message(
            id=uuid4(),
            responsible_id=responsible_id_1,
            vehicle_id=vehicle_id_2,
            name="Maria Santos",
            email="maria.santos@email.com",
            phone="(11) 88888-8888",
            message="Gostaria de agendar um test drive. Estou interessada em financiamento também.",
            status=Message.STATUS_CONTATO_INICIADO,
            service_start_time=datetime(2024, 1, 16, 14, 15),
            created_at=datetime(2024, 1, 16, 9, 45)
        )
        self._messages[message2.id] = message2
        
        # Mensagem 3 - Finalizada
        message3 = Message(
            id=uuid4(),
            responsible_id=responsible_id_1,
            vehicle_id=vehicle_id_1,
            name="Pedro Costa",
            email="pedro.costa@email.com",
            phone=None,
            message="Preciso de informações sobre garantia e documentação. É possível negociar o preço?",
            status=Message.STATUS_FINALIZADO,
            service_start_time=datetime(2024, 1, 10, 16, 20),
            created_at=datetime(2024, 1, 10, 11, 15),
            updated_at=datetime(2024, 1, 10, 17, 30)
        )
        self._messages[message3.id] = message3
        
        # Mensagem 4 - Pendente há mais tempo
        message4 = Message(
            id=uuid4(),
            responsible_id=None,
            vehicle_id=None,
            name="Ana Oliveira",
            email="ana.oliveira@email.com",
            phone="(11) 77777-7777",
            message="Estou procurando um carro usado, econômico. Vocês têm opções na faixa de R$ 30.000?",
            status=Message.STATUS_PENDENTE,
            created_at=datetime(2024, 1, 12, 8, 20)
        )
        self._messages[message4.id] = message4
        
        # Mensagem 5 - Cancelada
        message5 = Message(
            id=uuid4(),
            responsible_id=responsible_id_2,
            vehicle_id=vehicle_id_2,
            name="Carlos Lima",
            email="carlos.lima@email.com",
            phone="(11) 66666-6666",
            message="Interesse no veículo para compra à vista.",
            status=Message.STATUS_CANCELADO,
            created_at=datetime(2024, 1, 14, 15, 10),
            updated_at=datetime(2024, 1, 14, 16, 45)
        )
        self._messages[message5.id] = message5
    
    async def save(self, message: Message) -> Message:
        """
        Salva uma mensagem.
        
        Args:
            message: Mensagem a ser salva
            
        Returns:
            Message: Mensagem salva com dados atualizados
        """
        # Se não tem ID, gerar um novo
        if message.id is None:
            message.id = uuid4()
        
        # Atualizar timestamp
        message.updated_at = datetime.utcnow()
        
        # Armazenar
        self._messages[message.id] = message
        
        return message
    
    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """
        Busca uma mensagem pelo ID.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            Optional[Message]: A mensagem encontrada ou None
        """
        return self._messages.get(message_id)
    
    async def find_by_criteria(self, **kwargs) -> List[Message]:
        """
        Busca mensagens por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        messages = list(self._messages.values())
        
        # Aplicar filtros
        messages = self._apply_filters(messages, **kwargs)
        
        # Aplicar ordenação
        messages = self._apply_ordering(messages, kwargs.get('order_by'), kwargs.get('order_direction'))
        
        # Aplicar paginação
        if 'skip' in kwargs and kwargs['skip'] is not None:
            offset = kwargs['skip']
            messages = messages[offset:]
        
        if 'limit' in kwargs and kwargs['limit'] is not None:
            limit = kwargs['limit']
            messages = messages[:limit]
        
        return messages
    
    async def find_by_email(self, email: str, **kwargs) -> List[Message]:
        """
        Busca mensagens por email.
        
        Args:
            email: Email do interessado
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        kwargs['email'] = email
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_responsible(self, responsible_id: UUID, **kwargs) -> List[Message]:
        """
        Busca mensagens por responsável.
        
        Args:
            responsible_id: ID do funcionário responsável
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        kwargs['responsible_id'] = responsible_id
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_vehicle(self, vehicle_id: UUID, **kwargs) -> List[Message]:
        """
        Busca mensagens por veículo.
        
        Args:
            vehicle_id: ID do veículo
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        kwargs['vehicle_id'] = vehicle_id
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_status(self, status: str, **kwargs) -> List[Message]:
        """
        Busca mensagens por status.
        
        Args:
            status: Status das mensagens
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        kwargs['status'] = status
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_date_range(self, start_date: date, end_date: date, **kwargs) -> List[Message]:
        """
        Busca mensagens por período.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        kwargs['start_date'] = start_date
        kwargs['end_date'] = end_date
        return await self.find_by_criteria(**kwargs)
    
    async def find_pending_messages(self, **kwargs) -> List[Message]:
        """
        Busca mensagens pendentes.
        
        Args:
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens pendentes
        """
        kwargs['status'] = Message.STATUS_PENDENTE
        return await self.find_by_criteria(**kwargs)
    
    async def find_unassigned_messages(self, **kwargs) -> List[Message]:
        """
        Busca mensagens sem responsável atribuído.
        
        Args:
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens sem responsável
        """
        kwargs['unassigned_only'] = True
        return await self.find_by_criteria(**kwargs)
    
    async def find_overdue_messages(self, hours_threshold: int = 24, **kwargs) -> List[Message]:
        """
        Busca mensagens em atraso (pendentes há muito tempo).
        
        Args:
            hours_threshold: Número de horas para considerar em atraso
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens em atraso
        """
        now = datetime.utcnow()
        threshold_time = now.timestamp() - (hours_threshold * 3600)
        
        overdue_messages = []
        for message in self._messages.values():
            if (message.status == Message.STATUS_PENDENTE and 
                message.created_at.timestamp() < threshold_time):
                overdue_messages.append(message)
        
        # Aplicar outros filtros se fornecidos
        if kwargs:
            overdue_messages = self._apply_filters(overdue_messages, **kwargs)
        
        return overdue_messages
    
    async def delete(self, message_id: UUID) -> None:
        """
        Remove uma mensagem.
        
        Args:
            message_id: ID da mensagem a ser removida
        """
        if message_id in self._messages:
            del self._messages[message_id]
    
    async def exists_by_id(self, message_id: UUID) -> bool:
        """
        Verifica se existe mensagem com o ID.
        
        Args:
            message_id: ID a ser verificado
            
        Returns:
            bool: True se existir mensagem com o ID
        """
        return message_id in self._messages
    
    async def count_by_status(self, status: str) -> int:
        """
        Conta mensagens por status.
        
        Args:
            status: Status das mensagens
            
        Returns:
            int: Número de mensagens com o status
        """
        count = 0
        for message in self._messages.values():
            if message.status == status:
                count += 1
        return count
    
    async def count_by_responsible(self, responsible_id: UUID) -> int:
        """
        Conta mensagens por responsável.
        
        Args:
            responsible_id: ID do funcionário responsável
            
        Returns:
            int: Número de mensagens do responsável
        """
        count = 0
        for message in self._messages.values():
            if message.responsible_id == responsible_id:
                count += 1
        return count
    
    async def count_by_vehicle(self, vehicle_id: UUID) -> int:
        """
        Conta mensagens por veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Número de mensagens do veículo
        """
        count = 0
        for message in self._messages.values():
            if message.vehicle_id == vehicle_id:
                count += 1
        return count
    
    async def count_pending_messages(self) -> int:
        """
        Conta mensagens pendentes.
        
        Returns:
            int: Número de mensagens pendentes
        """
        return await self.count_by_status(Message.STATUS_PENDENTE)
    
    async def count_unassigned_messages(self) -> int:
        """
        Conta mensagens sem responsável.
        
        Returns:
            int: Número de mensagens sem responsável
        """
        count = 0
        for message in self._messages.values():
            if message.responsible_id is None:
                count += 1
        return count
    
    async def get_response_time_statistics(self, start_date: Optional[date] = None, 
                                          end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Calcula estatísticas de tempo de resposta.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas de tempo de resposta
        """
        filtered_messages = [
            message for message in self._messages.values()
            if self._message_in_date_range(message, start_date, end_date)
        ]
        
        # Calcular tempo de resposta (entre criação e início do atendimento)
        response_times = []
        service_times = []
        
        for message in filtered_messages:
            if message.service_start_time:
                response_time_hours = (message.service_start_time - message.created_at).total_seconds() / 3600
                response_times.append(response_time_hours)
                
                if message.is_finished():
                    service_time_minutes = (message.updated_at - message.service_start_time).total_seconds() / 60
                    service_times.append(service_time_minutes)
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else None
        avg_service_time = sum(service_times) / len(service_times) if service_times else None
        
        return {
            'average_response_time_hours': avg_response_time,
            'average_service_time_minutes': avg_service_time,
            'total_responded': len(response_times),
            'total_completed': len(service_times)
        }
    
    async def get_messages_statistics(self, start_date: Optional[date] = None, 
                                     end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Busca estatísticas gerais de mensagens.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas das mensagens
        """
        filtered_messages = [
            message for message in self._messages.values()
            if self._message_in_date_range(message, start_date, end_date)
        ]
        
        total_messages = len(filtered_messages)
        
        # Distribuição por dia
        messages_by_day = {}
        for message in filtered_messages:
            day_key = message.created_at.date().strftime('%Y-%m-%d')
            messages_by_day[day_key] = messages_by_day.get(day_key, 0) + 1
        
        return {
            'total_messages': total_messages,
            'messages_by_day': messages_by_day
        }
    
    async def get_top_performers(self, start_date: Optional[date] = None, 
                                end_date: Optional[date] = None, 
                                limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca funcionários com melhor performance no atendimento.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de funcionários com estatísticas
        """
        filtered_messages = [
            message for message in self._messages.values()
            if (self._message_in_date_range(message, start_date, end_date) and 
                message.responsible_id is not None)
        ]
        
        # Agrupar por funcionário
        employee_stats = {}
        for message in filtered_messages:
            emp_id = message.responsible_id
            if emp_id not in employee_stats:
                employee_stats[emp_id] = {
                    'employee_id': emp_id,
                    'messages_handled': 0,
                    'messages_finished': 0,
                    'total_service_time': 0,
                    'service_count': 0
                }
            
            employee_stats[emp_id]['messages_handled'] += 1
            
            if message.is_finished():
                employee_stats[emp_id]['messages_finished'] += 1
                
                if message.service_start_time:
                    service_time = (message.updated_at - message.service_start_time).total_seconds() / 60
                    employee_stats[emp_id]['total_service_time'] += service_time
                    employee_stats[emp_id]['service_count'] += 1
        
        # Calcular métricas e ordenar
        performers = []
        for stats in employee_stats.values():
            avg_service_time = (stats['total_service_time'] / stats['service_count'] 
                              if stats['service_count'] > 0 else 0)
            completion_rate = (stats['messages_finished'] / stats['messages_handled'] 
                             if stats['messages_handled'] > 0 else 0)
            
            performers.append({
                'employee_id': stats['employee_id'],
                'messages_handled': stats['messages_handled'],
                'average_service_time': avg_service_time,
                'completion_rate': completion_rate
            })
        
        # Ordenar por número de mensagens tratadas
        performers.sort(key=lambda x: x['messages_handled'], reverse=True)
        
        return performers[:limit]
    
    async def get_vehicles_with_most_interest(self, start_date: Optional[date] = None, 
                                            end_date: Optional[date] = None, 
                                            limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca veículos com mais interesse (mais mensagens).
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de veículos com estatísticas
        """
        filtered_messages = [
            message for message in self._messages.values()
            if (self._message_in_date_range(message, start_date, end_date) and 
                message.vehicle_id is not None)
        ]
        
        # Agrupar por veículo
        vehicle_stats = {}
        for message in filtered_messages:
            v_id = message.vehicle_id
            if v_id not in vehicle_stats:
                vehicle_stats[v_id] = {
                    'vehicle_id': v_id,
                    'interest_count': 0,
                    'pending_messages': 0,
                    'finished_messages': 0
                }
            
            vehicle_stats[v_id]['interest_count'] += 1
            
            if message.is_pending():
                vehicle_stats[v_id]['pending_messages'] += 1
            elif message.is_finished():
                vehicle_stats[v_id]['finished_messages'] += 1
        
        # Calcular conversion rate e ordenar
        vehicles = []
        for stats in vehicle_stats.values():
            conversion_rate = (stats['finished_messages'] / stats['interest_count'] 
                             if stats['interest_count'] > 0 else 0)
            
            vehicles.append({
                'vehicle_id': stats['vehicle_id'],
                'interest_count': stats['interest_count'],
                'pending_messages': stats['pending_messages'],
                'conversion_rate': conversion_rate
            })
        
        # Ordenar por interesse
        vehicles.sort(key=lambda x: x['interest_count'], reverse=True)
        
        return vehicles[:limit]
    
    def _apply_filters(self, messages: List[Message], **kwargs) -> List[Message]:
        """Aplica filtros à lista de mensagens."""
        result = messages.copy()
        
        # Filtros diretos
        if 'status' in kwargs and kwargs['status']:
            result = [m for m in result if m.status == kwargs['status']]
        
        if 'responsible_id' in kwargs and kwargs['responsible_id']:
            result = [m for m in result if m.responsible_id == kwargs['responsible_id']]
        
        if 'vehicle_id' in kwargs and kwargs['vehicle_id']:
            result = [m for m in result if m.vehicle_id == kwargs['vehicle_id']]
        
        if 'email' in kwargs and kwargs['email']:
            result = [m for m in result if m.email.lower() == kwargs['email'].lower()]
        
        # Filtros de data
        if 'start_date' in kwargs and kwargs['start_date']:
            start_date = kwargs['start_date']
            result = [m for m in result if m.created_at.date() >= start_date]
        
        if 'end_date' in kwargs and kwargs['end_date']:
            end_date = kwargs['end_date']
            result = [m for m in result if m.created_at.date() <= end_date]
        
        # Filtros especiais
        if 'unassigned_only' in kwargs and kwargs['unassigned_only']:
            result = [m for m in result if m.responsible_id is None]
        
        return result
    
    def _apply_ordering(self, messages: List[Message], order_by: Optional[str], order_direction: Optional[str]) -> List[Message]:
        """Aplica ordenação à lista de mensagens."""
        if not order_by:
            order_by = 'created_at'
        
        if not order_direction:
            order_direction = 'desc'
        
        reverse = order_direction.lower() == 'desc'
        
        # Ordenação por campo
        if order_by == 'created_at':
            messages.sort(key=lambda m: m.created_at, reverse=reverse)
        elif order_by == 'updated_at':
            messages.sort(key=lambda m: m.updated_at, reverse=reverse)
        elif order_by == 'status':
            messages.sort(key=lambda m: m.status, reverse=reverse)
        elif order_by == 'name':
            messages.sort(key=lambda m: m.name, reverse=reverse)
        elif order_by == 'service_start_time':
            messages.sort(key=lambda m: m.service_start_time or datetime.min, reverse=reverse)
        
        return messages
    
    def _message_in_date_range(self, message: Message, start_date: Optional[date], end_date: Optional[date]) -> bool:
        """Verifica se mensagem está no período especificado."""
        if start_date and message.created_at.date() < start_date:
            return False
        if end_date and message.created_at.date() > end_date:
            return False
        return True
