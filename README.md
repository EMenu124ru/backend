# EMenu

## Требования

Необходимо, чтобы были установлены следующие компоненты:

- Docker
- Docker compose

## Запуск

1. Создайте **.env** файл с переменными окружения

2. Запустите проект с помощью **Docker**:

```
make docker-up-buildd
```

3. Применение существующих миграций:

```
make migrate
```

4. Создание суперпользователя:

```
make createsuperuser
```

5. Генерация синтетических данных:

```
make fill_sample_data
```

## Тесты

1. Запуск тестов:

```
make tests
```

2. Для получения информации о покрытии:

```
make tests-cov
```

## Статический анализ

1. Запуск линтеров:

```
make linters
```

Для получения списка остальных команд и их описания:

## Help

```
make help
```
