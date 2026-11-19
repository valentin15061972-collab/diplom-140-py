# Дипломный проект: Backend-приложение для автоматизации закупок

DRF сервис заказа товаров для розничных сетей.

## Возможности

- Регистрация и авторизация пользователей с подтверждением по email
- Управление адресами доставки
- Просмотр списка товаров и детальной спецификации по каждому товару
- Импорт товаров из файлов YAML/JSON (для магазинов-поставщиков)
- Добавление и удаление товаров от разных магазинов в корзину
- Подтверждение заказа и выбор адреса доставки
- Отправка email клиенту и накладной администратору
- Просмотр деталей заказов
- Изменение статуса заказа (магазином-поставщиком)
- Настраиваемые поля товаров через модель Parameter
- Swagger-документация API

## Установка
```
# Создание виртуального окружения

python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate   # для Windows

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```
## API Endpoints
```
 # Пользователи
POST /api/users/register (Регистрация) 
POST /api/users/register/confirm (Подтверждение регистрации) 
POST /api/users/login (Авторизация (получение токена))
GET/PUT /api/users/details (Данные пользователя)
GET/POST/DELETE /api/users/contacts (Адреса доставки)

 # Товары
GET /api/products/shops (Список магазинов)
GET /api/products/categories (Список категорий)
GET /api/products/list_prods (Список товаров (с фильтрами))
GET /api/products/{id} (Детальная информация о товаре)
POST /api/products/importer (Импорт товаров (магазин-поставщик))

 # Заказы
GET /api/orders/basket (Просмотр корзины)
POST /api/orders/basket (Добавить товар в корзину)
DELETE /api/orders/basket (Удалить товар из корзины)
GET /api/orders/list_orders (Список заказов)
POST /api/orders/list_orders (Подтверждение заказа)
GET /api/orders/{id} (Детали заказа)
PUT /api/orders/{id}/status (Изменение статуса заказа)

 # Документация
/api/docs/ (Swagger UI)
/api/schema/ (JSON-schema API)
```
## Авторизация
```
- Используется Token Authentication. 
- После входа добавьте заголовок: 
  Authorization: Token <ваш_токен>
```
## Технологии

- Django 
- Django Rest Framework 
- django-filter
- drf-spectacular (Swagger/Schema)
- Celery (асинхронные задачи)
- SQLite (разработка)

