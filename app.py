import os
import sqlite3
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. BOOKS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        genre TEXT NOT NULL,
        total_copies INTEGER NOT NULL DEFAULT 1,
        available_copies INTEGER NOT NULL DEFAULT 1,
        published_year INTEGER NOT NULL,
        shelf_location TEXT NOT NULL
    );
    """)

    # 2. MEMBERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        membership_type TEXT NOT NULL DEFAULT 'Student',
        join_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Active'
    );
    """)

    # 3. BORROW RECORDS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow_records (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        status TEXT NOT NULL DEFAULT 'Issued',
        fine_amount REAL DEFAULT 0.0,
        FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
    );
    """)

    # 4. FINES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fines (
        fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_status TEXT NOT NULL DEFAULT 'Unpaid',
        paid_date TEXT,
        FOREIGN KEY (issue_id) REFERENCES borrow_records(issue_id) ON DELETE CASCADE
    );
    """)

    # Check if empty, seed initial data
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    sample_books = [
        ('Clean Code: Handbook of Agile Craftsmanship', 'Robert C. Martin', '978-0132350884', 'Computer Science', 5, 3, 2008, 'CS-A1'),
        ('The Pragmatic Programmer: Your Journey', 'Andrew Hunt, David Thomas', '978-0135957059', 'Computer Science', 4, 3, 2019, 'CS-A2'),
        ('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', 'Computer Science', 6, 5, 2009, 'CS-B1'),
        ('Database System Concepts', 'Abraham Silberschatz', '978-0073523323', 'Computer Science', 5, 4, 2019, 'CS-B2'),
        ('To Kill a Mockingbird', 'Harper Lee', '978-0061120084', 'Fiction', 4, 4, 1960, 'LIT-F1'),
        ('1984', 'George Orwell', '978-0451524935', 'Fiction', 5, 2, 1949, 'LIT-F2'),
        ('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', '978-0062316097', 'History', 4, 3, 2014, 'HIST-H1'),
        ('A Brief History of Time', 'Stephen Hawking', '978-0553380163', 'Science', 3, 3, 1988, 'SCI-S1'),
        ('Atomic Habits', 'James Clear', '978-0735211292', 'Self-Help', 6, 4, 2018, 'BUS-M1'),
        ('Principles: Life and Work', 'Ray Dalio', '978-1501124020', 'Business', 3, 3, 2017, 'BUS-M2')
    ]
    cursor.executemany(
        "INSERT INTO books (title, author, isbn, genre, total_copies, available_copies, published_year, shelf_location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        sample_books
    )

    sample_members = [
        ('Aarav Sharma', 'aarav.sharma@example.com', '+91 9876543210', 'Student', '2025-01-10', 'Active'),
        ('Diya Patel', 'diya.patel@example.com', '+91 9876543211', 'Student', '2025-02-15', 'Active'),
        ('Dr. Ramesh Kulkarni', 'ramesh.kulkarni@example.com', '+91 9876543212', 'Faculty', '2024-08-01', 'Active'),
        ('Sneha Deshmukh', 'sneha.deshmukh@example.com', '+91 9876543213', 'Premium', '2025-03-05', 'Active'),
        ('Vikram Mehta', 'vikram.mehta@example.com', '+91 9876543214', 'General', '2024-11-20', 'Active')
    ]
    cursor.executemany(
        "INSERT INTO members (name, email, phone, membership_type, join_date, status) VALUES (?, ?, ?, ?, ?, ?)",
        sample_members
    )

    sample_borrows = [
        (1, 1, '2026-08-01', '2026-08-15', None, 'Overdue', 20.0),
        (1, 2, '2026-08-10', '2026-08-24', None, 'Issued', 0.0),
        (2, 3, '2026-08-05', '2026-08-19', None, 'Issued', 0.0),
        (6, 4, '2026-07-15', '2026-07-29', '2026-07-28', 'Returned', 0.0),
        (6, 1, '2026-08-02', '2026-08-16', None, 'Overdue', 10.0),
        (6, 5, '2026-08-12', '2026-08-26', None, 'Issued', 0.0),
        (9, 2, '2026-08-08', '2026-08-22', None, 'Issued', 0.0),
        (9, 3, '2026-08-11', '2026-08-25', None, 'Issued', 0.0)
    ]
    cursor.executemany(
        "INSERT INTO borrow_records (book_id, member_id, issue_date, due_date, return_date, status, fine_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
        sample_borrows
    )

    sample_fines = [
        (1, 20.0, 'Unpaid', None),
        (5, 10.0, 'Unpaid', None)
    ]
    cursor.executemany(
        "INSERT INTO fines (issue_id, amount, payment_status, paid_date) VALUES (?, ?, ?, ?)",
        sample_fines
    )

