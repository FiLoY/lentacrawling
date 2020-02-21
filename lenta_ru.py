#######################################################################################################################
# Программа на языке Python, которая собирает статьи с главной страницы сайта https://lenta.ru                        #
# Записывает в файл: ссылку, заголовок, дату, побликации, тело                                                        #
# Программа получает на вход 3 параметра                                                                              #
# --file - Путь до файла, в который будут сохраняться данные                                                          #
# --rubric - Фильтрует статьи по рубрике, может быть только либо news, либо articles                                  #
# --date - Фильтрует статьи по дате                                                                                   #
#######################################################################################################################
import sys
import argparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Crawling:
    __target_url = 'https://lenta.ru'

    def __init__(self, file, rubric=None, date=None):
        self.file = file
        self.rubric = rubric
        self.date = date

    def run(self):
        articles = []
        for link in self.get_all_links():
            article = self.get_article(link)
            # Отсев по дате
            if date:
                if self.date == article['publication_date']:
                    articles.append(article)
            else:
                articles.append(article)
        self.save(articles)


    def get_all_links(self):
        '''
        Метод получения всех ссылок, кроме ведущих на другой сайт по рубрике или без
        '''
        request = requests.get(self.__target_url)
        request.encoding = 'utf-8'

        soup = BeautifulSoup(request.text, "html.parser")
        all_a_tags = soup.find_all("a", href=True)

        all_links = []
        for link in all_a_tags:
            # :// - используется для проверки ссылки, которая указывает на другой сайт
            # Ссылка статьи на своем(lenta.ru) сайте выглядит /news/2020/02/20/premium/
            # Ссылка статьи на другой сайте(в том числе и реклама) выглядит http://motor.ru/?utm_source=menu_lenta
            href = link['href']
            if not "://" in href:
                # В зависимости от того, что указано в rubric(news или articles), то и собираем,
                # если ничего не указано - все собираем
                if (self.rubric and f"/{self.rubric}/2" in href) or \
                        (not self.rubric and ("/news/2" in href or "/articles/2" in href)):
                    all_links.append(self.__target_url + link['href'])

        # Отбрасываем повторы и возвращаем
        return set(all_links)

    def get_article(self, article_url):
        """
        Проходит по всем ссылкам и забирает необходимую информацию
        """
        request = requests.get(article_url)
        request.encoding = 'utf-8'

        soup = BeautifulSoup(request.text, 'html.parser')

        # Статьи бывают 2х видов, премиал и обычные.
        premial_article = soup.find('main', 'premial-topic')
        common_article = soup.find('div', 'b-topic__content')

        if premial_article:
            date = soup.find('div', 'premial-header__date')
            title = soup.find("div", "premial-header__middle-wrap")
        else:
            date = common_article.find('time')
            title = common_article.find("h1", "b-topic__title")
        body = soup.find("div", "js-topic__text").text

        return {'link': article_url,
                'title': title.text,
                'publication_date': self.date_normalization(date.text),
                'body': body,
                }

    def date_normalization(self, lenta_date):
        '''
        Функция нормализации даты
        В зависимости от статьи(премиал или обычная) дата может быть '00:00 30 ноября 2019' или ' 09:33, 21 февраля 2020'
        Функция избавляется от лишних символов и времени.
        Функция приводит время в машиночитаймый формат.
        '''
        date = lenta_date.strip()[6:].lstrip().split()

        russian_month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                         'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11',
                         'декабря': '12'}

        date[1] = russian_month[date[1]]
        date = [int(x) for x in date]

        return datetime(date[2], date[1], date[0])


    def save(self, articles):
        with open(self.file, 'w', encoding='utf8') as f:
            for item in articles:
                f.write(f'{"#"*20}\n{item["link"]}\n{item["title"]}\n{item["publication_date"]}\n{item["body"]}\n{"#"*20}\n')


if __name__ == '__main__':
    available_rubrics = ['news', 'articles', ]

    # Считываем аргументы
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='Путь до файла, в который будут сохраняться данные')
    parser.add_argument('--rubric', help='Фильтрует статьи по рубрике, может быть только либо news, либо articles')
    parser.add_argument('--date', help='Фильтрует статьи по дате')
    args = parser.parse_args()

    # Проверка введеной даты
    date = args.date
    if args.date:
        try:
            date = datetime.strptime(date, '%Y.%m.%d')
        except:
            sys.exit("Неверный формат даты. Пример: 2020.01.28")

    # Проверка введеной рубрики
    if not args.rubric in available_rubrics and args.rubric is not None:
        sys.exit('Фильтрация статей по рубрике, может быть только либо news, либо articles')

    # Запуск
    print('Подождите, программа выполняется')
    Crawling(args.file, args.rubric, date).run()
    print('Программа успешно отработала.')

