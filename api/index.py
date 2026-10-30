from fastapi import FastAPI
from fastapi.responses import JSONResponse
import csv

app = FastAPI(
    title="Data Wilayah Indonesia — Sumatera Barat",
    description="API lengkap kode & nama provinsi, kabupaten, kecamatan Sumatera Barat",
    version="1.0.0"
)

# Baca CSV tanpa pandas — pakai modul bawaan Python
data = []
try:
    with open("../data_sumatera_barat.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    print(f"Berhasil memuat {len(data)} baris data")
except Exception as e:
    print(f"Error membaca CSV: {e}")
    data = []

@app.get("/", summary="Semua Data Wilayah")
def semua_data():
    return {
        "sumber": "https://emsifa.github.io/api-wilayah-indonesia/api",
        "jumlah": len(data),
        "data": data
    }

@app.get("/kabupaten", summary="Daftar Kabupaten")
def daftar_kabupaten():
    seen = set()
    daftar = []
    for row in data:
        kode = row.get("Kode_Kabupaten", "").strip()
        nama = row.get("Nama_Kabupaten", "").strip()
        if kode and kode not in seen:
            seen.add(kode)
            daftar.append({"Kode_Kabupaten": kode, "Nama_Kabupaten": nama})
    return {"jumlah": len(daftar), "data": daftar}

@app.get("/kecamatan/{kode_kab}", summary="Kecamatan per Kabupaten")
def kecamatan_di_kabupaten(kode_kab: str):
    hasil = []
    nama_kab = ""
    kode_input = kode_kab.strip()
    for row in data:
        if row.get("Kode_Kabupaten", "").strip() == kode_input:
            if not nama_kab:
                nama_kab = row.get("Nama_Kabupaten", "")
            hasil.append({
                "Kode_Kecamatan": row.get("Kode_Kecamatan", ""),
                "Nama_Kecamatan": row.get("Nama_Kecamatan", "")
            })
    if not hasil:
        return JSONResponse({"pesan": "Kode kabupaten tidak ditemukan"}, status_code=404)
    return {
        "kabupaten": nama_kab,
        "jumlah": len(hasil),
        "data": hasil
    }
