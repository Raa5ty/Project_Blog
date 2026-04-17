# MyBlog - блог на Django

Простой и элегантный блог с системой аутентификации пользователей, созданный в учебных целях.

## 🚀 Функционал

### Для всех пользователей:

- Просмотр списка постов
- Чтение отдельных постов
- Отправка сообщений через форму обратной связи
- Регистрация и авторизация

### Для авторизованных пользователей:

- Создание новых постов
- Редактирование своих постов
- Удаление своих постов
- Личный профиль с дополнительной информацией

## 🛠 Технологии

- **Backend:** Django 6.0.4
- **Frontend:** HTML5, SCSS/CSS3
- **База данных:** SQLite3
- **Аутентификация:** Django Auth + Profile модель

## 📁 Структура проекта

```
MyBlog/
├── blog_app/              # Основное приложение блога
│   ├── models.py         # Модель Post
│   ├── views.py          # CRUD вьюхи для постов
│   ├── forms.py          # Форма создания поста
│   ├── urls.py           # Маршруты блога
│   └── templates/blog_app/
│       ├── base.html
│       ├── base_header.html
│       ├── home.html
│       ├── about.html
│       ├── posts.html
│       ├── post_detail.html
│       ├── create_post.html
│       ├── edit_post.html
│       └── delete_post.html
│
├── auth_app/              # Приложение аутентификации
│   ├── models.py         # Profile (расширение User)
│   ├── forms.py          # Формы регистрации, логина, сообщения
│   ├── views.py          # Class-based вьюхи
│   ├── urls.py           # Маршруты аутентификации
│   └── templates/auth_app/
│       ├── register.html
│       ├── login.html
│       ├── profile.html
│       └── message.html
│
├── static/
│   ├── css/              # Скомпилированные стили
│   └── scss/             # SCSS исходники
│       ├── main.scss
│       ├── _variables.scss
│       └── _blog.scss
│
├── templates/            # Общие шаблоны
├── db.sqlite3            # База данных
└── manage.py
```


## 🗺 Навигация

| URL                     | Описание                                                        |
| ----------------------- | ----------------------------------------------------------------------- |
| `/`                   | Главная страница                                         |
| `/posts/`             | Список всех постов                                      |
| `/posts/<id>/`        | Просмотр поста                                             |
| `/posts/create/`      | Создание поста (только авторизованные) |
| `/posts/<id>/edit/`   | Редактирование поста                                 |
| `/posts/<id>/delete/` | Удаление поста                                             |
| `/about/`             | Страница "О себе"                                          |
| `/auth/register/`     | Регистрация                                                  |
| `/auth/login/`        | Вход в систему                                              |
| `/auth/logout/`       | Выход                                                              |
| `/auth/profile/`      | Профиль пользователя                                 |
| `/auth/message/`      | Отправка сообщения                                     |
| `/admin/`             | Админ-панель Django                                          |

## 🔧 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/yourusername/myblog.git
cd myblog
```

### 2. Создать виртуальное окружение

###### Windows

```
python -m venv .venv
.venv\Scripts\activate
```

###### Linux/Mac

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```
pip install django
```

### 4. Применить миграции

```
python manage.py migrate
python manage.py makemigrations blog_app
python manage.py makemigrations auth_app
python manage.py migrate
```

### 5. Создать суперпользователя (для админки)

```
python manage.py createsuperuser
```

### 6. Запустить сервер

```
python manage.py runserver
```


## 📝 Валидация форм

### Регистрация:

* Email должен быть уникальным
* Пароль и подтверждение пароля должны совпадать

### Отправка сообщения:

* Сообщение не может быть пустым
* Максимальная длина сообщения - 500 символов
* Минимальная длина сообщения - 10 символов

## 👨‍💻 Автор

Учебный проект в рамках курса по Python Developer - Django
