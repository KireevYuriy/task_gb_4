from requests import get, utils
from datetime import datetime

url = 'http://www.cbr.ru/scripts/XML_daily.asp'
response_get = get(url)


def currency_rates(response):
    """
        Функция получения информации с url с занесением нужных значений в словарь.
        Определение и вывод текущей даты в формате y-m-d.
    """
    if response.status_code == 200:
        dict_val = {}
        string = response.content.decode('windows-1251')
        string_val = string.split('</Value></Valute>')
        for elem_val in string_val:
            odd = []
            split_char = elem_val.find('<CharCode>')
            char_code = elem_val[split_char+10:split_char+13]
            split_char = elem_val.find('<Value>')
            value = elem_val[split_char+7:split_char+14]
            split_char = elem_val.find('</Nominal>')
            idx = 0
            while elem_val[split_char-1] == '0':
                split_char -= 1
                idx += 1
            nominal = '1'
            if idx > 0:
                for i in range(idx):
                    nominal = nominal + '0'
            value = value.replace(',', '.')
            if is_number(value) is True:
                odd.append(nominal)
                odd.append(float(value))
            dict_val.setdefault(char_code, odd)

            date_idx = elem_val.find('Date')
            if date_idx != -1:
                date_str = elem_val[date_idx + 6:date_idx + 16]
                date_object = datetime.strptime(date_str, "%d.%m.%Y")
                print(datetime.date(date_object))
    else:
        print('Error')

    return dict_val


def is_number(string):
    """Функция проверки можел ли числа value на тип float"""
    try:
        float(string)
        return True
    except ValueError:
        return False


inquiry = input('Введите аббревиатуру требуемой валюты(Например USD, EUR, GBP): ')
value_all = currency_rates(response_get)
for elem in value_all.items():
    if str(elem[0]) == inquiry.upper():
        print(f'{elem[1][0]} {elem[0]} = {elem[1][1]:.2f} RUB')
