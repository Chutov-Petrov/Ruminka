
import sqlite3
from datetime import datetime
from flask import flask 
app = Flask(__name__)
app.secret_key = "park_secret_key"
DB_NAME = "park.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            min_age INTEGER DEFAULT 0,
            min_height INTEGER DEFAULT 0,
            max_capacity INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT DEFAULT 'active',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            position TEXT NOT NULL,
            phone TEXT,
            hire_date DATE NOT NULL,
            salary REAL NOT NULL,
            attraction_id INTEGER,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (attraction_id) REFERENCES attractions(id)
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_name TEXT NOT NULL,
            attraction_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            visit_date DATE NOT NULL,
            quantity INTEGER DEFAULT 1,
            total_price REAL NOT NULL,
            payment_method TEXT DEFAULT 'cash',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (attraction_id) REFERENCES attractions(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );

        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attraction_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            maintenance_date DATE NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            cost REAL DEFAULT 0,
            status TEXT DEFAULT 'planned',
            FOREIGN KEY (attraction_id) REFERENCES attractions(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );


    """)

    # Seed data if empty
    cursor.execute("SELECT COUNT(*) FROM attractions")
    if cursor.fetchone()[0] == 0:
        cursor.executescript("""
            INSERT INTO attractions (name, category, min_age, min_height, max_capacity, price, description) VALUES
            ('Американские горки', 'Экстрим', 12, 140, 24, 350, 'Захватывающий аттракцион с петлями и резкими спусками'),
            ('Колесо обозрения', 'Семейный', 3, 0, 40, 200, 'Панорамный вид на весь парк с высоты 60 метров'),
            ('Комната страха', 'Развлечение', 14, 0, 10, 250, 'Пугающий лабиринт с актёрами и спецэффектами'),
            ('Карусель', 'Детский', 0, 0, 30, 150, 'Классическая карусель для детей с яркими фигурками'),
            ('Бампер-машинки', 'Семейный', 7, 120, 20, 180, 'Весёлые столкновения на электромобилях'),
            ('Водная горка', 'Активный', 10, 130, 15, 280, 'Скоростной спуск в бассейн с брызгами'),
            ('Лабиринт зеркал', 'Развлечение', 5, 0, 15, 130, 'Запутанный лабиринт из сотен зеркал'),
            ('Батут-арена', 'Детский', 4, 0, 25, 200, 'Большая арена с профессиональными батутами');

            INSERT INTO employees (full_name, position, phone, hire_date, salary, attraction_id) VALUES
            ('Иванов Алексей Петрович', 'Оператор аттракциона', '+7-900-111-22-33', '2022-03-15', 45000, 1),
            ('Смирнова Ольга Николаевна', 'Кассир', '+7-900-222-33-44', '2021-06-01', 38000, NULL),
            ('Козлов Дмитрий Сергеевич', 'Технический специалист', '+7-900-333-44-55', '2020-01-10', 55000, NULL),
            ('Петрова Анна Владимировна', 'Оператор аттракциона', '+7-900-444-55-66', '2023-04-20', 42000, 2),
            ('Новиков Игорь Андреевич', 'Администратор', '+7-900-555-66-77', '2019-09-05', 65000, NULL),
            ('Федорова Мария Ивановна', 'Оператор аттракциона', '+7-900-666-77-88', '2022-07-12', 43000, 4),
            ('Морозов Павел Александрович', 'Охранник', '+7-900-777-88-99', '2021-11-30', 40000, NULL),
            ('Волкова Елена Дмитриевна', 'Оператор аттракциона', '+7-900-888-99-00', '2023-01-15', 42000, 6);

            INSERT INTO tickets (visitor_name, attraction_id, employee_id, visit_date, quantity, total_price, payment_method) VALUES
            ('Сидоров Василий', 1, 2, '2024-06-01', 2, 700, 'card'),
            ('Кузнецова Ирина', 2, 2, '2024-06-01', 3, 600, 'cash'),
            ('Попов Николай', 4, 2, '2024-06-02', 1, 150, 'cash'),
            ('Лебедева Светлана', 6, 2, '2024-06-02', 2, 560, 'card'),
            ('Семёнов Артём', 1, 2, '2024-06-03', 1, 350, 'cash'),
            ('Орлова Надежда', 3, 2, '2024-06-03', 4, 1000, 'card'),
            ('Зайцев Константин', 5, 2, '2024-06-04', 2, 360, 'cash'),
            ('Белова Татьяна', 7, 2, '2024-06-04', 3, 390, 'card');

            INSERT INTO maintenance (attraction_id, employee_id, maintenance_date, type, description, cost, status) VALUES
            (1, 3, '2024-05-15', 'Плановое ТО', 'Проверка рельс, тормозной системы и ремней безопасности', 15000, 'completed'),
            (6, 3, '2024-05-20', 'Ремонт', 'Замена насоса водяной системы', 8500, 'completed'),
            (2, 3, '2024-06-10', 'Плановое ТО', 'Смазка подшипников и проверка электросистемы', 5000, 'planned'),
            (4, 3, '2024-06-05', 'Осмотр', 'Плановый визуальный осмотр механизмов', 0, 'completed');

    
        """)
        conn.commit()

    conn.close()


# ---- ГЛАВНАЯ ----
@app.route("/")
def index():
    conn = get_db()
    stats = {
        "attractions": conn.execute("SELECT COUNT(*) FROM attractions WHERE status='active'").fetchone()[0],
        "employees": conn.execute("SELECT COUNT(*) FROM employees WHERE status='active'").fetchone()[0],
        "tickets_today": conn.execute("SELECT COUNT(*) FROM tickets WHERE visit_date=date('now')").fetchone()[0],
        "revenue_today": conn.execute("SELECT COALESCE(SUM(total_price),0) FROM tickets WHERE visit_date=date('now')").fetchone()[0],
        "maintenance_planned": conn.execute("SELECT COUNT(*) FROM maintenance WHERE status='planned'").fetchone()[0],
    }
    recent_tickets = conn.execute("""
        SELECT t.*, a.name as attr_name FROM tickets t
        JOIN attractions a ON t.attraction_id = a.id
        ORDER BY t.created_at DESC LIMIT 5
    """).fetchall()
    conn.close()
    return render_template("index.html", stats=stats, recent_tickets=recent_tickets)


# ---- АТТРАКЦИОНЫ ----
@app.route("/attractions")
def attractions():
    conn = get_db()
    rows = conn.execute("SELECT * FROM attractions ORDER BY category, name").fetchall()
    conn.close()
    return render_template("attractions.html", attractions=rows)

@app.route("/attractions/add", methods=["GET", "POST"])
def add_attraction():
    if request.method == "POST":
        conn = get_db()
        conn.execute("""INSERT INTO attractions (name, category, min_age, min_height, max_capacity, price, status, description)
                        VALUES (?,?,?,?,?,?,?,?)""",
                     (request.form["name"], request.form["category"], request.form["min_age"],
                      request.form["min_height"], request.form["max_capacity"], request.form["price"],
                      request.form["status"], request.form["description"]))
        conn.commit(); conn.close()
        flash("Аттракцион добавлен!", "success")
        return redirect(url_for("attractions"))
    return render_template("attraction_form.html", attraction=None)

@app.route("/attractions/edit/<int:id>", methods=["GET", "POST"])
def edit_attraction(id):
    conn = get_db()
    if request.method == "POST":
        conn.execute("""UPDATE attractions SET name=?, category=?, min_age=?, min_height=?,
                        max_capacity=?, price=?, status=?, description=? WHERE id=?""",
                     (request.form["name"], request.form["category"], request.form["min_age"],
                      request.form["min_height"], request.form["max_capacity"], request.form["price"],
                      request.form["status"], request.form["description"], id))
        conn.commit(); conn.close()
        flash("Данные обновлены!", "success")
        return redirect(url_for("attractions"))
    row = conn.execute("SELECT * FROM attractions WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("attraction_form.html", attraction=row)

@app.route("/attractions/delete/<int:id>")
def delete_attraction(id):
    conn = get_db()
    conn.execute("UPDATE attractions SET status='inactive' WHERE id=?", (id,))
    conn.commit(); conn.close()
    flash("Аттракцион деактивирован.", "info")
    return redirect(url_for("attractions"))


# ---- СОТРУДНИКИ ----
@app.route("/employees")
def employees():
    conn = get_db()
    rows = conn.execute("""SELECT e.*, a.name as attr_name FROM employees e
                           LEFT JOIN attractions a ON e.attraction_id = a.id
                           ORDER BY e.position, e.full_name""").fetchall()
    conn.close()
    return render_template("employees.html", employees=rows)

@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    conn = get_db()
    if request.method == "POST":
        conn.execute("""INSERT INTO employees (full_name, position, phone, hire_date, salary, attraction_id)
                        VALUES (?,?,?,?,?,?)""",
                     (request.form["full_name"], request.form["position"], request.form["phone"],
                      request.form["hire_date"], request.form["salary"],
                      request.form["attraction_id"] or None))
        conn.commit(); conn.close()
        flash("Сотрудник добавлен!", "success")
        return redirect(url_for("employees"))
    attractions = conn.execute("SELECT id, name FROM attractions WHERE status='active'").fetchall()
    conn.close()
    return render_template("employee_form.html", employee=None, attractions=attractions)

@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    conn = get_db()
    if request.method == "POST":
        conn.execute("""UPDATE employees SET full_name=?, position=?, phone=?, hire_date=?,
                        salary=?, attraction_id=?, status=? WHERE id=?""",
                     (request.form["full_name"], request.form["position"], request.form["phone"],
                      request.form["hire_date"], request.form["salary"],
                      request.form["attraction_id"] or None, request.form["status"], id))
        conn.commit(); conn.close()
        flash("Данные обновлены!", "success")
        return redirect(url_for("employees"))
    emp = conn.execute("SELECT * FROM employees WHERE id=?", (id,)).fetchone()
    attractions = conn.execute("SELECT id, name FROM attractions WHERE status='active'").fetchall()
    conn.close()
    return render_template("employee_form.html", employee=emp, attractions=attractions)


# ---- БИЛЕТЫ ----
@app.route("/tickets")
def tickets():
    conn = get_db()
    rows = conn.execute("""SELECT t.*, a.name as attr_name, e.full_name as emp_name
                           FROM tickets t JOIN attractions a ON t.attraction_id=a.id
                           JOIN employees e ON t.employee_id=e.id
                           ORDER BY t.created_at DESC""").fetchall()
    conn.close()
    return render_template("tickets.html", tickets=rows)

@app.route("/tickets/add", methods=["GET", "POST"])
def add_ticket():
    conn = get_db()
    if request.method == "POST":
        qty = int(request.form["quantity"])
        price = conn.execute("SELECT price FROM attractions WHERE id=?", (request.form["attraction_id"],)).fetchone()[0]
        total = qty * price
        conn.execute("""INSERT INTO tickets (visitor_name, attraction_id, employee_id, visit_date, quantity, total_price, payment_method)
                        VALUES (?,?,?,?,?,?,?)""",
                     (request.form["visitor_name"], request.form["attraction_id"],
                      request.form["employee_id"], request.form["visit_date"],
                      qty, total, request.form["payment_method"]))
        conn.commit(); conn.close()
        flash(f"Билет продан! Итого: {total} ₽", "success")
        return redirect(url_for("tickets"))
    attractions = conn.execute("SELECT id, name, price FROM attractions WHERE status='active'").fetchall()
    employees = conn.execute("SELECT id, full_name FROM employees WHERE status='active'").fetchall()
    today = datetime.now().strftime("%Y-%m-%d")
    conn.close()
    return render_template("ticket_form.html", attractions=attractions, employees=employees, today=today)


# ---- ТЕХОБСЛУЖИВАНИЕ ----
@app.route("/maintenance")
def maintenance():
    conn = get_db()
    rows = conn.execute("""SELECT m.*, a.name as attr_name, e.full_name as emp_name
                           FROM maintenance m JOIN attractions a ON m.attraction_id=a.id
                           JOIN employees e ON m.employee_id=e.id
                           ORDER BY m.maintenance_date DESC""").fetchall()
    conn.close()
    return render_template("maintenance.html", maintenance=rows)

@app.route("/maintenance/add", methods=["GET", "POST"])
def add_maintenance():
    conn = get_db()
    if request.method == "POST":
        conn.execute("""INSERT INTO maintenance (attraction_id, employee_id, maintenance_date, type, description, cost, status)
                        VALUES (?,?,?,?,?,?,?)""",
                     (request.form["attraction_id"], request.form["employee_id"],
                      request.form["maintenance_date"], request.form["type"],
                      request.form["description"], request.form["cost"], request.form["status"]))
        conn.commit(); conn.close()
        flash("Запись ТО добавлена!", "success")
        return redirect(url_for("maintenance"))
    attractions = conn.execute("SELECT id, name FROM attractions").fetchall()
    employees = conn.execute("SELECT id, full_name FROM employees WHERE position='Технический специалист'").fetchall()
    if not employees:
        employees = conn.execute("SELECT id, full_name FROM employees").fetchall()
    today = datetime.now().strftime("%Y-%m-%d")
    conn.close()
    return render_template("maintenance_form.html", attractions=attractions, employees=employees, today=today)

@app.route("/maintenance/complete/<int:id>")
def complete_maintenance(id):
    conn = get_db()
    conn.execute("UPDATE maintenance SET status='completed' WHERE id=?", (id,))
    conn.commit(); conn.close()
    flash("ТО отмечено как выполненное.", "success")
    return redirect(url_for("maintenance"))



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
