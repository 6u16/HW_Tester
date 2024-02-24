
import requests # подгружаем библиотеку отправки запросов на сервера
import json # работа с файлами json
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # для того чтобы организовать функцю задержки на извлечение данных из java script
from selenium.webdriver.support import expected_conditions  # для WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Данные задачи № 2
url = 'https://cloud-api.yandex.net/v1/disk/resources'
params = {'path':'Image'}   # отдельно параматр, и он сохранит папку с этим именем
headers = {'Authorization': '**OAuth TOKEN**'} # Введите ваш OAuth ТОКЕН

# Данные задачи № 3
login_ya = '**LOGIN**'  # Введите ЛОГИН
passowrd_ya = r'**PASSWORD**'  # Введите ПАРОЛЬ


# загрузить файл на яндекс диск (Читаем документацию к ЯД!!!)
def upload_to_YD(data): 
    ##запрос на создание папки 'Image' 
    response = requests.put(url, params=params, headers=headers)       
    d_data = response.json()
    return response.json(), response.status_code

#print(upload_to_YD(data_yadisc))


# Авторизуемся через Selenium на Yandex
class YaAutorize:
    
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()  # Используем движок Хрома
        self.driver.get('https://passport.yandex.ru/auth/')  # Адрес страницы для взаимодействия
        self.elem = ''
        
    def wait_element(self, dalay_s=1, by=By.TAG_NAME, value=None): # Функция ожидания
        wait = WebDriverWait(self.driver, dalay_s)
        return wait.until(expected_conditions.element_to_be_clickable((By.ID, value)))
    
    def login(self, login, password):
        # Обращаемся к полю ЛОГИН
        elem = self.driver.find_element(by=By.ID, value='passp-field-login') # ищем элемент, в данном случае нам нужно поле для ввода логина <input data-t='field:input-login' в нём будет id='passp-field-login'
        # далее мы можем делать всё что захотим, в частности мы введём данные в это поле с помощью .send_keys([text])
        elem.send_keys(login)  # введём данные в это поле с помощью .send_keys([text])
        elem.send_keys(Keys.ENTER)  # Жмём ВВОД

        # Повторяем действия с полем ПАРОЛЬ и ВВОДОМ
        elem = self.wait_element(dalay_s=5, by=By.TAG_NAME, value='passp-field-passwd')  # Используем в этот раз функцию ожидания
        elem.send_keys(password)
        elem.send_keys(Keys.ENTER)

        # При авторизации иногда спрашивает ключевое слово: Дата рождения, решение такое же как и при вводе логина и пароля
        # Либо вопрос о привязке телефона и т.д

        # Проверяем что мы на странице пользователя
        elem = self.wait_element(dalay_s=5, by=By.ID, value='__next')
        if elem:
            print('Мы вошли ура!')
        self.elem = elem.tag_name
        
            
# ya = YaAutorize()
# ya.login(login_ya, passowrd_ya)
# print(ya.elem)
    



