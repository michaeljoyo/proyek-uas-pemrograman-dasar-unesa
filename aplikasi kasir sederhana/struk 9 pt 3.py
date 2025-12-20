import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import datetime

products = [
    {"name": "minyak goreng", "price": 21000, "image": "minyak goreng.png"},
    {"name": "Beras bintang", "price": 80000, "image": "Beras bintang.png"},
    {"name": "Telur", "price": 32000, "image": "telur.png"},
    {"name": "Gula", "price": 10000, "image": "Gula.png"},
    {"name": "Mie Instan", "price": 4000, "image": "Mie Instan.png"},
    {"name": "Teh pucuk", "price": 4000, "image": "teh pucuk.png"},
    {"name": "Garam", "price": 4000, "image": "garam.png"},

]
cart = {}

def update_total():
    total = 0
    for item, qty in cart.items():
        total += qty * next(p["price"] for p in products if p["name"] == item)
    total_label.config(text=f"Total: Rp {total:,}".replace(",", "."))
    return total

def hitung_kembalian():
    total = update_total()
    try:
        bayar = int(entry_bayar.get())
        kembali = bayar - total
        if kembali < 0:
            kembalian_label.config(text="Uang kurang!")
        else:
            kembalian_label.config(text=f"Kembalian: Rp {kembali:,}".replace(",", "."))
    except:
        kembalian_label.config(text="Masukkan angka yang valid!")

def add_item(name, qty_label):
    cart[name] = cart.get(name, 0) + 1
    qty_label.config(text=str(cart[name]))
    update_total()

def remove_item(name, qty_label):
    if cart.get(name, 0) > 0:
        cart[name] -= 1
    qty_label.config(text=str(cart.get(name, 0)))
    update_total()

def generate_struk():
    total = update_total()
    struk_box.delete(1.0, END)
    struk_box.insert(END, "==== STRUK PEMBELIAN ====\n")
    struk_box.insert(END, f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
    struk_box.insert(END, "----------------------------\n")

    for item, qty in cart.items():
        if qty > 0:
            harga = next(p["price"] for p in products if p["name"] == item)
            struk_box.insert(END, f"{item} x{qty} = Rp {qty * harga:,}\n".replace(",", "."))

    struk_box.insert(END, "----------------------------\n")
    struk_box.insert(END, f"Total: Rp {total:,}\n".replace(",", "."))

def save_struk():
    content = struk_box.get(1.0, END)
    if len(content.strip()) == 0:
        return
    with open("struk_pembelian.txt", "w", encoding="utf-8") as f:
        f.write(content)
    kembalian_label.config(text="Struk tersimpan ke: struk_pembelian.txt")


root = Tk()
root.title("Aplikasi Kasir Tkinter")
root.geometry("620x780")
root.configure(bg="#f5f5f5")

# ------------------ JUDUL ------------------
title_label = Label(
    root,
    text="🛒 Aplikasi Kasir Sederhana",
    font=("Arial", 30, "bold"),
    bg="#4e73df",
    fg="white",
)
title_label.pack(pady=10)

# ------------------ PRODUK HORIZONTAL ------------------
product_frame = Frame(root, bg="#ffffff", bd=3, relief="ridge")
product_frame.pack(pady=5)

col = 0
for p in products:
    frame = Frame(product_frame, pady=5, padx=10, bg="#f9f9f9", bd=2, relief="groove")
    frame.grid(row=0, column=col, padx=10)

    img = Image.open(p["image"])
    img = img.resize((50, 50))
    photo = ImageTk.PhotoImage(img)

    img_label = Label(frame, image=photo, bg="#f9f9f9")
    img_label.image = photo
    img_label.pack()

    Label(frame, text=p["name"], font=("Arial", 12, "bold"), bg="#f9f9f9").pack()
    Label(frame, text=f"Rp {p['price']:,}".replace(",", "."), bg="#f9f9f9").pack()

    qty_label = Label(frame, text="0", font=("Arial", 12), bg="#f9f9f9")
    qty_label.pack()

    btn_frame = Frame(frame, bg="#f9f9f9")
    btn_frame.pack()

    Button(btn_frame, text="-", width=3, bg="#ff6b6b", fg="white",
           command=lambda n=p["name"], q=qty_label: remove_item(n, q)).pack(side=LEFT, padx=3)

    Button(btn_frame, text="+", width=3, bg="#4CAF50", fg="white",
           command=lambda n=p["name"], q=qty_label: add_item(n, q)).pack(side=RIGHT, padx=3)

    col += 1

# ------------------ TOTAL & PEMBAYARAN ------------------
total_label = Label(root, text="Total: Rp 0", font=("Arial", 16, "bold"), bg="#f5f5f5")
total_label.pack(pady=5)

Label(root, text="Uang Bayar:", font=("Arial", 12), bg="#f5f5f5").pack()
entry_bayar = Entry(root, font=("Arial", 14), bd=2)
entry_bayar.pack()

Button(root, text="Hitung Kembalian", bg="#007acc", fg="white", font=("Arial", 12),
       command=hitung_kembalian).pack(pady=5)

kembalian_label = Label(root, text="", font=("Arial", 14, "bold"), bg="#f5f5f5")
kembalian_label.pack()

# ------------------ STRUK ------------------
Label(root, text="Struk Pembelian:", font=("Arial", 14, "bold"), bg="#f5f5f5").pack()
struk_box = Text(root, width=35, height=12, bd=2, relief="sunken")
struk_box.pack()

Button(root, text="Cetak Struk", bg="#ffa726", fg="white",
       command=generate_struk).pack(pady=5)

Button(root, text="Simpan Struk ke File", bg="#8e44ad", fg="white",
       command=save_struk).pack()

root.mainloop()
