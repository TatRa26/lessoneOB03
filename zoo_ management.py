import json

# Базовый класс Animal, представляющий животное
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        """
        Метод для создания звука животного.
        Этот метод должен быть переопределен в подклассах.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def eat(self):
        print(f"{self.name} is eating.")

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data):
        animal_classes = {
            "Bird": Bird,
            "Mammal": Mammal,
            "Reptile": Reptile
        }
        animal_class = animal_classes.get(data["type"])
        if not animal_class:
            raise ValueError(f"Unknown animal type {data['type']}")
        return animal_class(**{k: v for k, v in data.items() if k != "type"})


# Подклассы Animal: Bird, Mammal и Reptile демонстрируют наследование
class Bird(Animal):
    def __init__(self, name, age, wingspan):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self):
        print(f"{self.name} says: chirp chirp!")

    def to_dict(self):
        return {**super().to_dict(), "wingspan": self.wingspan}


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} says: roar!")

    def to_dict(self):
        return {**super().to_dict(), "fur_color": self.fur_color}


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        print(f"{self.name} says: hiss!")

    def to_dict(self):
        return {**super().to_dict(), "scale_type": self.scale_type}


# Функция для демонстрации полиморфизма
def animal_sound(animals):
    """
    Демонстрирует звуки, которые издают животные, используя полиморфизм.
    :param animals: Список животных
    """
    for animal in animals:
        animal.make_sound()


# Класс Employee представляет сотрудника зоопарка
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def to_dict(self):
        return {"name": self.name, "position": self.position}

    @classmethod
    def from_dict(cls, data):
        if data['position'] == 'ZooKeeper':
            return ZooKeeper(data['name'])
        elif data['position'] == 'Veterinarian':
            return Veterinarian(data['name'])
        else:
            raise ValueError(f"Unknown position {data['position']}")


# Подклассы Employee: ZooKeeper и Veterinarian демонстрируют наследование
class ZooKeeper(Employee):
    def __init__(self, name):
        super().__init__(name, position="ZooKeeper")

    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}.")
        animal.eat()


class Veterinarian(Employee):
    def __init__(self, name):
        super().__init__(name, position="Veterinarian")

    def heal_animal(self, animal):
        print(f"{self.name} is treating {animal.name}.")


# Класс ZooSection демонстрирует композицию: зоопарк содержит несколько секций
class ZooSection:
    def __init__(self, section_name):
        self.section_name = section_name
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} has been added to the {self.section_name} section.")

    def show_animals(self):
        print(f"Animals in the {self.section_name} section:")
        for animal in self.animals:
            print(f"- {animal.name}, {animal.age} years old")

    def to_dict(self):
        return {
            "section_name": self.section_name,
            "animals": [animal.to_dict() for animal in self.animals]
        }

    @classmethod
    def from_dict(cls, data):
        section = cls(data["section_name"])
        section.animals = [Animal.from_dict(animal_data) for animal_data in data["animals"]]
        return section


# Класс Zoo использует композицию для управления секциями животных и сотрудниками
class Zoo:
    def __init__(self):
        self.sections = []
        self.staff = ZooStaff()

    def add_section(self, section):
        self.sections.append(section)
        print(f"Section {section.section_name} has been added to the zoo.")

    def show_sections(self):
        for section in self.sections:
            section.show_animals()

    def add_employee(self, employee):
        self.staff.add_employee(employee)

    def show_employees(self):
        self.staff.show_employees()

    def save_zoo(self, filename):
        data = {
            "sections": [section.to_dict() for section in self.sections],
            "staff": self.staff.to_dict()
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Zoo state has been saved to {filename}.")

    @staticmethod
    def load_zoo(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            zoo = Zoo()
            zoo.sections = [ZooSection.from_dict(section_data) for section_data in data["sections"]]
            zoo.staff = ZooStaff.from_dict(data["staff"])
            print(f"Zoo state has been loaded from {filename}.")
            return zoo
        except FileNotFoundError:
            print(f"File {filename} not found. Creating a new zoo.")
            return Zoo()


# Класс ZooStaff демонстрирует композицию: зоопарк содержит сотрудников
class ZooStaff:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"{employee.name} has been hired as a {employee.position}.")

    def show_employees(self):
        print("Employees in the zoo:")
        for employee in self.employees:
            print(f"- {employee.name}, {employee.position}")

    def to_dict(self):
        return {"employees": [employee.to_dict() for employee in self.employees]}

    @classmethod
    def from_dict(cls, data):
        staff = cls()
        staff.employees = [Employee.from_dict(employee_data) for employee_data in data["employees"]]
        return staff


# Примеры использования
if __name__ == "__main__":
    zoo = Zoo.load_zoo("zoo_state.json")

    bird = Bird(name="Sparrow", age=2, wingspan="20 cm")
    mammal = Mammal(name="Lion", age=5, fur_color="golden")
    reptile = Reptile(name="Snake", age=3, scale_type="smooth")

    zookeeper = ZooKeeper(name="John")
    vet = Veterinarian(name="Dr. Smith")

    bird_section = ZooSection(section_name="Birds")
    mammal_section = ZooSection(section_name="Mammals")
    reptile_section = ZooSection(section_name="Reptiles")

    bird_section.add_animal(bird)
    mammal_section.add_animal(mammal)
    reptile_section.add_animal(reptile)

    zoo.add_section(bird_section)
    zoo.add_section(mammal_section)
    zoo.add_section(reptile_section)

    zoo.add_employee(zookeeper)
    zoo.add_employee(vet)

    zoo.show_sections()
    zoo.show_employees()

    zookeeper.feed_animal(mammal)
    vet.heal_animal(reptile)

    animal_sound([bird, mammal, reptile])

    zoo.save_zoo("zoo_state.json")