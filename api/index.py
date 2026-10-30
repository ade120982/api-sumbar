from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI(
    title="Data Wilayah Indonesia — Sumatera Barat",
    description="API lengkap kode & nama provinsi, kabupaten, kecamatan Sumatera Barat",
    version="1.0.0"
)

try:
    df = pd.read_csv("../data_sumatera_barat.csv")
    df = df.fillna("")
except Exception as e:
    print(f"Error: {e}")
    df = pd.DataFrame()

@app.get("/", summary="Semua Data Wilayah")
def semua_data():
    data = df.to_dict(orient="records")
    return {
        "sumber": "https://emsifa.github.io/api-wilayah-indonesia/api",
        "jumlah": len(data),
        "data": data
    }

@app.get("/kabupaten", summary="Daftar Kabupaten")
def daftar_kabupaten():
    if df.empty:
        return {"jumlah": 0, "data": []}
    kab = df[["Kode_Kabupaten", "Nama_Kabupaten"]].drop_duplicates()
    return {"jumlah": len(kab), "data": kab.to_dict(orient="records")}

@app.get("/kecamatan/{kode_kab}", summary="Kecamatan per Kabupaten")
def kecamatan_di_kabupaten(kode_kab: str):
    hasil = df[df["Kode_Kabupaten"] == kode_kab]
    if hasil.empty:
        return JSONResponse({"pesan": "Kode kabupaten tidak ditemukan"}, status_code=404)
    return {
        "kabupaten": hasil.iloc[0]["Nama_Kabupaten"],
        "jumlah": len(hasil),
        "data": hasil[["Kode_Kecamatan", "Nama_Kecamatan"]].to_dict(orient="records")
    }
