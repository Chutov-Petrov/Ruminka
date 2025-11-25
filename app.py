# vet_clinic_client.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import random

class VetClinicClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Ветлечебница 'Друг' - Клиентский портал")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f8ff')
        
        # Стили
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f8ff')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f8ff')
        
        self.current_user = None
        self.user_animals = []
        
        self.init_database()
        self.create_login_screen()
    
    def init_database(self):
        """Инициализация базы данных для демо"""
        conn = sqlite3.connect('vet_clinic_client.db')
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE,
                name TEXT,
                email TEXT,
                registration_date TEXT
            )
        ''')
        
        # Таблица животных клиентов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_phone TEXT,
                name TEXT,
                species TEXT,
                breed TEXT,
                age INTEGER,
                weight REAL,
                special_notes TEXT,
                FOREIGN KEY (client_phone) REFERENCES clients (phone)
            )
        ''')
        
        # Таблица записей на прием
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_phone TEXT,
                animal_name TEXT,
                service_type TEXT,
                appointment_date TEXT,
                appointment_time TEXT,
                status TEXT,
                doctor TEXT,
                notes TEXT
            )
        ''')
        
        # Добавляем демо-данные
        self.add_demo_data(cursor)
        
        conn.commit()
        conn.close()
    
    def add_demo_data(self, cursor):
        """Добавление демо-данных"""
        # Демо-клиенты
        demo_clients = [
            ('79161234567', 'Иван Петров', 'ivan@mail.ru'),
            ('79037654321', 'Мария Сидорова', 'maria@mail.ru'),
        ]
        
        for phone, name, email in demo_clients:
            try:
                cursor.execute(
                    'INSERT INTO clients (phone, name, email, registration_date) VALUES (?, ?, ?, ?)',
                    (phone, name, email, datetime.now().strftime("%Y-%m-%d"))
                )
            except sqlite3.IntegrityError:
                pass
        
        # Демо-животные
        demo_animals = [
            ('79161234567', 'Барсик', 'Кот', 'Сиамский', 3, 4.5, 'Аллергия на курицу'),
            ('79161234567', 'Рекс', 'Собака', 'Овчарка', 5, 30.0, 'Любит играть с мячом'),
            ('79037654321', 'Кеша', 'Попугай', 'Ара', 2, 1.2, 'Разговаривает'),
        ]
        
        for phone, name, species, breed, age, weight, notes in demo_animals:
            cursor.execute(
                '''INSERT INTO client_animals 
                (client_phone, name, species, breed, age, weight, special_notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (phone, name, species, breed, age, weight, notes)
            )
        
        # Демо-записи
        demo_appointments = [
            ('79161234567', 'Барсик', 'Вакцинация', '2024-12-15', '10:00', 'Подтвержден', 'Др. Смирнова', 'Ежегодная вакцинация'),
            ('79037654321', 'Кеша', 'Осмотр', '2024-12-16', '14:30', 'Подтвержден', 'Др. Иванов', 'Плановый осмотр'),
        ]
        
        for phone, animal, service, date, time, status, doctor, notes in demo_appointments:
            cursor.execute(
                '''INSERT INTO appointments 
                (client_phone, animal_name, service_type, appointment_date, appointment_time, status, doctor, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (phone, animal, service, date, time, status, doctor, notes)
            )
    
    def create_login_screen(self):
        """Создание экрана входа"""
        self.clear_screen()
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill='both')
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Ветлечебница 'Друг'", style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(main_frame, text="Клиентский портал", font=('Arial', 14))
        subtitle_label.pack(pady=10)
        
        # Фрейм для входа
        login_frame = ttk.LabelFrame(main_frame, text="Вход в систему", padding=15)
        login_frame.pack(pady=20, ipadx=10, ipady=10)
        
        ttk.Label(login_frame, text="Номер телефона:").grid(row=0, column=0, sticky='w', pady=5)
        self.phone_entry = ttk.Entry(login_frame, font=('Arial', 12), width=20)
        self.phone_entry.grid(row=0, column=1, pady=5, padx=10)
        self.phone_entry.insert(0, '79161234567')  # Демо-номер
        
        ttk.Label(login_frame, text="Имя:").grid(row=1, column=0, sticky='w', pady=5)
        self.name_entry = ttk.Entry(login_frame, font=('Arial', 12), width=20)
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)
        self.name_entry.insert(0, 'Иван Петров')  # Демо-имя
        
        # Кнопки
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Войти", 
                  command=self.login, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Регистрация", 
                  command=self.show_registration, width=15).pack(side='left', padx=5)
        
        # Информация
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=20)
        
        info_text = """Добро пожаловать в клиентский портал ветлечебницы "Друг"!
        
Возможности системы:
• Просмотр ваших питомцев
• Запись на прием онлайн
• История посещений
• Управление записями
• Медицинские карты животных"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify='center', font=('Arial', 10))
        info_label.pack()
    
    def show_registration(self):
        """Окно регистрации"""
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Регистрация")
        registration_window.geometry("400x300")
        registration_window.configure(bg='#f0f8ff')
        
        ttk.Label(registration_window, text="Регистрация нового клиента", 
                 style='Title.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(registration_window, padding=10)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Телефон:").grid(row=0, column=0, sticky='w', pady=5)
        reg_phone = ttk.Entry(form_frame, width=20)
        reg_phone.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="ФИО:").grid(row=1, column=0, sticky='w', pady=5)
        reg_name = ttk.Entry(form_frame, width=20)
        reg_name.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        reg_email = ttk.Entry(form_frame, width=20)
        reg_email.grid(row=2, column=1, pady=5, padx=10)
        
        def register():
            phone = reg_phone.get()
            name = reg_name.get()
            email = reg_email.get()
            
            if not all([phone, name, email]):
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            try:
                conn = sqlite3.connect('vet_clinic_client.db')
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO clients (phone, name, email, registration_date) VALUES (?, ?, ?, ?)',
                    (phone, name, email, datetime.now().strftime("%Y-%m-%d"))
                )
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Успех", "Регистрация завершена! Теперь вы можете войти в систему.")
                registration_window.destroy()
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Пользователь с таким телефоном уже существует!")
        
        ttk.Button(registration_window, text="Зарегистрироваться", 
                  command=register).pack(pady=20)
    
    def login(self):
        """Вход в систему"""
        phone = self.phone_entry.get()
        name = self.name_entry.get()
        
        if not phone or not name:
            messagebox.showerror("Ошибка", "Введите телефон и имя!")
            return
        
        conn = sqlite3.connect('vet_clinic_client.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clients WHERE phone = ? AND name = ?', (phone, name))
        user = cursor.fetchone()
        
        if user:
            self.current_user = {
                'phone': user[1],
                'name': user[2],
                'email': user[3]
            }
            self.load_user_animals()
            self.create_main_screen()
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден!")
        
        conn.close()
    
    def load_user_animals(self):
        """Загрузка животных пользователя"""
        conn = sqlite3.connect('vet_clinic_client.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT * FROM client_animals WHERE client_phone = ?', 
            (self.current_user['phone'],)
        )
        self.user_animals = []
        
        for animal in cursor.fetchall():
            self.user_animals.append({
                'id': animal[0],
                'name': animal[2],
                'species': animal[3],
                'breed': animal[4],
                'age': animal[5],
                'weight': animal[6],
                'notes': animal[7]
            })
        
        conn.close()
    
    def create_main_screen(self):
        """Создание главного экрана после входа"""
        self.clear_screen()
        
        # Верхняя панель
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill='x')
        
        welcome_label = ttk.Label(
            header_frame, 
            text=f"Добро пожаловать, {self.current_user['name']}!",
            style='Title.TLabel'
        )
        welcome_label.pack(side='left')
        
        ttk.Button(header_frame, text="Выйти", 
                  command=self.logout).pack(side='right')
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        
        # Вкладка питомцев
        pets_frame = ttk.Frame(notebook, padding=10)
        notebook.add(pets_frame, text="Мои питомцы")
        
        # Вкладка записи
        appointments_frame = ttk.Frame(notebook, padding=10)
        notebook.add(appointments_frame, text="Запись на прием")
        
        # Вкладка история
        history_frame = ttk.Frame(notebook, padding=10)
        notebook.add(history_frame, text="История посещений")
        
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Заполнение вкладок
        self.create_pets_tab(pets_frame)
        self.create_appointments_tab(appointments_frame)
        self.create_history_tab(history_frame)
    
    def create_pets_tab(self, parent):
        """Вкладка моих питомцев"""
        # Кнопка добавления питомца
        ttk.Button(parent, text="+ Добавить питомца", 
                  command=self.show_add_pet_dialog).pack(anchor='w', pady=5)
        
        # Фрейм для карточек питомцев
        self.pets_cards_frame = ttk.Frame(parent)
        self.pets_cards_frame.pack(fill='both', expand=True, pady=10)
        
        self.update_pets_display()
    
    def update_pets_display(self):
        """Обновление отображения питомцев"""
        for widget in self.pets_cards_frame.winfo_children():
            widget.destroy()
        
        if not self.user_animals:
            ttk.Label(self.pets_cards_frame, text="У вас пока нет зарегистрированных питомцев", 
                     font=('Arial', 12)).pack(pady=50)
            return
        
        # Создание карточек питомцев
        for i, animal in enumerate(self.user_animals):
            card_frame = ttk.LabelFrame(self.pets_cards_frame, text=animal['name'], padding=10)
            card_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            info_text = f"""Вид: {animal['species']}
Порода: {animal['breed']}
Возраст: {animal['age']} лет
Вес: {animal['weight']} кг
Особенности: {animal['notes']}"""
            
            ttk.Label(card_frame, text=info_text, justify='left').pack(anchor='w')
            
            button_frame = ttk.Frame(card_frame)
            button_frame.pack(fill='x', pady=5)
            
            ttk.Button(button_frame, text="Записаться", 
                      command=lambda a=animal: self.show_appointment_dialog(a)).pack(side='left', padx=2)
            ttk.Button(button_frame, text="Удалить", 
                      command=lambda a=animal: self.delete_pet(a)).pack(side='left', padx=2)
        
        # Настройка сетки
        for i in range(2):
            self.pets_cards_frame.columnconfigure(i, weight=1)
    
    def show_add_pet_dialog(self):
        """Диалог добавления питомца"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить питомца")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Добавление нового питомца", 
                 style='Title.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky='w', pady=5)
        pet_name = ttk.Entry(form_frame, width=20)
        pet_name.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Вид:").grid(row=1, column=0, sticky='w', pady=5)
        pet_species = ttk.Combobox(form_frame, values=["Собака", "Кот", "Попугай", "Хомяк", "Кролик", "Другое"])
        pet_species.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Порода:").grid(row=2, column=0, sticky='w', pady=5)
        pet_breed = ttk.Entry(form_frame, width=20)
        pet_breed.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Возраст (лет):").grid(row=3, column=0, sticky='w', pady=5)
        pet_age = ttk.Spinbox(form_frame, from_=0, to=50, width=18)
        pet_age.grid(row=3, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Вес (кг):").grid(row=4, column=0, sticky='w', pady=5)
        pet_weight = ttk.Spinbox(form_frame, from_=0.1, to=100.0, increment=0.1, width=18)
        pet_weight.grid(row=4, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Особенности:").grid(row=5, column=0, sticky='w', pady=5)
        pet_notes = tk.Text(form_frame, width=20, height=4)
        pet_notes.grid(row=5, column=1, pady=5, padx=10)
        
        def add_pet():
            name = pet_name.get()
            species = pet_species.get()
            breed = pet_breed.get()
            age = pet_age.get()
            weight = pet_weight.get()
            notes = pet_notes.get("1.0", tk.END).strip()
            
            if not all([name, species, breed, age, weight]):
                messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
                return
            
            try:
                conn = sqlite3.connect('vet_clinic_client.db')
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO client_animals 
                    (client_phone, name, species, breed, age, weight, special_notes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (self.current_user['phone'], name, species, breed, int(age), float(weight), notes)
                )
                conn.commit()
                conn.close()
                
                self.load_user_animals()
                self.update_pets_display()
                dialog.destroy()
                messagebox.showinfo("Успех", "Питомец добавлен!")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении: {str(e)}")
        
        ttk.Button(dialog, text="Добавить", command=add_pet).pack(pady=10)
    
    def delete_pet(self, animal):
        """Удаление питомца"""
        result = messagebox.askyesno("Подтверждение", f"Удалить питомца {animal['name']}?")
        if result:
            conn = sqlite3.connect('vet_clinic_client.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM client_animals WHERE id = ?', (animal['id'],))
            conn.commit()
            conn.close()
            
            self.load_user_animals()
            self.update_pets_display()
            messagebox.showinfo("Успех", "Питомец удален!")
    
    def create_appointments_tab(self, parent):
        """Вкладка записи на прием"""
        self.appointments_frame = parent
        
        ttk.Label(parent, text="Запись на прием в ветлечебницу", 
                 style='Header.TLabel').pack(pady=10)
        
        # Если есть питомцы, показываем форму записи
        if self.user_animals:
            self.show_appointment_form()
        else:
            ttk.Label(parent, text="Сначала добавьте питомца для записи на прием", 
                     font=('Arial', 12)).pack(pady=50)
    
    def show_appointment_form(self, selected_animal=None):
        """Форма записи на прием"""
        form_frame = ttk.LabelFrame(self.appointments_frame, text="Новая запись", padding=15)
        form_frame.pack(fill='x', pady=10)
        
        ttk.Label(form_frame, text="Питомец:").grid(row=0, column=0, sticky='w', pady=5)
        animal_var = tk.StringVar()
        animal_combo = ttk.Combobox(form_frame, textvariable=animal_var, width=20)
        animal_combo['values'] = [animal['name'] for animal in self.user_animals]
        if selected_animal:
            animal_var.set(selected_animal['name'])
        animal_combo.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Услуга:").grid(row=1, column=0, sticky='w', pady=5)
        service_var = tk.StringVar()
        service_combo = ttk.Combobox(form_frame, textvariable=service_var, width=20)
        service_combo['values'] = ["Осмотр", "Вакцинация", "Стерилизация", "Чистка зубов", "Стрижка", "Экстренный прием"]
        service_combo.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Дата:").grid(row=2, column=0, sticky='w', pady=5)
        date_var = tk.StringVar()
        date_entry = ttk.Entry(form_frame, textvariable=date_var, width=20)
        date_entry.grid(row=2, column=1, pady=5, padx=10)
        # Предлагаем ближайшие даты
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_var.set(tomorrow)
        
        ttk.Label(form_frame, text="Время:").grid(row=3, column=0, sticky='w', pady=5)
        time_var = tk.StringVar()
        time_combo = ttk.Combobox(form_frame, textvariable=time_var, width=20)
        time_combo['values'] = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
        time_combo.grid(row=3, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Примечания:").grid(row=4, column=0, sticky='w', pady=5)
        notes_text = tk.Text(form_frame, width=20, height=4)
        notes_text.grid(row=4, column=1, pady=5, padx=10)
        
        def make_appointment():
            animal_name = animal_var.get()
            service = service_var.get()
            date = date_var.get()
            time = time_var.get()
            notes = notes_text.get("1.0", tk.END).strip()
            
            if not all([animal_name, service, date, time]):
                messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
                return
            
            try:
                conn = sqlite3.connect('vet_clinic_client.db')
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO appointments 
                    (client_phone, animal_name, service_type, appointment_date, appointment_time, status, doctor, notes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (self.current_user['phone'], animal_name, service, date, time, 'Ожидание', 'Не назначен', notes)
                )
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Успех", "Запись создана! Ожидайте подтверждения от администратора.")
                form_frame.destroy()
                self.update_appointments_display()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при создании записи: {str(e)}")
        
        ttk.Button(form_frame, text="Записаться", 
                  command=make_appointment).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Показ текущих записей
        self.update_appointments_display()
    
    def show_appointment_dialog(self, animal):
        """Диалог быстрой записи для конкретного животного"""
        self.appointments_frame.destroy()
        self.appointments_frame = ttk.Frame(ttk.Notebook(self.root).winfo_children()[1])  # Получаем вкладку записей
        self.appointments_frame.pack(fill='both', expand=True)
        self.show_appointment_form(animal)
    
    def update_appointments_display(self):
        """Обновление отображения записей"""
        # Загрузка записей пользователя
        conn = sqlite3.connect('vet_clinic_client.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM appointments WHERE client_phone = ? ORDER BY appointment_date DESC', 
            (self.current_user['phone'],)
        )
        appointments = cursor.fetchall()
        conn.close()
        
        # Создание фрейма для отображения записей
        if hasattr(self, 'appointments_list_frame'):
            self.appointments_list_frame.destroy()
        
        self.appointments_list_frame = ttk.LabelFrame(self.appointments_frame, text="Мои записи", padding=10)
        self.appointments_list_frame.pack(fill='both', expand=True, pady=10)
        
        if not appointments:
            ttk.Label(self.appointments_list_frame, text="У вас пока нет записей").pack(pady=20)
            return
        
        for appointment in appointments:
            appt_frame = ttk.Frame(self.appointments_list_frame, relief='solid', padding=10)
            appt_frame.pack(fill='x', pady=5, padx=5)
            
            status_color = '#90EE90' if appointment[6] == 'Подтвержден' else '#FFB6C1'
            appt_frame.configure(style='')
            
            info_text = f"""Животное: {appointment[2]}
Услуга: {appointment[3]}
Дата: {appointment[4]} {appointment[5]}
Статус: {appointment[6]}
Врач: {appointment[7]}"""
            
            if appointment[8]:
                info_text += f"\nПримечания: {appointment[8]}"
            
            ttk.Label(appt_frame, text=info_text, justify='left').pack(anchor='w')
            
            if appointment[6] == 'Ожидание':
                ttk.Button(appt_frame, text="Отменить запись", 
                          command=lambda a=appointment: self.cancel_appointment(a)).pack(anchor='e')
    
    def cancel_appointment(self, appointment):
        """Отмена записи"""
        result = messagebox.askyesno("Подтверждение", "Отменить запись?")
        if result:
            conn = sqlite3.connect('vet_clinic_client.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment[0],))
            conn.commit()
            conn.close()
            
            self.update_appointments_display()
            messagebox.showinfo("Успех", "Запись отменена!")
    
    def create_history_tab(self, parent):
        """Вкладка истории посещений"""
        ttk.Label(parent, text="История посещений и медицинские записи", 
                 style='Header.TLabel').pack(pady=10)
        
        # Демо-история (в реальной системе здесь были бы данные из БД)
        history_data = [
            {"date": "2024-11-15", "animal": "Барсик", "service": "Вакцинация", "doctor": "Др. Смирнова", "diagnosis": "Здоров", "recommendations": "Повторная вакцинация через год"},
            {"date": "2024-09-10", "animal": "Рекс", "service": "Осмотр", "doctor": "Др. Иванов", "diagnosis": "Легкая аллергия", "recommendations": "Сменить корм"},
            {"date": "2024-07-05", "animal": "Барсик", "service": "Стрижка", "doctor": "Др. Петрова", "diagnosis": "-", "recommendations": "Регулярный уход за шерстью"},
        ]
        
        for visit in history_data:
            visit_frame = ttk.LabelFrame(parent, text=f"{visit['date']} - {visit['animal']}", padding=10)
            visit_frame.pack(fill='x', pady=5, padx=10)
            
            visit_text = f"""Услуга: {visit['service']}
Врач: {visit['doctor']}
Диагноз: {visit['diagnosis']}
Рекомендации: {visit['recommendations']}"""
            
            ttk.Label(visit_frame, text=visit_text, justify='left').pack(anchor='w')
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.user_animals = []
        self.create_login_screen()
    
    def clear_screen(self):
        """Очистка экрана"""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = VetClinicClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
