# Foodgram API
![workflow badge](https://github.com/dzheronimo/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Описание проекта:

Проект Foodgram или "Продуктовый помощник" - это сервис для обмена рецептами, с возможностью планированиия списка покупок 
для их приготовления.
Рецепты можно отфильтровать по тегам, добавить в избранное и список покупок. Автор рецепта может добавить рецепт и отредактировать уже добавленый (автором).
Пользователь может подписаться на полюбившегося автора и следить за его гастрономическими изысканиями. 
Сервис подразумевает регистрацию пользователей и сохранение всей истории работы с ним.

```
Ресурсы API Foodgram:
    users: аутентификация, пользователи
    recipes: рецепты
    ingredients: ингредиенты
    tags: доступные теги
    subscriptions: подписки пользователей
```

## Используется:

+ Python 3.9
+ Django 3.2
+ Django REST framework 3.12
+ Djoser
+ PostgreSQL
+ gunicorn
+ Docker (Docker-compose)
+ Nginx

## Распаковка проекта

Развёртывание контейнеров в **Docker**:

```bash
# Переходим в папку проекта
cd ~/infra
docker-compose up
# Создание миграций
docker-compose exec backend python3 manage.py makemigrations
# Применение миграций
docker-compose exec backend python3 manage.py migrate
# Создание суперпользователя
docker-compose exec backend python3 manage.py createsuperuser
# Загрузка статики
docker-compose exec backend python3 manage.py collectstatic --no-input
# Загрузка ингредиентов
docmer-compose exec backend python3 manage.py loadingredients
```

## Наполнение файла *.env*:

```
DB_ENGINE=движок БД (по умолчанию PostgreSQL)
DB_NAME=название БД 
DB_USER=пользователь БД 
DB_PASSWORD=пароль пользователя 
DB_HOST=контейнер с БД  
DB_PORT=порт для работы с бд
```

## Документация и эндпойнты:

[http://127.0.0.1:8000/api/doc/redoc/](http://127.0.0.1:8000/api/doc/redoc/)

## Примеры запросов к API:

- GET: http://127.0.0.1:8000/api/recipes/1/

Rsponse:

```JSON
{
    "id": 1,
    "tags": [
        {
            "id": 1,
            "name": "Завтрак",
            "color": "#fff480",
            "slug": "breakfast"
        }
    ],
    "author": {
        "email": "dzheronimo@me.com",
        "id": 1,
        "username": "dzheronimo",
        "first_name": "Владислав",
        "last_name": "Яковенко",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 2183,
            "name": "яйца куриные крупные",
            "measurement_unit": "г",
            "amount": 360
        },
        {
            "id": 1344,
            "name": "помидоры вяленые",
            "measurement_unit": "по вкусу",
            "amount": 1
        },
        {
            "id": 1285,
            "name": "перец черный молотый",
            "measurement_unit": "г",
            "amount": 5
        },
        {
            "id": 1685,
            "name": "соль",
            "measurement_unit": "г",
            "amount": 2
        },
        {
            "id": 1335,
            "name": "подсолнечное масло",
            "measurement_unit": "г",
            "amount": 15
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Яичница",
    "image": "http://yatube.bounceme.net/media/recipes/recipe_image.webp",
    "text": "Хорошо прожарить помидоры на растительном масле. Сверху разбить 4 яйца и сразу посолить, поперчить. Крышкой не закрывать. Жарить на среднем-сильном огне до готовности. Должен быть слегка жидким белок.",
    "cooking_time": 15
}
```

- GET: http://127.0.0.1:8000/api/ingredients/170/

Response:

```JSON
    {
        "id": 170,
        "name": "Буррата",
        "measurement_unit": "г"
    }
```


## Автор:

###### Студент курса "Python-разработчик" от Яндекс-Практикума

+ [Dzheronimo](https://github.com/dzheronimo)
