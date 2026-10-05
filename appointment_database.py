from datetime import datetime, timedelta
import sqlite3

DB = "clinic.db"


def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'booked',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_doctor_appointment
        ON appointments(doctor, appointment_time)
        WHERE status = 'booked'
    """)

    conn.commit()
    conn.close()

def create_appointment(patient_name, phone, doctor, appointment_time):
    conn = sqlite3.connect(DB)

    cursor = conn.execute("""
        INSERT INTO appointments
            (patient_name, phone, doctor, appointment_time)
        VALUES (?, ?, ?, ?)
    """, (
        patient_name,
        phone,
        doctor,
        appointment_time,
    ))

    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()

    return appointment_id

def get_appointments(doctor=None, status=None):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM appointments WHERE 1=1"
    params = []

    if doctor:
        query += " AND doctor = ?"
        params.append(doctor)

    if status:
        query += " AND status = ?"
        params.append(status)

    cursor.execute(query, params)
    appointments = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return appointments

def postpone_appointment(appointment_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if the appointment exists and is booked
    cursor.execute("""
        SELECT * FROM appointments
        WHERE id = ? AND status = 'booked'
    """, (appointment_id,))
    appointment = dict(cursor.fetchone())

    if not appointment:
        conn.close()
        return False  # Appointment not found or not booked

    new_time = datetime.strptime(
        appointment['appointment_time'],
        "%Y-%m-%d %H:%M:%S"
    ) + timedelta(hours=1)

    # Update the appointment time
    cursor.execute("""
        UPDATE appointments
        SET appointment_time = ?
        WHERE id = ?
    """, (new_time, appointment_id))

    conn.commit()
    conn.close()
    return True

def delete_appointment(appointment_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Check if the appointment exists
    cursor.execute("""
        SELECT * FROM appointments
        WHERE id = ?
    """, (appointment_id,))
    appointment = cursor.fetchone()

    if not appointment:
        conn.close()
        return False  # Appointment not found

    # Delete the appointment
    cursor.execute("""
        DELETE FROM appointments
        WHERE id = ?
    """, (appointment_id,))

    conn.commit()
    conn.close()
    return True