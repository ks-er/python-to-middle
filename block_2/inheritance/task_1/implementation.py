from operator import attrgetter


class Responsibilities:
    def __init__(self, analyse, dev, test) -> None:
        self._analyse = analyse
        self._dev = dev
        self._test = test

class Employee(Responsibilities):
    """Сотрудник."""

    def __init__(self, salary, analyse, dev, test) -> None:
        super().__init__(analyse, dev, test)
        self.salary = salary

class Organization:
    """Организация."""

    def __init__(self) -> None:
        self._employees = []

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return sum(map(attrgetter('_analyse'), self._employees))

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return sum(map(attrgetter('_dev'), self._employees))

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return sum(map(attrgetter('_test'), self._employees))

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError
        self._employees.append(employee)
        return self

    def accept_employees(self, *employees):
        """Принимает массово сотрудников на работу."""
        for employee in employees:
            self.accept_employee(employee)

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        return sum(map(attrgetter('salary'), self._employees))

class CEO(Employee):
    # Генеральный директор
    def __init__(self, salary):
        super().__init__(salary, 1,1, 1)

class Analyst(Employee):
    # Аналитик
    def __init__(self, salary):
        super().__init__(salary, 1, 0, 0)

class Developer(Employee):
    # Разработчик
    def __init__(self, salary):
        super().__init__(salary, 0, 1, 0)

class Tester(Employee):
    # Тестеровщик
    def __init__(self, salary):
        super().__init__(salary, 0, 0, 1)

class TeamLead(Employee):
    # ТимЛид
    def __init__(self, salary):
        super().__init__(salary, 0, 1, 1)

class ProductOwner(Employee):
    # Менеджер продукта
    def __init__(self, salary):
        super().__init__(salary, 1, 0, 1)

class Freelancer(Employee):
    # Внештатный сотрудник
    def __init__(self, responsibilities) -> None:
        self._responsibilities = responsibilities

    def __getattr__(self, name):
        if name == 'salary':
            return 0
        return getattr(self._responsibilities, name)
