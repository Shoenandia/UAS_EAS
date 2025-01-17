# models.py
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def add_user(self, username, email, password):
        """Add a new user to the database"""
        try:
            cur = self.mysql.connection.cursor()
            hashed_password = generate_password_hash(password)
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def get_user_by_username(self, username):
        """Get user data by username"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def verify_password(self, stored_password, provided_password):
        """Verify if provided password matches stored hash"""
        return check_password_hash(stored_password, provided_password)

class StudentModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def add_student(self, nim, name, age, email, course, gpa, nilai):
        """Add a new student to the database"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(
                """INSERT INTO students 
                   (nim, name, age, email, course, gpa, nilai) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (nim, name, age, email, course, gpa, nilai)
            )
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    def get_all_students(self):
        """Get all students from database"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            cur.close()
            return students
        except Exception as e:
            print(f"Error getting students: {e}")
            return []

    def get_student_by_nim(self, nim):
        """Get student data by NIM"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT * FROM students WHERE nim = %s", (nim,))
            student = cur.fetchone()
            cur.close()
            return student
        except Exception as e:
            print(f"Error getting student: {e}")
            return None

    def update_student(self, nim, name, age, email, course, gpa, nilai):
        """Update student data"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(
                """UPDATE students 
                   SET name = %s, age = %s, email = %s, 
                       course = %s, gpa = %s, nilai = %s 
                   WHERE nim = %s""",
                (name, age, email, course, gpa, nilai, nim)
            )
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error updating student: {e}")
            return False

    def delete_student(self, nim):
        """Delete student by NIM"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("DELETE FROM students WHERE nim = %s", (nim,))
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

    def get_student_statistics(self):
        """Get statistics about students"""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    AVG(gpa) as avg_gpa,
                    MAX(gpa) as max_gpa,
                    MIN(gpa) as min_gpa,
                    AVG(nilai) as avg_nilai,
                    MAX(nilai) as max_nilai,
                    MIN(nilai) as min_nilai,
                    COUNT(*) as total_students
                FROM students
            """)
            stats = cur.fetchone()
            cur.close()
            return {
                'avg_gpa': float(stats[0]) if stats[0] else 0,
                'max_gpa': float(stats[1]) if stats[1] else 0,
                'min_gpa': float(stats[2]) if stats[2] else 0,
                'avg_nilai': float(stats[3]) if stats[3] else 0,
                'max_nilai': float(stats[4]) if stats[4] else 0,
                'min_nilai': float(stats[5]) if stats[5] else 0,
                'total_students': int(stats[6]) if stats[6] else 0
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return None