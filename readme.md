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

### Ниже приведeны команды для взаимодействия с приложением в локальном окружении:

- `make local_up` - запустить приложение 


- `make local_down` - остановить работу приложения и удалить все контейнеры


- `make local_shell` - зайти в bash контейнера "web"


- `make local_django_shell` - зайти в shell django


- `make local_migrate` - применить миграции


- `make local_make_migration` - создать новые миграции


- `make local_create_superuser` - создать суперпользователя


- `make format` - отформатировать код по стандарту PEP 8