init_db()

@app.route("/")
def index():
    return render_template("library.html")

# ----------------- DASHBOARD ANALYTICS API ----------------- #

@app.route("/api/dashboard-stats", methods=["GET"])
def dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Books metrics
    cursor.execute("SELECT COUNT(*) as total_titles, COALESCE(SUM(total_copies), 0) as total_inventory, COALESCE(SUM(available_copies), 0) as available_copies FROM books")
    book_stats = dict(cursor.fetchone())
    book_stats["borrowed_copies"] = book_stats["total_inventory"] - book_stats["available_copies"]

    # Members metrics
    cursor.execute("SELECT COUNT(*) as total_members, SUM(CASE WHEN status='Active' THEN 1 ELSE 0 END) as active_members FROM members")
    member_stats = dict(cursor.fetchone())

    # Circulation metrics
    cursor.execute("""
    SELECT 
        COUNT(*) as total_issues,
        SUM(CASE WHEN status='Issued' THEN 1 ELSE 0 END) as active_issues,
        SUM(CASE WHEN status='Overdue' THEN 1 ELSE 0 END) as overdue_issues,
        SUM(CASE WHEN status='Returned' THEN 1 ELSE 0 END) as returned_issues
    FROM borrow_records
    """)
    circulation_stats = dict(cursor.fetchone())

    # Fines metrics
    cursor.execute("""
    SELECT 
        COALESCE(SUM(CASE WHEN payment_status='Unpaid' THEN amount ELSE 0 END), 0) as unpaid_fines,
        COALESCE(SUM(CASE WHEN payment_status='Paid' THEN amount ELSE 0 END), 0) as collected_fines
    FROM fines
    """)
    fines_stats = dict(cursor.fetchone())

    # Genre breakdown
    cursor.execute("""
    SELECT genre, COUNT(*) as titles_count, SUM(total_copies) as total_copies, SUM(available_copies) as available_copies
    FROM books
    GROUP BY genre
    ORDER BY total_copies DESC
    """)
    genre_stats = [dict(r) for r in cursor.fetchall()]

    # Recent borrow activity
    cursor.execute("""
    SELECT br.issue_id, b.title as book_title, m.name as member_name, br.issue_date, br.due_date, br.status
    FROM borrow_records br
    JOIN books b ON br.book_id = b.book_id
    JOIN members m ON br.member_id = m.member_id
    ORDER BY br.issue_id DESC
    LIMIT 6
    """)
    recent_activity = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return jsonify({
        "book_stats": book_stats,
        "member_stats": member_stats,
        "circulation_stats": circulation_stats,
        "fines_stats": fines_stats,
        "genre_stats": genre_stats,
        "recent_activity": recent_activity
    })

# ----------------- BOOKS API ----------------- #

