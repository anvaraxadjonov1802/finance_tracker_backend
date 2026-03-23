# Personal Finance Tracker Backend

Shaxsiy moliyani boshqarish uchun yaratilgan backend API. Ushbu loyiha foydalanuvchiga accountlar, daromadlar, xarajatlar, transferlar, qarzlar, byudjet va analytics ma’lumotlarini boshqarish imkonini beradi.

## Asosiy imkoniyatlar

- JWT asosidagi autentifikatsiya
- Ro‘yxatdan o‘tish va tizimga kirish
- Account va kartalarni boshqarish
- Income va expense transactionlar
- Accountlar orasida transfer
- Debt va receivable yozuvlari
- Monthly budget va category limitlar
- Dashboard analytics
- Token refresh va auto auth flow

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- Django Filter

## Loyihaning modullari

- `users` — auth, register, me
- `accounts` — account va kartalar
- `categories` — income/expense kategoriyalar
- `transactions` — daromad va xarajatlar
- `transfers` — accountlar orasidagi o‘tkazmalar
- `debts` — qarz va haqdorliklar
- `budgets` — monthly budget va limitlar
- `analytics_app` — dashboard statistikasi

## O‘rnatish

### 1. Repository ni clone qilish

```bash
git clone <BACKEND_REPOSITORY_URL>
cd <BACKEND_PROJECT_FOLDER>
```

### 2. Virtual environment yaratish

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### 3. Paketlarni o‘rnatish

```bash
pip install -r requirements.txt
```

### 4. `.env` fayl yaratish

Loyiha rootida `.env` oching:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/finance_db

ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### 5. Migratsiyalarni ishga tushirish

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 7. Serverni ishga tushirish

```bash
python manage.py runserver
```

Backend odatda quyidagi manzilda ishlaydi:

```text
http://127.0.0.1:8000/
```

## API Endpointlar

### Auth

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`

### Accounts

- `GET /api/accounts/`
- `POST /api/accounts/`
- `GET /api/accounts/{id}/`
- `PUT /api/accounts/{id}/`
- `DELETE /api/accounts/{id}/`

### Categories

- `GET /api/categories/`
- `POST /api/categories/`
- `GET /api/categories/{id}/`
- `PUT /api/categories/{id}/`
- `DELETE /api/categories/{id}/`

### Transactions

- `GET /api/transactions/`
- `POST /api/transactions/`
- `GET /api/transactions/{id}/`
- `PUT /api/transactions/{id}/`
- `DELETE /api/transactions/{id}/`

### Transfers

- `GET /api/transfers/`
- `POST /api/transfers/`
- `GET /api/transfers/{id}/`
- `DELETE /api/transfers/{id}/`

### Debts

- `GET /api/debts/`
- `POST /api/debts/`
- `GET /api/debts/{id}/`
- `PUT /api/debts/{id}/`
- `DELETE /api/debts/{id}/`
- `PATCH /api/debts/{id}/close/`
- `PATCH /api/debts/{id}/reopen/`

### Budgets

- `GET /api/budgets/`
- `POST /api/budgets/`
- `GET /api/budgets/current/`
- `GET /api/budgets/{id}/`
- `DELETE /api/budgets/{id}/`
- `GET /api/budgets/{budget_id}/limits/`
- `POST /api/budgets/{budget_id}/limits/`
- `DELETE /api/budgets/{budget_id}/limits/{id}/`

### Analytics

- `GET /api/analytics/summary/`
- `GET /api/analytics/category-breakdown/`
- `GET /api/analytics/income-vs-expense/`
- `GET /api/analytics/calendar/`
- `GET /api/analytics/budget-vs-actual/`

## Authentication

Loyiha JWT token asosida ishlaydi.

Login response:

```json
{
  "access": "your-access-token",
  "refresh": "your-refresh-token"
}
```

Protected endpointlarga so‘rov yuborishda headerga token qo‘shiladi:

```http
Authorization: Bearer your-access-token
```

## Loyihaning maqsadi

Bu loyiha hackathon doirasida yaratilgan bo‘lib, foydalanuvchining shaxsiy moliyasini bitta platformada boshqarish imkonini beradi:

- account balansi
- daromadlar
- xarajatlar
- qarzlar
- byudjet
- statistika

## Deployment

Backend deploy uchun tavsiya etiladi:

- Render
- Railway
- VPS

Production uchun kerakli narsalar:

- `DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `CORS_ALLOWED_ORIGINS`
- `DATABASE_URL`
- `collectstatic`
- `migrate`

## Author

Created for hackathon MVP by **Anvar Axadjonov**

## License

This project is created for educational and hackathon purposes.
