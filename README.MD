# Aplikasi Manajemen Ritel

Aplikasi desktop sederhana berbasis Python untuk mengelola produk dan transaksi, khususnya untuk bisnis ritel kecil. Aplikasi ini menyediakan operasi CRUD untuk produk dan mencatat transaksi penjualan dengan menyimpan semua data di database MySQL.

## Fitur

### Manajemen Produk
- Tambah produk baru dengan nama dan harga.
- Perbarui detail produk yang ada.
- Hapus produk dari database.
- Lihat daftar semua produk.

### Manajemen Transaksi
- Catat transaksi dengan memilih produk dan menentukan jumlah.
- Hitung total harga transaksi secara otomatis.
- Simpan detail transaksi termasuk produk, jumlah, total harga, dan tanggal.
- Lihat daftar semua transaksi.

## Prasyarat

1. **Python 3.x** terinstal di komputer Anda.
2. **MySQL Server** terinstal dan berjalan.
3. Perpustakaan `mysql-connector-python` terinstal:
   ```bash
   pip install mysql-connector-python
   ```
4. Sebuah database MySQL bernama `app_penjualan`. Program akan secara otomatis membuat tabel yang diperlukan saat pertama kali dijalankan.

## Persiapan

### Konfigurasi Database
Pastikan Anda memiliki database MySQL yang berjalan secara lokal. Perbarui pengaturan koneksi database di fungsi `connect_to_db()` jika diperlukan:

```python
return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Ganti dengan kata sandi root MySQL Anda
    database="app_penjualan"
)
```

### Pembuatan Tabel
Program mencakup fungsi `setup_database()` yang secara otomatis membuat tabel `products` dan `transactions` jika belum ada.

## Penggunaan

1. Kloning atau unduh repositori ini.
2. Jalankan skrip:
   ```bash
   python retail_app.py
   ```
3. Gunakan antarmuka GUI aplikasi untuk mengelola produk dan mencatat transaksi.

## Struktur File

- `retail_app.py`: File aplikasi utama yang berisi semua logika dan komponen UI.

## Detail Teknis

### Skema Database

#### Tabel `products`
| Kolom          | Tipe          | Deskripsi                |
|----------------|---------------|--------------------------|
| `product_id`   | INT           | Primary Key, Auto Increment |
| `product_name` | VARCHAR(255)  | Nama produk             |
| `product_price`| DECIMAL(10,2) | Harga produk            |

#### Tabel `transactions`
| Kolom             | Tipe          | Deskripsi                          |
|--------------------|---------------|------------------------------------|
| `transaction_id`   | INT           | Primary Key, Auto Increment        |
| `product_id`       | INT           | Foreign Key ke `products.product_id` |
| `quantity`         | INT           | Jumlah pembelian                   |
| `total_price`      | DECIMAL(10,2) | Total harga transaksi              |
| `transaction_date` | DATE          | Tanggal transaksi                  |

### Perpustakaan yang Digunakan

- **Tkinter**: Untuk membangun antarmuka pengguna grafis (GUI).
- **mysql-connector-python**: Untuk berinteraksi dengan database MySQL.

## Pengembangan

Peningkatan di masa depan dapat mencakup:
- Menambahkan fungsi pencarian dan filter.
- Membuat laporan penjualan dalam rentang tanggal tertentu.
- Mengekspor data ke file CSV atau Excel.

## Lisensi

Proyek ini bersifat open-source dan tersedia di bawah Lisensi MIT.