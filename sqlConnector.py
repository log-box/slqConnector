# Импортируем нашу ORM библиотеку
from peewee import *

# Создаем соединение с нашей базой данных
conn = SqliteDatabase('Chinook_Sqlite.sqlite')


################ 3, ОПРЕДЕЛЯЕМ МОДЕЛИ ######################

# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):
    class Meta:
        database = conn


# Определяем модель исполнителя
class Artist(BaseModel):
    artist_id = AutoField(column_name='ArtistId')
    name = TextField(column_name='Name', null=True)

    class Meta:
        table_name = 'Artist'


def print_last_five_artists():
    """ Печатаем последние 5 записей в таблице исполнителей"""
    print('########################################################')
    cur_query = Artist.select().limit(5).order_by(Artist.artist_id.desc())
    for item in cur_query.dicts().execute():
        print('artist: ', item)


# Создаем курсор - это специальный объект который делает запросы
# и получает их результаты
cursor = conn.cursor()

################ 2, ИСПОЛЬЗУЕМ КУРСОР  ###################

# Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")

# Получаем результат сделанного запроса
results = cursor.fetchall()
print(results)   # [('A Cor Do Som',), ('AC/DC',), ('Aaron Copland & London Symphony Orchestra',)]


######################## 5, ЧИТАЕМ ИЗ БАЗЫ ########################

# 5.1 Получение одиночной записи с методом модели Model.get()
artist = Artist.get(Artist.artist_id == 1)
# теперь у нас есть объект artist,
# с полями соответствующим данным исполнителя в конкретной строке
# а также доступными методами модели исполнителя
# этот объект можно использовать не только для чтения данных,
# но и для их обновления и удаления данной записи, в чем убедимся позже
print('artist: ', artist.artist_id, artist.name)  # artist:  1 AC/DC

# 5.2 Получение набора записей похоже на стандартный select запрос к базе,
# но осуществляемый через нашу модель Model.select()
# Обратите внимание, что к какой таблице обращаться и какие поля у нее есть
# уже определено в нашей модели и нам не надо это указывать в нашем запросе

# Формируем запрос к базе с помощью нашей ORM прослойки
# и смотрим как этот запрос будет выглядеть
query = Artist.select()
print(query)
# SELECT "t1"."ArtistId", "t1"."Name" FROM "Artist" AS "t1"

# Полезно добавить дополнительные параметры,
# уточняющие запрос, они очень похожи на SQL инструкции:
query = Artist.select().where(Artist.artist_id < 10).\
                        limit(5).order_by(Artist.artist_id.desc())
print(query)
# SELECT "t1"."ArtistId", "t1"."Name" FROM "Artist" AS "t1"
#   WHERE ("t1"."ArtistId" < 10) ORDER BY "t1"."ArtistId" DESC LIMIT 5

# Теперь, определившись с запросом к базе, мы можем получить от нее ответ,
# для удобства делаем это сразу в виде словаря
artists_selected = query.dicts().execute()
print(artists_selected)
# <peewee.ModelDictCursorWrapper object at 0x7f6fdd9bdda0>
# это итератор по полученным из базы записям, который можно обходить в цикле
for artist in artists_selected:
    print('artist: ', artist)   # artist:  {'artist_id': 9, 'name': 'BackBeat'}
    # То есть, каждая итерация соответствует одной строке таблицы
    # и соответственно одному исполнителю


################  6, СОЗДАЕМ НОВУЮ ЗАПИСЬ В БАЗЕ  #######################

# 6.1 Первый способ: Model.create() - передаем все требуемые параметры сразу
Artist.create(name='1-Qwerty')

# 6.2 Второй способ: Мы создаем объект класса нашей модели,
# работаем в коде в содержимым его полей,
# а в конце вызываем его метод .save()
artist = Artist(name='2-asdfg')
artist.save()  # save() returns the number of rows modified.
# обратите внимание, что здесь метод вызываем у объекта класса модели,
# а не у самой модели, как в первом способе

# 6.3 Третий способ - массовое добавление из коллекции
# методом модели Model.insert_many()
# Обратите внимание, что первые два метода не требуют добавления .execute(),
# а этот требует!
artists_data = [{'name': '3-qaswed'}, {'name': '4-yhnbgt'}]
Artist.insert_many(artists_data).execute()

# Визуализируем последние 5 записей в таблице исполнителей,
# чтобы убедится. что к последней добавлены 4 новые
print_last_five_artists()
# artist:  {'artist_id': 279, 'name': '4-yhnbgt'}
# artist:  {'artist_id': 278, 'name': '3-qaswed'}
# artist:  {'artist_id': 277, 'name': '2-asdfg'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}


############### 7, ОБНОВЛЯЕМ ДАННЫЕ СУЩЕСТВУЮЩЕЙ ЗАПИСИ ##############

# 7.1 Выше, способом 6.2 мы создавали новую запись,
# но так можно не только создавать новую запись, но и обновлять существующую.
# Для этого нам надо для нашего объекта указать
# уже существующий в таблице первичный ключ.

artist = Artist(name='2-asdfg+++++')
artist.artist_id = 277  # Тот самый первичный ключ
# который связывает наш объект с конкретной строке таблицы базы данных
artist.save()

print_last_five_artists()
# artist:  {'artist_id': 279, 'name': '4-yhnbgt'}
# artist:  {'artist_id': 278, 'name': '3-qaswed'}
# artist:  {'artist_id': 277, 'name': '2-asdfg+++++'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}

# 7.2 Для обновления многих записей сразу,
# можно использовать метод модели Model.update(),
# в котором указываем что именно у нас меняется,
# а метод .where() определяет по каким критериям отбираются записи
query = Artist.update(name=Artist.name + '!!!').where(Artist.artist_id > 275)
query.execute()

print_last_five_artists()
# artist:  {'artist_id': 279, 'name': '4-yhnbgt!!!'}
# artist:  {'artist_id': 278, 'name': '3-qaswed!!!'}
# artist:  {'artist_id': 277, 'name': '2-asdfg+++!!!'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty!!!'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}


###################### 8. УДАЛЯЕМ ЗАПИСЬ #######################

# 8.1 Первый способ удаления записи -
# это получение объекта записи методом Model.get() как в 5.1 выше
artist = Artist.get(Artist.artist_id == 279)
# и вызова метода удаления этой записи .delete_instance():
artist.delete_instance()

print_last_five_artists()
# artist:  {'artist_id': 278, 'name': '3-qaswed!!!'}
# artist:  {'artist_id': 277, 'name': '2-asdfg+++!!!'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty!!!'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}
# artist:  {'artist_id': 274, 'name': 'Nash Ensemble'}

# 8.2 Для удаления набора строк можно использовать Model.delete() метод
query = Artist.delete().where(Artist.artist_id > 275)
query.execute()

print_last_five_artists()
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}
# artist:  {'artist_id': 274, 'name': 'Nash Ensemble'}
# artist:  {'artist_id': 273, 'name': 'C. Monteverdi, Nigel Rogers - Chiaroscuro; London Baroque; London Cornett & Sackbu'}
# artist:  {'artist_id': 272, 'name': 'Emerson String Quartet'}
# artist:  {'artist_id': 271, 'name': 'Mela Tenenbaum, Pro Musica Prague & Richard Kapp'}


# Не забываем закрыть соединение с базой данных в конце работы
conn.close()