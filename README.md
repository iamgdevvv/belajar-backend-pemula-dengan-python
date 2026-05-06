# OpenShop (Backend API)

OpenShop adalah RESTful API sederhana untuk mengelola data produk menggunakan **Django 4.2 (LTS)** dan **Django REST Framework**.

## Menjalankan Project

Prasyarat: Python **3.10+**

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

### Menjalankan Project Admin
```bash
python manage.py createsuperuser
python manage.py runserver 8000
```

### Mode Soft Delete (opsional)

API mendukung dua perilaku delete tanpa konfigurasi tambahan:

- Jika payload `POST` atau `PUT` menyertakan field `is_delete`, produk akan diperlakukan sebagai soft-delete product.
- Jika field itu tidak dikirim, `DELETE` akan menghapus data secara permanen.

## Endpoint

- `POST /products/` menambahkan produk
- `GET /products/` menampilkan semua produk (support query `?name=` dan `?location=`)
- `GET /products/{id}/` menampilkan detail produk
- `PUT /products/{id}/` mengubah produk
- `DELETE /products/{id}/` menghapus produk

Response produk akan menyertakan `_links` (HATEOAS) untuk resource terkait.
