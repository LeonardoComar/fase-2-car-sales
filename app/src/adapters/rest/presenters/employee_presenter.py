from typing import List, Dict, Any
from datetime import datetime

from src.application.dtos.employee_dto import EmployeeResponseDto


class EmployeePresenter:
    """
    Presenter para formatação de respostas de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por formatar dados de funcionários para apresentação.
    """
    
    def present_employee(self, employee: EmployeeResponseDto) -> Dict[str, Any]:
        """
        Apresenta um funcionário.
        
        Args:
            employee: DTO de resposta do funcionário
            
        Returns:
            Dict[str, Any]: Funcionário formatado para apresentação
        """
        return {
            "success": True,
            "data": {
                "id": str(employee.id),
                "personal_info": {
                    "name": employee.name,
                    "display_name": employee.display_name,
                    "email": employee.email,
                    "phone": employee.phone,
                    "formatted_phone": employee.formatted_phone,
                    "cpf": employee.cpf,
                    "formatted_cpf": employee.formatted_cpf,
                    "birth_date": employee.birth_date.isoformat(),
                    "age": employee.age
                },
                "employment_info": {
                    "employee_id": employee.employee_id,
                    "position": employee.position,
                    "department": employee.department,
                    "salary": float(employee.salary),
                    "formatted_salary": employee.formatted_salary,
                    "hire_date": employee.hire_date.isoformat(),
                    "years_of_service": employee.years_of_service,
                    "manager_id": str(employee.manager_id) if employee.manager_id else None,
                    "status": employee.status
                },
                "address_info": {
                    "address": employee.address,
                    "city": employee.city,
                    "state": employee.state,
                    "zip_code": employee.zip_code,
                    "formatted_zip_code": employee.formatted_zip_code,
                    "full_address": employee.full_address
                },
                "emergency_contact": {
                    "name": employee.emergency_contact_name,
                    "phone": employee.emergency_contact_phone
                },
                "attributes": {
                    "is_manager": employee.is_manager,
                    "is_senior": employee.is_senior,
                    "can_approve_expenses": employee.can_approve_expenses,
                    "needs_performance_review": employee.needs_performance_review
                },
                "notes": employee.notes,
                "audit": {
                    "created_at": employee.created_at.isoformat(),
                    "updated_at": employee.updated_at.isoformat()
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def present_employee_list(self, employees: List[EmployeeResponseDto]) -> Dict[str, Any]:
        """
        Apresenta uma lista de funcionários.
        
        Args:
            employees: Lista de DTOs de resposta de funcionários
            
        Returns:
            Dict[str, Any]: Lista formatada para apresentação
        """
        return {
            "success": True,
            "data": {
                "employees": [self._format_employee_summary(employee) for employee in employees],
                "total_count": len(employees),
                "summary": self._generate_employee_summary(employees)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def present_promotion_success(self, employee: EmployeeResponseDto) -> Dict[str, Any]:
        """
        Apresenta sucesso de promoção.
        
        Args:
            employee: DTO de resposta do funcionário promovido
            
        Returns:
            Dict[str, Any]: Resposta de promoção formatada
        """
        return {
            "success": True,
            "message": f"Funcionário {employee.name} promovido com sucesso",
            "data": {
                "employee": self._format_employee_summary(employee),
                "promotion_details": {
                    "new_position": employee.position,
                    "new_department": employee.department,
                    "new_salary": employee.formatted_salary,
                    "years_of_service": employee.years_of_service,
                    "is_manager": employee.is_manager
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def present_status_update_success(self, employee: EmployeeResponseDto) -> Dict[str, Any]:
        """
        Apresenta sucesso de atualização de status.
        
        Args:
            employee: DTO de resposta do funcionário
            
        Returns:
            Dict[str, Any]: Resposta de atualização formatada
        """
        status_translation = {
            "active": "Ativo",
            "inactive": "Inativo",
            "suspended": "Suspenso", 
            "terminated": "Terminado",
            "on_leave": "Em Licença"
        }
        
        return {
            "success": True,
            "message": f"Status do funcionário {employee.name} atualizado para {status_translation.get(employee.status, employee.status)}",
            "data": {
                "employee": self._format_employee_summary(employee),
                "status_info": {
                    "current_status": employee.status,
                    "status_description": status_translation.get(employee.status, employee.status),
                    "can_work": employee.status == "active"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def present_deletion_success(self, entity_type: str) -> Dict[str, Any]:
        """
        Apresenta sucesso de exclusão.
        
        Args:
            entity_type: Tipo da entidade excluída
            
        Returns:
            Dict[str, Any]: Resposta de exclusão formatada
        """
        return {
            "success": True,
            "message": f"{entity_type} excluído com sucesso",
            "timestamp": datetime.now().isoformat()
        }
    
    def present_department_employees(self, employees: List[EmployeeResponseDto], department: str) -> Dict[str, Any]:
        """
        Apresenta funcionários por departamento.
        
        Args:
            employees: Lista de funcionários
            department: Nome do departamento
            
        Returns:
            Dict[str, Any]: Funcionários do departamento formatados
        """
        active_employees = [emp for emp in employees if emp.status == "active"]
        managers = [emp for emp in employees if emp.is_manager]
        
        total_payroll = sum(float(emp.salary) for emp in active_employees)
        avg_salary = total_payroll / len(active_employees) if active_employees else 0
        avg_service_time = sum(emp.years_of_service for emp in active_employees) / len(active_employees) if active_employees else 0
        
        return {
            "success": True,
            "data": {
                "department": department,
                "employees": [self._format_employee_summary(emp) for emp in employees],
                "statistics": {
                    "total_employees": len(employees),
                    "active_employees": len(active_employees),
                    "managers_count": len(managers),
                    "total_payroll": f"R$ {total_payroll:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    "average_salary": f"R$ {avg_salary:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    "average_service_time": f"{avg_service_time:.1f} anos"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def present_managers_list(self, managers: List[EmployeeResponseDto]) -> Dict[str, Any]:
        """
        Apresenta lista de gerentes.
        
        Args:
            managers: Lista de gerentes
            
        Returns:
            Dict[str, Any]: Lista de gerentes formatada
        """
        departments = {}
        for manager in managers:
            dept = manager.department
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(manager)
        
        return {
            "success": True,
            "data": {
                "managers": [self._format_manager_info(manager) for manager in managers],
                "by_department": {
                    dept: [self._format_manager_info(mgr) for mgr in mgrs] 
                    for dept, mgrs in departments.items()
                },
                "total_managers": len(managers),
                "departments_count": len(departments)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_employee_summary(self, employee: EmployeeResponseDto) -> Dict[str, Any]:
        """
        Formata resumo de funcionário.
        
        Args:
            employee: DTO de resposta do funcionário
            
        Returns:
            Dict[str, Any]: Resumo formatado
        """
        return {
            "id": str(employee.id),
            "name": employee.name,
            "display_name": employee.display_name,
            "employee_id": employee.employee_id,
            "email": employee.email,
            "phone": employee.formatted_phone,
            "position": employee.position,
            "department": employee.department,
            "salary": employee.formatted_salary,
            "hire_date": employee.hire_date.isoformat(),
            "years_of_service": employee.years_of_service,
            "status": employee.status,
            "is_manager": employee.is_manager,
            "is_senior": employee.is_senior
        }
    
    def _format_manager_info(self, manager: EmployeeResponseDto) -> Dict[str, Any]:
        """
        Formata informações de gerente.
        
        Args:
            manager: DTO de resposta do gerente
            
        Returns:
            Dict[str, Any]: Informações de gerente formatadas
        """
        return {
            "id": str(manager.id),
            "name": manager.name,
            "display_name": manager.display_name,
            "employee_id": manager.employee_id,
            "email": manager.email,
            "position": manager.position,
            "department": manager.department,
            "years_of_service": manager.years_of_service,
            "can_approve_expenses": manager.can_approve_expenses,
            "status": manager.status
        }
    
    def _generate_employee_summary(self, employees: List[EmployeeResponseDto]) -> Dict[str, Any]:
        """
        Gera resumo estatístico dos funcionários.
        
        Args:
            employees: Lista de funcionários
            
        Returns:
            Dict[str, Any]: Resumo estatístico
        """
        if not employees:
            return {
                "total_employees": 0,
                "active_employees": 0,
                "departments": 0,
                "managers": 0,
                "average_age": 0,
                "average_service_time": 0
            }
        
        active_employees = [emp for emp in employees if emp.status == "active"]
        departments = set(emp.department for emp in employees)
        managers = [emp for emp in employees if emp.is_manager]
        
        avg_age = sum(emp.age for emp in employees) / len(employees)
        avg_service = sum(emp.years_of_service for emp in employees) / len(employees)
        
        return {
            "total_employees": len(employees),
            "active_employees": len(active_employees),
            "departments": len(departments),
            "managers": len(managers),
            "average_age": round(avg_age, 1),
            "average_service_time": round(avg_service, 1)
        }
