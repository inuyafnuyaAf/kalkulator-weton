from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Data pasaran Jawa dan nilai neptu
pasaran_jawa = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
neptu_hari = {
    "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8,
    "Jumat": 6, "Sabtu": 9, "Minggu": 5
}
neptu_pasaran = {
    "Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8
}

def hitung_weton(tanggal):
    try:
        # Konversi string ke datetime
        tanggal_lahir = datetime.strptime(tanggal, "%Y-%m-%d")
        
        # Ambil hari dalam bahasa Indonesia
        hari_lahir = tanggal_lahir.strftime("%A")
        hari_lahir_id = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }[hari_lahir]

        # Perhitungan pasaran menggunakan rumus yang benar
        selisih_tahun = tanggal_lahir.year - 1800  # Tahun referensi 1800-01-01
        jumlah_hari = selisih_tahun * 365 + (selisih_tahun // 4) + tanggal_lahir.timetuple().tm_yday
        index_pasaran = jumlah_hari % 5
        pasaran = pasaran_jawa[index_pasaran]

        # Hitung neptu
        neptu = neptu_hari[hari_lahir_id] + neptu_pasaran[pasaran]

        return hari_lahir_id, pasaran, neptu
    except ValueError:
        return None, None, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama = request.form["nama"]
        tanggal_lahir = request.form["tanggal"]

        hari, pasaran, neptu = hitung_weton(tanggal_lahir)
        if hari:
            return render_template("hasil.html", nama=nama, tanggal=tanggal_lahir, hari=hari, pasaran=pasaran, neptu=neptu)
        else:
            return render_template("index.html", error="Format tanggal salah! Gunakan format YYYY-MM-DD.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
