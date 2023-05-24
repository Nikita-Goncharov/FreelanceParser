## Парсер фріланс сайту freelancehunt.com

Складається з двох контейнерів, у першому redis(БД для celery), у другому python.

Через заданий проміжок перевіряє наявність нових тасок по заданим шляхам у словарі.


### Для запуску на своєму комп'ютері:

* Зклонувати собі цей репозиторій:
  ***git clone https://github.com/Nikita-Goncharov/FreelanceParser.git***
* Створити та активувати віртуальне середовище: ***python -venv env***
* Встановити залежності проекту: ***pip install -r requirements.txt***
* Створити бота у телеграмі за допомогою [BotFather](https://t.me/botfather?start=botostore).
* Скопіювати токен(який дав BotFather)
  та [знайдений вами id чату з ботом якого ви створили](https://awd.in.ua/yak-otrimati-id-chata-dlya-bota-telegram.html)
* Створити .env файл у директорії проекта: ***touch .env***
* Відкрити .env файл та вставити:
  ```python
  CHAT_ID='Ваш id чату у телеграмі з створеним ботом'
  BOT_TOKEN='токен бота, який при створенні надає вам BotFather'
  ```
* Запуск командою:
  ```shell 
  docker-compose -f docker-compose.yml up --build
  ```
