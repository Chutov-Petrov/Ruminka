# vet_clinic_db.py
import sqlite3
from datetime import datetime
import random

class VetClinicDB:
    def __init__(self, db_name="vet_clinic.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица животных
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT,
                age INTEGER,
                owner_name TEXT,
                phone TEXT,
                registration_date TEXT
            )
        ''')
        
        # Таблица визитов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER,
                visit_date TEXT,
                diagnosis TEXT,
                treatment TEXT,
                cost REAL,
                FOREIGN KEY (animal_id) REFERENCES animals (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_animal(self, name, species, breed, age, owner_name, phone):
        """Добавление нового животного"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO animals (name, species, breed, age, owner_name, phone, registration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, species, breed, age, owner_name, phone, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        conn.commit()
        conn.close()
        print(f"Животное {name} успешно добавлено!")
    
    def add_visit(self, animal_id, diagnosis, treatment, cost):
        """Добавление записи о визите"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO visits (animal_id, visit_date, diagnosis, treatment, cost)
            VALUES (?, ?, ?, ?, ?)
        ''', (animal_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), diagnosis, treatment, cost))
        
        conn.commit()
        conn.close()
        print(f"Визит для животного ID {animal_id} записан!")
    
    def get_all_animals(self):
        """Получение списка всех животных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM animals')
        animals = cursor.fetchall()
        
        conn.close()
        return animals
    
    def get_animal_visits(self, animal_id):
        """Получение истории визитов животного"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.visit_date, v.diagnosis, v.treatment, v.cost 
            FROM visits v 
            WHERE v.animal_id = ? 
            ORDER BY v.visit_date DESC
        ''', (animal_id,))
        
        visits = cursor.fetchall()
        conn.close()
        return visits
    
    def get_statistics(self):
        """Получение статистики клиники"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Общее количество животных
        cursor.execute('SELECT COUNT(*) FROM animals')
        total_animals = cursor.fetchone()[0]
        
        # Количество животных по видам
        cursor.execute('SELECT species, COUNT(*) FROM animals GROUP BY species')
        species_count = cursor.fetchall()
        
        # Общий доход
        cursor.execute('SELECT SUM(cost) FROM visits')
        total_income = cursor.fetchone()[0] or 0
        
        # Количество визитов
        cursor.execute('SELECT COUNT(*) FROM visits')
        total_visits = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_animals': total_animals,
            'species_count': species_count,
            'total_income': total_income,
            'total_visits': total_visits
        }

def main():
    clinic = VetClinicDB()
    
    while True:
        print("\n=== Система управления ветлечебницей ===")
        print("1. Добавить животное")
        print("2. Добавить визит")
        print("3. Показать всех животных")
        print("4. Показать историю визитов")
        print("5. Статистика клиники")
        print("6. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            name = input("Имя животного: ")
            species = input("Вид (собака, кот, etc): ")
            breed = input("Порода: ")
            age = int(input("Возраст: "))
            owner_name = input("Имя владельца: ")
            phone = input("Телефон: ")
            clinic.add_animal(name, species, breed, age, owner_name, phone)
            
        elif choice == '2':
            animal_id = int(input("ID животного: "))
            diagnosis = input("Диагноз: ")
            treatment = input("Лечение: ")
            cost = float(input("Стоимость: "))
            clinic.add_visit(animal_id, diagnosis, treatment, cost)
            
        elif choice == '3':
            animals = clinic.get_all_animals()
            print("\nСписок животных:")
            for animal in animals:
                print(f"ID: {animal[0]}, Имя: {animal[1]}, Вид: {animal[2]}, Порода: {animal[3]}, Возраст: {animal[4]}, Владелец: {animal[5]}")
                
        elif choice == '4':
            animal_id = int(input("ID животного: "))
            visits = clinic.get_animal_visits(animal_id)
            print(f"\nИстория визитов животного ID {animal_id}:")
            for visit in visits:
                print(f"Дата: {visit[0]}, Диагноз: {visit[1]}, Лечение: {visit[2]}, Стоимость: {visit[3]}")
                
        elif choice == '5':
            stats = clinic.get_statistics()
            print("\nСтатистика клиники:")
            print(f"Всего животных: {stats['total_animals']}")
            print("Животные по видам:")
            for species, count in stats['species_count']:
                print(f"  {species}: {count}")
            print(f"Всего визитов: {stats['total_visits']}")
            print(f"Общий доход: {stats['total_income']:.2f} руб.")
            
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()
61
