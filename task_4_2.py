from requests import get, utils

url = 'http://www.cbr.ru/scripts/XML_daily.asp'
response_get = get(url)


def currency_rates(response):
    """Функция получения информации с url с занесением нужных значений в словарь"""
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
            odd.append(nominal)
            odd.append(value)
            dict_val.setdefault(char_code, odd)
    else:
        print('Error')
    return dict_val


inquiry = input('Введите аббревиатуру требуемой валюты(Например USD, EUR, GBP): ')
value_all = currency_rates(response_get)
for elem in value_all.items():
    if str(elem[0]) == inquiry.upper():
        print(f'{elem[1][0]} {elem[0]} = {elem[1][1]} RUB')
