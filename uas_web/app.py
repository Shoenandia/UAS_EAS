from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from models import UserModel, StudentModel

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Should be moved to environment variable

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uas_web'

mysql = MySQL(app)

# Initialize models
user_model = UserModel(mysql)
student_model = StudentModel(mysql)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if user_model.add_user(username, email, password):
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Terjadi kesalahan saat registrasi.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = user_model.get_user_by_username(username)
        if user and user_model.verify_password(user[3], password):
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    stats = student_model.get_student_statistics()
    students = student_model.get_all_students()
    return render_template('dashboard.html', students=students, stats=stats)

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        student_data = {
            'nim': request.form['nim'],
            'name': request.form['name'],
            'age': request.form['age'],
            'email': request.form['email'],
            'course': request.form['course'],
            'gpa': request.form['gpa'],
            'nilai': request.form['nilai']
        }
        
        if student_model.add_student(**student_data):
            flash('Data mahasiswa berhasil disimpan!', 'success')
        else:
            flash('Terjadi kesalahan saat menyimpan data.', 'danger')
        return redirect(url_for('students'))
    
    students = student_model.get_all_students()
    return render_template('students.html', students=students)

@app.route('/api/student-stats')
def student_stats():
    stats = student_model.get_student_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)