from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import random

app = Flask(__name__)
app.secret_key = 'rahasia-anak-pintar'  # Change this to a random secret key for production

# --- Main Routes ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Calistung Module ---
@app.route('/calistung')
def calistung_menu():
    return render_template('calistung/menu.html')

@app.route('/calistung/huruf')
def calistung_huruf():
    # Menyiapkan data huruf A-Z untuk template
    huruf_list = [chr(i) for i in range(65, 91)] # A-Z
    kata_dict = {
        'A': 'Apel', 'B': 'Bola', 'C': 'Ceri', 'D': 'Dinosaurus', 'E': 'Elang',
        'F': 'Foto', 'G': 'Gajah', 'H': 'Harimau', 'I': 'Ikan', 'J': 'Jerapah',
        'K': 'Kuda', 'L': 'Lemon', 'M': 'Monyet', 'N': 'Nanas', 'O': 'Obor',
        'P': 'Pisang', 'Q': 'Queen', 'R': 'Rumah', 'S': 'Semangka', 'T': 'Topi',
        'U': 'Ular', 'V': 'Vas', 'W': 'Wortel', 'X': 'Xylofon', 'Y': 'Yoyo', 'Z': 'Zebra'
    }
    return render_template('calistung/huruf.html', huruf_list=huruf_list, kata_dict=kata_dict)

@app.route('/calistung/angka', methods=['GET', 'POST'])
def calistung_angka():
    if 'score' not in session:
        session['score'] = 0
        
    mensaje = None
    if request.method == 'POST':
        try:
            jawaban_user = int(request.form.get('jawaban'))
            jawaban_benar = int(request.form.get('kunci_jawaban'))
            
            if jawaban_user == jawaban_benar:
                session['score'] += 10
                mensaje = ("Benar! Hebat!", "success")
            else:
                mensaje = (f"Yah, kurang tepat. Jawabannya {jawaban_benar}.", "warning")
        except ValueError:
            mensaje = ("Masukkan angka ya!", "danger")

    # Generate soal baru
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operator = random.choice(['+', '-'])
    
    if operator == '-':
        # Pastikan tidak negatif untuk anak-anak
        if a < b: a, b = b, a
        jawaban = a - b
    else:
        jawaban = a + b
        
    soal = f"{a} {operator} {b} = ?"
    
    return render_template('calistung/angka.html', 
                           soal=soal, 
                           kunci_jawaban=jawaban, 
                           score=session['score'], 
                           mensaje=mensaje)

# --- English Module ---
@app.route('/english')
def english_menu():
    return render_template('english/menu.html')

@app.route('/english/animals')
def english_animals():
    # Dictionary: English Word -> Indonesian Meaning
    data_dict = {
        'Cat': 'Kucing', 'Dog': 'Anjing', 'Bird': 'Burung', 'Fish': 'Ikan',
        'Elephant': 'Gajah', 'Lion': 'Singa', 'Tiger': 'Harimau', 'Monkey': 'Monyet',
        'Rabbit': 'Kelinci', 'Chicken': 'Ayam', 'Duck': 'Bebek', 'Cow': 'Sapi',
        'Sheep': 'Domba', 'Horse': 'Kuda', 'Snake': 'Ular', 'Bear': 'Beruang',
        'Zebra': 'Zebra', 'Giraffe': 'Jerapah', 'Crocodile': 'Buaya', 'Turtle': 'Kura-kura'
    }
    return render_template('english/vocab.html', title="Animals 🐱", data_dict=data_dict, color_theme="info")

@app.route('/english/fruits')
def english_fruits():
    # Dictionary: English Word -> Indonesian Meaning
    data_dict = {
        'Apple': 'Apel', 'Banana': 'Pisang', 'Orange': 'Jeruk', 'Grape': 'Anggur',
        'Mango': 'Mangga', 'Strawberry': 'Stroberi', 'Watermelon': 'Semangka', 'Pineapple': 'Nanas',
        'Papaya': 'Pepaya', 'Avocado': 'Alpukat', 'Cherry': 'Ceri', 'Lemon': 'Lemon',
        'Coconut': 'Kelapa', 'Durian': 'Durian', 'Kiwi': 'Kiwi', 'Melon': 'Melon',
        'Pear': 'Pir', 'Peach': 'Persik', 'Plum': 'Plum', 'Guava': 'Jambu'
    }
    return render_template('english/vocab.html', title="Fruits 🍎", data_dict=data_dict, color_theme="warning")

# --- Arabic Module ---
@app.route('/arabic')
def arabic_menu():
    return render_template('arabic/menu.html')

@app.route('/arabic/angka')
def arabic_angka():
    # Dictionary: Arabic Numeral/Text -> Latin Pronunciation
    # Format: Key (to display on card) -> Value (Latin pronunciation + Arabic script in modal)
    
    # We will pass a list of dicts for more control or just a simple dict
    # Let's use two lists zipped or a list of objects for easier template handling
    # But to keep consistent with 'dictionary' request:
    
    # Key = Number (1-10), Value = Tuple (Latin, Arabic Script)
    angka_dict = {
        '1': ('Wahidun', 'وَاحِدٌ'),
        '2': ('Itsnani', 'اِثْنَانِ'),
        '3': ('Tsalasatun', 'ثَلَاثَةٌ'),
        '4': ('Arbaatun', 'أَرْبَعَةٌ'),
        '5': ('Khamsatun', 'خَمْسَةٌ'),
        '6': ('Sittatun', 'سِتَّةٌ'),
        '7': ('Sabatun', 'سَبْعَةٌ'),
        '8': ('Samaniyatun', 'ثَمَانِيَةٌ'),
        '9': ('Tisatun', 'تِسْعَةٌ'),
        '10': ('Asharatun', 'عَشَرَةٌ')
    }
    return render_template('arabic/angka.html', angka_dict=angka_dict)

if __name__ == '__main__':
    app.run(debug=True)
