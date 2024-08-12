from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    exam_results = db.relationship('ExamResult', backref='student', lazy=True)

class ExamResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    correct_option = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()  # Veritabanı ve tabloları oluştur

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        student_number = request.form.get('student_number')

        if not student_number.isdigit() or len(student_number) != 6:
            flash('Öğrenci numarası 6 haneli bir sayı olmalıdır.')
            return redirect(url_for('index'))

        if not name.replace(" ", "").isalpha():
            flash('İsim sadece harflerden oluşmalıdır.')
            return redirect(url_for('index'))

        if Student.query.filter_by(student_number=student_number).first():
            flash('Bu öğrenci numarası ile sınava zaten giriş yaptınız.')
            return redirect(url_for('index'))

        session['name'] = name
        session['student_number'] = student_number
        return redirect(url_for('quiz'))

    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'student_number' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        score = 0
        questions = Question.query.all()
        for question in questions:
            selected_option = request.form.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1

        # Sınav sonucunu session'a kaydet
        session['score'] = score

        student = Student.query.filter_by(student_number=session['student_number']).first()
        if student:
            exam_result = ExamResult(student_id=student.id, score=score)
            db.session.add(exam_result)
            db.session.commit()

        return redirect(url_for('result'))

    questions = Question.query.all()
    return render_template('quiz.html', questions=questions)

@app.route('/result')
def result():
    # Session'dan score'u al, score yoksa 0 olarak ayarla
    score = session.get('score', 0)

    # En yüksek puanı hesapla
    highest_score_record = ExamResult.query.order_by(ExamResult.score.desc()).first()
    highest_score = highest_score_record.score if highest_score_record else 'Henüz sınav yapılmadı.'

    # Sonrasında session'dan kullanıcı bilgilerini temizleyin
    session.pop('name', None)
    session.pop('student_number', None)
    session.pop('score', None)

    return render_template('result.html',
                           score=score,
                           total_questions=len(Question.query.all()),
                           highest_score=highest_score)

if __name__ == '__main__':
    app.run(debug=True)
