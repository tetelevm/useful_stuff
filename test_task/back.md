Бэкенд-часть:
=======

* Свежая версия Python 3 (>= 3.8)
* фреймворки `django` и `graphene` (`graphene-django`)

Немного доков
* https://docs.djangoproject.com/en/3.1/
* http://docs.graphene-python.org/en/latest/
* http://docs.graphene-python.org/projects/django/en/latest/
* https://graphql.org/learn/
 

Тестовое задание состоит из нескольких частей:

БД
--

дать проект с приложением, в котором описать модель БД со следующими полями:

```
Имя: name (varchar 200)
Компания: company_name (varchar 100)
Должность: position_name (varchar 100)
Дата приёма: hire_date (date)
Дата увольнения: fire_date (date, null)
Ставка, руб.: salary (int)
Ставка, %: fraction (int)
База, руб.: base (int)
Аванс, руб.: advance (int)
Почасовая оплата: by_hours (boolean)
```

Движок БД не имеет значения, для удобства можно использовать доступный из
коробки SQLite.

Админка
-------

Добавить модель во встроенную админку для внутреннего просмотра и
редактирования. Создать пользователя – администратора с логином
`admin@example.com` и паролем `admin`.

API
---

Создать слой API с использованием graphene и graphene-django. API должен быть
доступен по endpoint’у `/api`, иметь встроенный web GraphQL-клиент GraphiQL и
реализовывать следующую схему:

##### тип
`OccupationType`

должен быть связан с моделью `Occupation` используя `graphene-django`.

##### запрос

`getOccupation(occupationId!): OccupationType`

должен принимать `id` модели `Occupation` и возвращать соответствующий этому
`id` экземпляр модели `Occupation` из БД.

##### запрос

`getOccupations(): [OccupationType]`

должен возвращать список всех имеющихся в БД моделей `Occupation`.

##### мутация

```
addOccupation(
	name: String!,
	companyName: String!,
	positionName: String!,
	hireDate: Date!,
	fireDate: Date,
	salary: Int!,
	fraction: Int!,
	base: Int!,
	advance: Int!,
	by_hours: Boolean!
): OccupationType
```

должна принимать все поля, указанные в модели Occupation, создавать новую
запись в БД с этими полями, и возвращать новосозданный экземпляр модели в
качестве результата.
