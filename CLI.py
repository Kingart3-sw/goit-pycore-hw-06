from collections import UserDict


class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Ім'я контакту не може бути порожнім.")
        super().__init__(value)


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (рівно 10 цифр)."""
    def __init__(self, value):
        # Перевіряємо, що рядок складається рівно з 10 цифр
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Номер телефону повинен складатися рівно з 10 цифр.")
        super().__init__(value)


class Record:
    """Клас для зберігання інформації про контакт: ім'я та список телефонів."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        """Додає новий об'єкт Phone до списку телефонів."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        """Видаляє телефон зі списку за його значенням."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Номер телефону {phone_number} не знайдено.")

    def edit_phone(self, old_phone: str, new_phone: str):
        """Замінює старий номер телефону на новий (із перевіркою валідності нового)."""
        phone_to_edit = self.find_phone(old_phone)
        if not phone_to_edit:
            raise ValueError(f"Старий номер телефону {old_phone} не знайдено.")
        
        validated_new_phone = Phone(new_phone)
        index = self.phones.index(phone_to_edit)
        self.phones[index] = validated_new_phone

    def find_phone(self, phone_number: str):
        """Шукає об'єкт Phone у списку за рядком номера. Повертає об'єкт або None."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання записів та керування ними."""
    def add_record(self, record: Record):
        """Додає запис до словника self.data, де ключем є ім'я контакту."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Знаходить і повертає запис Record за ім'ям або None, якщо не знайдено."""
        return self.data.get(name)

    def delete(self, name: str):
        """Видаляє запис за ім'ям."""
        if name in self.data:
            del self.data[name]

if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("=== Усі контакти в книзі ===")
    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print("\n=== Після редагування телефону John ===")
    print(john)  

    found_phone = john.find_phone("5555555555")
    print(f"\nЗнайдений телефон для {john.name}: {found_phone}")  

    book.delete("Jane")
    
    print("\n=== Після видалення Jane ===")
    for name, record in book.data.items():
        print(record)