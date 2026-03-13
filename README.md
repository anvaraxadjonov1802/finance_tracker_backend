# MB.UZ-HACKTHON

# Xarajatlarni Toifalash va Shaxsiy Moliyani Boshqarish Tizimi

## 1. Kirish

Zamonaviy fintech va smart banking ilovalarda foydalanuvchilarning nafaqat xarajatlarini, balki daromadlari, balanslari, qarz va haqdorliklarini ham kompleks tarzda boshqarish muhim hisoblanadi.  

Ushbu task foydalanuvchining **shaxsiy moliyasini to‘liq nazorat qilishga yo‘naltirilgan yengil, ammo funksional moliyaviy boshqaruv tizimini** yaratishni nazarda tutadi.

---

# 2. Muammo Bayoni

Ko‘pchilik foydalanuvchilar:

- xarajat va daromadlarni alohida tizimlarda yoki umuman qayd etmaydi;
- qaysi karta yoki accountda qancha mablag‘ borligini real vaqtda bilmaydi;
- qarzlari va boshqalardan olishi kerak bo‘lgan pullarni (haqdorlik) unutib qo‘yadi;
- oylik byudjet va real sarf o‘rtasidagi farqni nazorat qila olmaydi.

Natijada:

- shaxsiy moliyaviy intizom pasayadi
- noto‘g‘ri moliyaviy qarorlar qabul qilinadi.

---

# 3. Vazifa Tavsifi

Ishtirokchilar **foydalanuvchi daromadlari (income), xarajatlari (expense), account va kartalari, balanslari, qarzlari va haqdorliklarini yagona tizimda boshqarish imkonini beruvchi fintech ilova** ishlab chiqishlari kerak.

Ilova:

- **Web** yoki **Mobile** bo‘lishi mumkin
- **Hackathon doirasida MVP darajasida** ishlab chiqilishi kerak

Qo‘shimcha imkoniyat:

- **Oila a’zolari bilan shared foydalanish**
- xarajatlar va tushumlar umumiy hisoblanadi

---

# 4. Asosiy Funksional Talablar

## Account va Kartalar

- account va bank kartalarini qo‘shish  
  - nomi
  - turi
  - valyuta
  - boshlang‘ich balans

- har bir account/karta uchun **joriy balansni ko‘rish**

---

## Xarajatlar (Expenses)

- xarajat qo‘shish
  - summa
  - sana
  - tavsif
  - kategoriya

- xarajat qaysi account/karta yoki naqd puldan qilinganini tanlash
- xarajat kiritilganda **balans avtomatik kamayishi**
- xarajatlarni **tahrirlash**
- xarajatlarni **o‘chirish**

---

## Daromadlar (Income)

- daromad qo‘shish
  - summa
  - sana
  - manba
  - category

- daromad qaysi account yoki kartaga tushganini belgilash
- naqd pul varianti ham bo‘lishi mumkin
- daromad qo‘shilganda **balans avtomatik oshishi**

---

## Transferlar

- bir account/kartadan boshqasiga pul o‘tkazish
- transfer vaqtida:
  - bir balans kamayadi
  - boshqasi oshadi

- agar **ikki xil valyuta** bo‘lsa
  - **valyuta kursi orqali konvertatsiya qilish**

---

## Qarzlar va Haqdorliklar

- berilgan qarzlarni qayd etish
  - kimga
  - qancha

- olinishi kerak bo‘lgan mablag‘larni (haqdorlik) yuritish

- qarz holati:
  - `OPEN`
  - `CLOSED`

---

## Byudjet va Rejalashtirish

- oylik **daromad (income) byudjeti**
- kategoriya bo‘yicha **xarajat limitlari**

Tizim quyidagilarni solishtiradi:

- rejalashtirilgan byudjet
- real xarajatlar

---

# 5. Ko‘rish va Tahlil

Statistik tahlillar:

### Umumiy statistika
- daromadlar
- xarajatlar

### Kategoriya bo‘yicha statistika

### Vaqt bo‘yicha statistika

- yillik
- oylik
- haftalik
- kunlik

### Qo‘shimcha tahlillar

- kategoriya bo‘yicha **xarajatlar vs tushumlar**
- **calendar view** orqali kunlik operatsiyalarni ko‘rish

---

# 6. Oila A’zolari Bilan Ulashish (Ixtiyoriy)

- oila a’zolarini taklif qilish
- umumiy byudjet
- umumiy xarajatlar
- umumiy daromadlar

---

# 7. AI va Avtomatlashtirish (Bonus)

AI yoki rule-based tizim yordamida:

### Avtomatik kategoriya aniqlash

xarajat tavsifi asosida kategoriya aniqlash.

### Xarajat tahlili

foydalanuvchi odatlariga qarab:

- moliyaviy tahlil
- sarf odatlari

### Ogohlantirishlar (Notifications)

Misollar:

- bu oy ma’lum kategoriya bo‘yicha odatdagidan ko‘p sarfladingiz
- kommunal to‘lov qilish vaqti keldi
- telefon to‘lovini qilish kerak

AI/ML yoki oddiy **rule-based** yondashuvdan foydalanish mumkin.

---

# 8. Asosiy Use Case Holatlari

1. Foydalanuvchi yangi karta qo‘shadi va boshlang‘ich balans kiritadi.
2. Foydalanuvchi xarajat kiritadi va balans avtomatik kamayadi.
3. Foydalanuvchi daromad kiritadi va balans oshadi.
4. Foydalanuvchi bir kartadan boshqasiga transfer qiladi.
5. Foydalanuvchi qarz yoki haqdorlikni qayd etadi.
6. Tizim oylik byudjet va real xarajatlarni solishtiradi.
7. (Bonus) AI foydalanuvchiga moliyaviy tavsiyalar beradi.

---

# 9. Texnik Talablar

### Backend
- REST API
- **Java (tavsiya etiladi)**

### Frontend
- Web yoki Mobile
- React
- Flutter
- Vue

### Ma’lumotlar Bazasi

- **PostgreSQL tavsiya etiladi**

### AI Integratsiya

- majburiy emas
- ammo qo‘llab-quvvatlanadi

---

# 10. Kutilayotgan Natija

Hackathon yakunida ishtirokchilar:

- ishlaydigan **web yoki mobile fintech ilova**
- foydalanuvchining **shaxsiy moliyasini to‘liq boshqarish imkoniyati**
- daromad, xarajat, balans, qarzlarni boshqarish tizimi
- statistik tahlillar
- (ixtiyoriy) **AI asosidagi avtomatlashtirish va ogohlantirishlar**

namoyish qilib berishlari kerak.