@app.route("/api/books", methods=["GET"])
def get_books():
    genre = request.args.get("genre", "").strip()
    search = request.args.get("search", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if genre:
        query += " AND genre = ?"
        params.append(genre)
    if search:
        query += " AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY book_id ASC"
    cursor.execute(query, params)
    books = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"books": books, "count": len(books)})

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, isbn, genre, total_copies, available_copies, published_year, shelf_location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("title"),
            data.get("author"),
            data.get("isbn"),
            data.get("genre"),
            int(data.get("total_copies", 1)),
            int(data.get("total_copies", 1)), # initially available = total
            int(data.get("published_year", 2024)),
            data.get("shelf_location", "A1")
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Book added successfully!"})
    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Book with this ISBN already exists: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books 
            SET title=?, author=?, isbn=?, genre=?, total_copies=?, available_copies=?, published_year=?, shelf_location=?
            WHERE book_id=?
        """, (
            data.get("title"),
            data.get("author"),
            data.get("isbn"),
            data.get("genre"),
            int(data.get("total_copies")),
            int(data.get("available_copies")),
            int(data.get("published_year")),
            data.get("shelf_location"),
            book_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Book updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Book deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------- MEMBERS API ----------------- #

@app.route("/api/members", methods=["GET"])
def get_members():
    search = request.args.get("search", "").strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM members WHERE 1=1"
    params = []
    if search:
        query += " AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY member_id ASC"
    cursor.execute(query, params)
    members = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"members": members, "count": len(members)})

@app.route("/api/members", methods=["POST"])
def add_member():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO members (name, email, phone, membership_type, join_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("membership_type", "Student"),
            data.get("join_date", today),
            data.get("status", "Active")
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Member registered successfully!"})
    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Member with this email already exists: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/members/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE members 
            SET name=?, email=?, phone=?, membership_type=?, status=?
            WHERE member_id=?
        """, (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("membership_type"),
            data.get("status"),
            member_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Member updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE member_id=?", (member_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Member removed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------- CIRCULATION (ISSUE / RETURN) API ----------------- #

@app.route("/api/borrow-records", methods=["GET"])
def get_borrow_records():
    status_filter = request.args.get("status", "").strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        br.issue_id,
        br.book_id,
        b.title AS book_title,
        b.isbn,
        br.member_id,
        m.name AS member_name,
        m.email AS member_email,
        br.issue_date,
        br.due_date,
        br.return_date,
        br.status,
        br.fine_amount
    FROM borrow_records br
    JOIN books b ON br.book_id = b.book_id
    JOIN members m ON br.member_id = m.member_id
    WHERE 1=1
    """
    params = []
    if status_filter and status_filter != 'All':
        query += " AND br.status = ?"
        params.append(status_filter)

    query += " ORDER BY br.issue_id DESC"
    cursor.execute(query, params)
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"records": records, "count": len(records)})

@app.route("/api/borrow", methods=["POST"])
def issue_book():
    data = request.json
    book_id = data.get("book_id")
    member_id = data.get("member_id")
    due_days = int(data.get("due_days", 14))

    if not book_id or not member_id:
        return jsonify({"error": "Book and Member are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Check book stock
    cursor.execute("SELECT available_copies, title FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()
    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404
    if book["available_copies"] <= 0:
        conn.close()
        return jsonify({"error": f"No available copies of '{book['title']}' in stock."}), 400

    # 2. Check member status
    cursor.execute("SELECT status, name FROM members WHERE member_id=?", (member_id,))
    member = cursor.fetchone()
    if not member:
        conn.close()
        return jsonify({"error": "Member not found"}), 404
    if member["status"] != "Active":
        conn.close()
        return jsonify({"error": f"Member '{member['name']}' is not Active."}), 400

    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")

    try:
        # Decrement book available copies
        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
        # Insert borrow record
        cursor.execute("""
            INSERT INTO borrow_records (book_id, member_id, issue_date, due_date, status, fine_amount)
            VALUES (?, ?, ?, ?, 'Issued', 0.0)
        """, (book_id, member_id, issue_date, due_date))

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"Book issued successfully! Due on {due_date}."})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/api/return/<int:issue_id>", methods=["POST"])
def return_book(issue_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM borrow_records WHERE issue_id=?", (issue_id,))
    record = cursor.fetchone()
    if not record:
        conn.close()
        return jsonify({"error": "Borrow record not found"}), 404
    if record["status"] == "Returned":
        conn.close()
        return jsonify({"error": "This book is already returned."}), 400

    return_date = datetime.now().strftime("%Y-%m-%d")
    due_date_str = record["due_date"]
    
    # Calculate overdue fine (₹10/day overdue)
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    return_dt = datetime.strptime(return_date, "%Y-%m-%d")
    
    fine_amount = 0.0
    if return_dt > due_date:
        overdue_days = (return_dt - due_date).days
        fine_amount = overdue_days * 10.0

    try:
        # Increase book copies
        cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id=?", (record["book_id"],))
        # Update borrow record
        cursor.execute("""
            UPDATE borrow_records 
            SET return_date=?, status='Returned', fine_amount=?
            WHERE issue_id=?
        """, (return_date, fine_amount, issue_id))

        # Create fine record if applicable
        if fine_amount > 0:
            cursor.execute("""
                INSERT INTO fines (issue_id, amount, payment_status)
                VALUES (?, ?, 'Unpaid')
            """, (issue_id, fine_amount))

        conn.commit()
        conn.close()

        msg = f"Book returned successfully."
        if fine_amount > 0:
            msg += f" Overdue fine generated: ₹{fine_amount}."
        return jsonify({"success": True, "message": msg, "fine_amount": fine_amount})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500

# ----------------- FINES API ----------------- #

@app.route("/api/fines", methods=["GET"])
def get_fines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        f.fine_id,
        f.issue_id,
        f.amount,
        f.payment_status,
        f.paid_date,
        b.title AS book_title,
        m.name AS member_name,
        m.email AS member_email,
        br.due_date,
        br.return_date
    FROM fines f
    JOIN borrow_records br ON f.issue_id = br.issue_id
    JOIN books b ON br.book_id = b.book_id
    JOIN members m ON br.member_id = m.member_id
    ORDER BY f.fine_id DESC
    """)
    fines = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"fines": fines, "count": len(fines)})

