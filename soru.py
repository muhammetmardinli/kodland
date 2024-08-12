import time
from sqlalchemy.exc import OperationalError
from app import app,Question,db
with app.app_context():
    questions = [
        {"question_text": "Python'da yapay zeka geliştirme için hangi kütüphaneler yaygın olarak kullanılır?",
         "options": ["NumPy", "Pandas", "TensorFlow", "Matplotlib"],
         "correct_option": "TensorFlow"},
        {"question_text": "Python'da yapay zeka geliştirme için hangi kütüphaneler yaygın olarak kullanılır?",
         "options": ["NumPy", "Pandas", "TensorFlow", "Matplotlib"],
         "correct_option": "TensorFlow"},

        {"question_text": "Scikit-learn kütüphanesi genellikle hangi tür yapay zeka modelleri için kullanılır?",
         "options": ["Derin öğrenme", "Makine öğrenmesi", "Doğal dil işleme", "Bilgisayar görüşü"],
         "correct_option": "Makine öğrenmesi"},

        {"question_text": "Bilgisayar görüşü uygulamalarında kullanılan yaygın bir algoritma nedir?",
         "options": ["K-ortalama", "Yapay Sinir Ağları", "Convolutional Neural Networks (CNN)", "Karar Ağaçları"],
         "correct_option": "Convolutional Neural Networks (CNN)"},

        {"question_text": "Hangi kütüphane bilgisayarla görme (computer vision) görevlerini destekler?",
         "options": ["SciPy", "OpenCV", "Seaborn", "NLTK"],
         "correct_option": "OpenCV"},

        {"question_text": "Doğal dil işleme (NLP) alanında kelime gömme (word embedding) için hangi teknik yaygın olarak kullanılır?",
         "options": ["Bag of Words", "TF-IDF", "Word2Vec", "LSTM"],
         "correct_option": "Word2Vec"},

        {"question_text": "Bir metnin özetini çıkarmak için hangi NLP tekniği kullanılır?",
         "options": ["Sınıflandırma", "Özellik Çıkartma", "Özetleme", "Duygu Analizi"],
         "correct_option": "Özetleme"},

        {"question_text": "Keras kütüphanesi hangi Python uygulama türlerinde yaygın olarak kullanılır?",
         "options": ["Web geliştirme", "Veri analizi", "Yapay zeka ve derin öğrenme", "Oyun geliştirme"],
         "correct_option": "Yapay zeka ve derin öğrenme"},

        {"question_text": "Bir yapay zeka modelini Python'da eğitirken modelin performansını değerlendirmek için hangi metrik kullanılır?",
         "options": ["MSE (Mean Squared Error)", "Accuracy", "F1 Score", "Tüm yukarıdaki"],
         "correct_option": "Tüm yukarıdaki"}


        # Diğer sorular buraya eklenebilir
    ]

    for q in questions:
        question = Question(
            question_text=q['question_text'],
            options=q['options'],
            correct_option=q['correct_option']
        )

        attempt = 0
        while attempt < 5:  # Maksimum 5 deneme
            try:
                db.session.add(question)
                db.session.commit()
                break  # Başarılıysa döngüden çık
            except OperationalError as e:
                print(f"Veritabanı hatası: {e}, deneme {attempt + 1}")
                time.sleep(1)  # 1 saniye bekle ve yeniden dene
                attempt += 1





    # Veritabanına ekleme
    for q in questions:
        question = Question(
            question_text=q['question_text'],
            options=q['options'],
            correct_option=q['correct_option']
        )
        db.session.add(question)

    db.session.commit()
