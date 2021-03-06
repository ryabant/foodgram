Онлайн-сервис, где пользователи могут сохранять и публиковать свои рецепты, 
подписываться на публикации других пользователей, добавлять 
понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать
сводный список продуктов, необходимых для приготовления одного или нескольких 
выбранных блюд

Cоздан в качестве дипломного проекта учебного курса Яндекс.Практикум.

## Стек технологий
- проект написан на Python с использованием веб-фреймворка Django.
- деплой на сервере - nginx, gunicorn
- база данных PostgreSQL
- автоматическое развертывание проекта - Docker, docker-compose

## Установка и запуск

Для работы требуется **Docker** и **Docker-compose**

Клонируйте репозиторий. В директории с manage.py создайте файл .env со следующим
содержимым:

```  
DB_ENGINE=django.db.backends.postgresql
DB_NAME=(укажите название вашей БД, для подключения django)
POSTGRES_USER=(укажите имя пользователя вашей БД)
POSTGRES_PASSWORD=(укажите пароль к БД)
POSTGRES_DB=(укажите название вашей БД)
DB_HOST=db
DB_PORT=5432
SECRET_KEY=(укажите свой ключ)
DEBUG=False
```
Чтобы собрать образ из директории с docker-compose.yaml выполните команду:
````
sudo docker-compose build
````
Далее необходимо собрать статику и выполнить миграцию:
````
sudo docker-compose run web python manage.py collectstatic
sudo docker-compose run web python manage.py migrate
````
Для запуска сервиса:
````
sudo docker-compose up
````
После этого сервис станет доступен по адресу http://localhost

Для заполнения базы данными выполните команду:
````
sudo docker-compose run web python manage.py add_ing_data
sudo docker-compose run web python manage.py add_tags_data
````