@app.route("/api/fines/pay/<int:fine_id>", methods=["POST"])
def pay_fine(fine_id):
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fines 
            SET payment_status='Paid', paid_date=?
            WHERE fine_id=?
        """, (today, fine_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Fine payment recorded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------- LIVE SQL CONSOLE API ----------------- #

@app.route("/api/execute-sql", methods=["POST"])
def execute_sql():
    sql_text = request.json.get("query", "").strip()
    if not sql_text:
        return jsonify({"error": "Query cannot be empty"}), 400

    start_time = time.time()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        statements = [s.strip() for s in sql_text.split(";") if s.strip()]
        last_columns = []
        last_rows = []
        is_select = False
        total_affected = 0

        for stmt in statements:
            cursor.execute(stmt)
            if stmt.strip().upper().startswith("SELECT") or stmt.strip().upper().startswith("PRAGMA") or stmt.strip().upper().startswith("WITH"):
                is_select = True
                if cursor.description:
                    last_columns = [desc[0] for desc in cursor.description]
                    last_rows = [list(r) for r in cursor.fetchall()]
            else:
                total_affected += cursor.rowcount

        conn.commit()
        conn.close()
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return jsonify({
            "success": True,
            "is_select": is_select,
            "columns": last_columns,
            "rows": last_rows,
            "row_count": len(last_rows) if is_select else total_affected,
            "execution_time_ms": elapsed_ms,
            "message": f"Query executed successfully in {elapsed_ms}ms." if is_select else f"Operation successful. Rows affected: {total_affected} ({elapsed_ms}ms)"
        })
    except Exception as e:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return jsonify({
            "success": False,
            "error": str(e),
            "execution_time_ms": elapsed_ms
        }), 400

@app.route("/api/reset-db", methods=["POST"])
def reset_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS fines")
        cursor.execute("DROP TABLE IF EXISTS borrow_records")
        cursor.execute("DROP TABLE IF EXISTS members")
        cursor.execute("DROP TABLE IF EXISTS books")
        conn.commit()
        conn.close()
        init_db()
        return jsonify({"success": True, "message": "Library database reset to initial sample records successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("==========================================================")
    print("  Library Management System DBMS Server running!")
    print("  Local URL: http://127.0.0.1:5000")
    print("==========================================================")
    app.run(debug=True, host="0.0.0.0", port=5000)
