import json
import os
import time
import random
from datetime import datetime
from prettytable import PrettyTable
import pwinput

FileUser = "users.json"
FileJadwall = "jadwal.json"
FileTrx = "transaksi.json"

KelasTiket = ("Ekonomi", "Bisnis", "Eksluksif")
topupsaldo = ""
Akundefault = [{"username": "admin", "password": "admin123", "role": "admin", "saldo": 0}]
JadwalTiket = [
    {"Tiket": "T01", "nama": "Majapahit", "Dari": "Malang", "Tujuan": "Pasar Senen PP", "Jam": "09:45", "kelas": "Bisnis", "harga": 450000, "stok": 25},
    {"Tiket": "T02", "nama": "Lodaya", "Dari": "Solo Balapan", "Tujuan": "Bandung PP", "Jam": "12:15", "Kelas": "Eksluksif", "harga": 610000, "stok": 35},
    {"Tiket": "T03", "nama": "Malabar", "Dari": "Malang", "Tujuan": "Bandung PP", "Jam": "08:30", "Kelas": "Ekonomi", "harga": 200000, "stok": 10},
    {"Tiket": "T04", "nama": "Taksaka", "Dari": "Yogyakarta", "Tujuan": "Gambir PP", "Jam": "15:00", "Kelas": "Eksluksif", "harga": 710000, "stok": 50},
    {"Tiket": "T05", "nama": "Ambarawa Ekspres", "Dari": "Semarang Poncol", "Tujuan": "Surabaya Pasarturi PP", "Jam": "13:20", "kelas": "Bisnis", "harga": 350000, "stok":25},
    {"Tiket": "T06", "nama": "Ciremai", "Dari": "Bandung", "Tujuan": "Semarang Tawang PP", "Jam": "07:00", "kelas": "Ekonomi", "harga": 150000, "stok": 32},
]

def cleanterminal():
    os.system("cls" if os.name == "nt" else "clear")

def savedata(namafilee, data):
    try:
        with open(namafilee, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Erorr, data gak kesimpan ke file.....")
        return False
 
def slow(detik=2):
    time.sleep(detik)

def detekinput(wm):
    while True:
        teks = input(wm).strip()
        try:
            if teks:
                return teks
            raise ValueError("Input gak boleh kosong :) ")
        except ValueError as e:
            print(e)

def konfirmasi(ipanbencib):
    while True:
        jawab = input(f"{ipanbencib} (y/n): ").lower()
        try: 
            if jawab in ("y", "n"):
                return jawab == "y"
            raise ValueError("Ketik y atau n saja...")
        except ValueError as p:
           print(p)

def rupiah(angka):
    return "Rp{:,}".format(angka).replace(",", ".")

def deteksiuser(daftar, key, nilai):
    for item in daftar:
        if item[key] == nilai:
            return item
    return None

# Menu
def tampilanJadwal(jadwal):
    if not jadwal:
        print("Jadwal belum ada....")
        return
    tabel = PrettyTable(["Tiket", "Kereta", "Dari", "Tujuan", "Jam", "Kelas", "Harga", "Stok"])
    for m in jadwal:
       tabel.add_row([["Tiket"], m["nama"], m["Dari"], m["Tujuan"], m["jam"], m["kelas"], rupiah(m["harga"]), m["stok"]])
    print(tabel)

def transaksi(bayar):
    if not bayar:
        print("Belum ada transaksi....")
        return
    tabel = PrettyTable(["Tiket", "Waktu", "User", "Kereta", "Jumlah", "Total"])
    for t in bayar:
        tabel.add_row([t["Tiket"], t["waktu"], t["username"], t["kereta"], t["jumlah"], rupiah(t["total"])])
    print(tabel)

def invoice(trx):
    print("\n ===========================")
    print("   INVOICE TIKET KERETA API")
    print("===========================")
    print(f"Tiket Transaksi : {trx['Tiket']}")
    print(f"Waktu          : {trx['waktu']}")
    print(f"Penumpang      : {trx['username']}")
    print(f"Kereta         : {trx['kereta']} ({trx['kelas']})")
    print(f"Rute           : {trx['Dari']} -> {trx['tujuan']}")
    print(f"Jam            : {trx['jam']}")
    print(f"Jumlah Tiket   : {trx['jumlah']}")
    print(f"Total Bayar    : {rupiah(trx['total'])}")
    print("===========================")

#  Auth
def registrasi(users):
    print("=== REGISTRASI ===")
    try:
        username = input("Masukkan username (min 5 karakter): ")
        if username == "":
            raise ValueError("Username tidak boleh kosong....")
        if len(username) < 5:
            raise ValueError("Username minimal 5 karakter....")
        if deteksiuser(users, "username", username):
            raise ValueError("Username sudah dipakai....")
        password = pwinput.pwinput("Password (min. 6 karakter): ", mask="*")
        if password == "":
            raise ValueError("Password tidak boleh kosong....")
        if len(password) < 6:
            raise ValueError("Password minimal 6 karakter....")
        users.append({"username": username, "password": password, "role": "user", "saldo": 0})
        savedata(FileUser, users)
        print("Registrasi berhasil! Silakan login....")
    except ValueError as ipan:
        print(ipan)
    except FileNotFoundError:
        print("File user tidak ditemukan, registrasi gagal....")
    return users
