### Получение и распаковка дистрибутива

1. Создайте директорию /home/root2/mptt;
2. Скачайте репозиторий и распакуйте в нее содержимое папки chtec-master;
3. В директории /home/root2/mptt создайте папку pids;
4. В директории /home/root2/mptt/readtags создайте папки tags, logs;
5. Скачайте архив `https://www.dropbox.com/s/nwccvtz8cqkqpzn/mongo_data.tar` с первоначальными настройками БД (тестовые шины, группы, рабочие места, отчеты) и распакуйте в /home/root2/mptt/data/db.

### Установка необходимого ПО

Предполагается, что вы самостоятельно можете установить и настроить Nginx, uWSGI, Redis, MongoDB, MySQL (нужно для Django), драйвер виртуального com-порта.

### Необходимые библиотеки для Python 2.7
* Pyro4
* mongo-python-driver
* pyserial
* redis-py-master
* serpent-1.7
* elementtree
* xlwt

### Регулярно выполняемые задания

Добавьте строки в crontab. Если эти возможности не нужны - закомментируйте.

0 */6 * * * root python /home/root2/mptt/readtags/correct_time.py # Автокоррекция времени у "Логики"

0 * * * * root python /home/root2/mptt/readtags/averaging.py hour # Усреднение за час и сутки

5 0 * * * root python /home/root2/mptt/readtags/averaging.py day

30 * * * * root python /home/root2/mptt/readtags/read_arch_tags.py 1_h_repeat # Вычитываение архивов за час и сутки с "Логики"

0 2 * * * root python /home/root2/mptt/readtags/read_arch_tags.py 1_d_repeat

0 0 * * 0 root python /home/root2/mptt/readtags/drop_old_collections.py # Удаление старых коллекций (по умолчанию данные хранятся 60 дней)


### Запуск
Находясь в директории /home/root2/mptt выполните ./startup

В случае успеха вы увидите рабочий экран:
![](https://www.dropbox.com/s/hprdvk5i1uys4zr/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%202014-08-05%2014.11.30.png)
