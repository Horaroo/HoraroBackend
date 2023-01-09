# Horaro `backend`
___
### _production: https://api.horaro.net/_
### _staging: https://api.staging.horaro.net/_ - Доступен только для contributors.
___

## Инструкция
___

### Для работы с приложением необходимо установить:
1.  Docker
2.  docker-compose
___

### Переменные окружения:
В корневой директории проекта необходимо создать файл `.env` с ниже перечисленными переменными:
- `ALLOWED_HOSTS=*`
- `DEBUG=True`
- `POSTGRES_NAME=postgres`
- `POSTGRES_HOST=db`
- `POSTGRES_PASSWORD=postgres`
- `POSTGRES_PORT=5432`
- `POSTGRES_USER=postgres`
- `SECRET_KEY="django-insecure-b(=r+o15ecqk0yslac@*^@w^5a8"`
#### Необязательные переменные
Ниже перечисленные переменные необходимы для взаимодействия с gmail.
В случае если вам необходимо их установить, то следует их [создать по данному туториалу.](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab)
- `EMAIL_HOST`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_HOST_USER`
- `EMAIL_PORT`
___

### Ниже приведeны команды для взаимодействия с приложением в локальном окружении:

- `make local_up` - запустить приложение 


- `make local_down` - остановить работу приложения и удалить все контейнеры


- `make local_shell` - зайти в bash контейнера "web"


- `make local_django_shell` - зайти в shell django


- `make local_migrate` - применить миграции


- `make local_make_migration` - создать новые миграции


- `make local_create_superuser` - создать суперпользователя


- `make format` - отформатировать код по стандарту PEP 8






