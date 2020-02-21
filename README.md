## Description
Программа на языке Python, которая собирает статьи с главной страницы сайта https://lenta.ru
Записывает в файл: ссылку, заголовок, дату, побликации, тело статьи

Программа получает на вход 3 параметра:

 - --file - Путь до файла, в который будут сохраняться данные

 - --rubric - необязательный параметр, фильтрует статьи по рубрике, может быть только либо news, либо articles. Если не указан, должны собираться все статьи

 - --date - необязательный параметр, фильтрует статьи по дате. Поддерживается только формат в виде: `YYYY.MM.DD`
 
Пример запуска программы:
`python lenta_ru.py --file=”/home/Ivanov/crawler/data/lenta_ru.pkl” --rubric=news --date=2020.01.28`

## Technical specifications
 - python 3.8
 - beautifulsoup4 4.8.2
 - requests 2.23.0

## Installation
Инструкция установки для командной оболочки bash или zsh.

Для нормальной установки и запуска программы необходим python 3.8.

1. Скачайте: 
    * если git установлен: `git clone https://github.com/FiLoY/lentacrawling.git`
    * если git не установлен: скачайте программу https://github.com/FiLoY/lentacrawling
2. Зайдите в папку `cd lentacrawling`
3. Установите дополнительные пакеты `pip install -r requirements.txt`, если они отсутствуют. Желательно устанавливать в виртуальном окружении.
3. Запустите программу `python lenta_ru.py --file=/Users/file.data`.