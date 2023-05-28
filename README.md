# Сервис поиска ближайших машин для перевозки грузов.
___
## Тестовое задание web-программист Python

Список используемых технологий: Python, Django, Django-rest-framework, PostgreSQL, Docker, Docker-compose, Pytest, Celery, Celery-beat

___
## Как установить проект

1. Клонируйте репозиторий в любую папку:
   - git init
   - git clone https://github.com/NYikolay/Search-Service.git
2. Создайте .env файл в папке config/.env. Заполните всеми необходимыми значениями (см. .env.dist)
3. Для сборки проекта, находясь в корневой папке выполните в терминале команду: 
   - docker-compose -f docker-compose.yml --env-file config/.env up --build
   - или docker-compose -f docker-compose.yml --env-file config/.env  up -d --build - Чтобы запустить в фоновом режиме
4. Убедитесь, что контейнеры запущены командой docker ps
5. Для создания суперпользователя:
   - docker exec -it welbex-rest python3 manage.py createsuperuser
6. Перейдите в браузере по урлу http://127.0.0.1:8000/

Чтобы остановить контейнеры используйте команду:
   - docker-compose -f docker-compose.yml down

При каждом последующем запуске приложения используйте:
   - docker-compose -f docker-compose.yml --env-file config/.env up
___
## Запуск тестов

При запущенных контейнерах используйте команду:
   - docker exec -it welbex-rest pytest
___

## Дополнительная информация

Документация к API находится по следующим urls:
   - http://127.0.0.1:8000/api/docs/
   - http://127.0.0.1:8000/api/docs/schema/ - Загрузка документации в формате yaml

При первоначальной сборке проекта в базе данных будут созданы 20 объектов модели Car 
и загружены данные из файла ./uszips.csv в таблицу Location. 
Скрипты по формированию первоначальных данных используют Django Command и находятся в ./search_service/management/commands/

Каждые 3 минуты локации объектов Car обновляются случайным образом с помощью Celery и Celery-beat