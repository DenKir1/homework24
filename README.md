SPA веб-приложение бэкенд-сервер, который возвращает клиенту JSON-структуры
Использование фикстур для заполнения таблицы платежей:
python manage.py dumpdata users.payment > user_payment_data.json
python manage.py loaddata user_payment_data.json
