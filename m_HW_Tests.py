# Домашнее задание к лекции 4.«Tests»

import unittest
import re  # работа с регулярками
from unittest import TestCase, skipIf  # skipIf - условия для пропуска функций теста
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # для того чтобы организовать функцю задержки на извлечение данных из java script
from selenium.webdriver.support import expected_conditions  # для WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from apps.task_mnojestva import course_duration, connection, top_3  # Пдгрузим функции
from apps.m_API_reqest_http import upload_to_YD, YaAutorize
from apps.data import FIXTURE_01, FIXTURE_02, FIXTURE_03  # Пдгрузим данные


### Задача №1 unit-tests

# Тестируем функцию: Упорядочивание курсов по продолжительности
class Test_task_m_dict_cursi(TestCase):
    
    def test_type_of(self):  # Тест правильного формата даннх
        l_list = course_duration(FIXTURE_01[0], FIXTURE_01[2], FIXTURE_01[3])
        self.assertEqual(type(l_list), list), f'Не подходящий тип файла'
        
    def test_list_num_count(self):  # Тест, содержит ли выходные данные числа указанные в durations
        l_list = course_duration(FIXTURE_01[0], FIXTURE_01[2], FIXTURE_01[3])
        s_str = ''
        for it_tup, it_lst in zip(FIXTURE_01[2],l_list):
            s_str += ''.join(it_lst)
        assert str(it_tup) in s_str, f'{it_tup} должен быть в списке'
        
    def test_list_num_progression(self):  # Тест, отсортированна ли продолжительность курсов в порядке задачи
        l_list = course_duration(FIXTURE_01[0], FIXTURE_01[2], FIXTURE_01[3])
        s_str = ''
        for it_tup, it_lst in zip(sorted(FIXTURE_01[2]),l_list):
            s_str = it_lst
            assert str(it_tup) in s_str, f'Неправильный порядок: {s_str} != {it_tup}'
        
        
# Тестируем функцию: Есть ли связь между продолжительностью курса и количеством преподавателей
class Test_task_m_dict_leng(TestCase):
    
    def test_type_of(self):  # Тест правильного формата даннх
        d_dict = connection(FIXTURE_01[1], FIXTURE_01[2], FIXTURE_01[3])
        self.assertEqual(type(d_dict), dict), f'Не подходящий тип файла'
        
    def test_associations(self):  # Тест правильного соотношения данных 'Связь есть', 'Связи нет'
        d_dict = connection(FIXTURE_01[1], FIXTURE_01[2], FIXTURE_01[3])
        l_val_1 = d_dict.get('Связи нет')
        l_val_2 = d_dict.get('Связь есть')
        if l_val_1: assert l_val_1[0] != l_val_1[1], f'Неправильная ассоциация связей неравенства'
        if l_val_2: assert l_val_2[0] == l_val_2[1], f'Неправильная ассоциация связей равенства'
        

# Тестируем функцию: Узнайте топ-3 популярных имён
class Test_task_m_list_imena1(TestCase):
    
    def test_type_of(self):  # Тест правильного формата даннх
        d_dict = top_3(FIXTURE_01[1])
        self.assertEqual(type(d_dict), dict), f'Не подходящий тип файла'
        
    def test_num_regression(self):  # Тест убывающего порядка чисел топ
        d_dict = top_3(FIXTURE_01[1])
        l_list = d_dict.values()
        result = []
        pattern = r'\d{2}|\d'  # Формат в котором ищем данные Regex(найдём только числа из текста)
        
        for elem in l_list:
            result.extend(re.findall(pattern, elem))  # Выберем с помощью regex только числа - сколько раз встречется имя
            
        for elem in result: # Список чисел должен быть отсортирован в убывающем порядке, проверяем
            i_data = 0
            assert int(elem) >= i_data, f'Неправильная последовательность ТОП 3: {result}'
            i_data = int(elem)
    

### Задача №2 Автотест API Яндекса
class Test_upload_to_YD(TestCase):
    '''
        Варианты ответа сервара зависящие от клиетна:
        
        # 201
        # {'href': 'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2FImage',
        # 'method': 'GET',
        # 'templated': False}

        # 409
        # {'description': 'Specified path "Image" points to existent directory.',
        # 'error': 'DiskPathPointsToExistentDirectoryError',
        # 'message': 'По указанному пути "Image" уже существует папка с таким именем.'}

        # 401
        # {'description': 'Unauthorized',
        # 'error': 'UnauthorizedError',
        # 'message': 'Не авторизован.'}
        
        # 400
        # {'description': 'Error validating field "path": This field is required.',
        # 'error': 'FieldValidationError',
        # 'message': 'Ошибка проверки поля "path": Это поле является обязательным.'}
        
        При вриантах кроме 201 будет срабатывать assert c описанием {t_tuple[1]} = {d_descr_01} причины
    '''
    
    def test_response_of(self):
        t_tuple = upload_to_YD(FIXTURE_02)
        d_descr_01 = t_tuple[0].get('message')
        d_descr_02 = t_tuple[0].get('href')
        if d_descr_02:  # Если пе существует(при 201) то выбеем из него название созданной папки с помощью regex
            pattern = r'([^3A%2F]+$)'  # Ищем между 3A%2F и $(концом строки)
            result = re.findall(pattern, d_descr_02)
            print(f'Папка: {result} создана')
        assert t_tuple[1] == 201, f'Папка не создана, ответ сервера: {t_tuple[1]} = {d_descr_01}'  # пример: 409 = По указанному пути "Image" уже существует папка с таким именем
        
    
### Задача №3. Дополнительная (не обязательная)
class Test_authorized_to_Ya(unittest.TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.driver = webdriver.Chrome()  # Используем браузер Хром
        self.driver.get('https://passport.yandex.ru/auth/')
        self.b = ''
        self.a = ''
    
    def wait_element(self, dalay_s=1, by=By.TAG_NAME, value=None): # Функция ожидания
            wait = WebDriverWait(self.driver, dalay_s)
            return wait.until(expected_conditions.element_to_be_clickable((By.ID, value)))
    
    def test_selenium_tester(self):
        # Опрашиваем сраницу на наличие поля 'passp-field-login'
        self.elem = self.wait_element(dalay_s=5, by=By.ID, value='passp-field-login')
        self.elem.send_keys(FIXTURE_03[0])  # введём данные: ЛОГИН, в поле с помощью .send_keys([text])
        self.elem.send_keys(Keys.ENTER)  # Нажимаем ВВОД
        
        sleep(1)  # Необходимая задержка обновления запрашиваемой инфомации, страница не усевает обновиться и поменять self.elem.accessible_name = 'Введите ваш ID'
                  # срабатывает assertNotEqual(self.b, self.a), 'Введите ваш ID'=='Введите ваш ID' при правильном вводе данных
                  # при правильных данных и задержке, страница сменится что значит 'Введите пароль'!='Введите ваш ID' -> идём дальше
        try:
            self.elem = self.wait_element(dalay_s=2, by=By.ID, value='passp-field-login')  # Проверяем страницу, изменилась или осталась прежней(при неверных данных)
            self.b = self.elem.accessible_name  # Получаем accessible_name страницы: при нверном вводе данных останется на 'Введите ваш ID', при верном перейдём на 'Введите пароль'
        except Exception:
            pass
        
        self.a = 'Введите ваш ID'
        self.assertNotEqual(self.b, self.a), f'Такй логин не годится, мы всё ещё на странице {self.b}' # Если страница осталась прежней то срабатывает assertNotEqual
        
        
        # Страница ввода ПАРОЛЯ, та же процедура что и с вводом ЛОГИНА
        self.elem = self.wait_element(dalay_s=5, by=By.ID, value='passp-field-passwd')  # Используем в этот раз функцию ожидания
        self.elem.send_keys(FIXTURE_03[1])
        self.elem.send_keys(Keys.ENTER)
        
        sleep(1)
        
        try:
            self.elem = self.wait_element(dalay_s=2, by=By.ID, value='passp-field-passwd')
            self.b = self.elem.accessible_name
        except Exception:
            pass
        
        self.a = 'Введите пароль'
        self.assertNotEqual(self.b, self.a), f'Неверный пароль, мы всё ещё на странице {self.b}'
        
        
        # Страница ПОЛЬЗОВАТЕЛЯ, та же процедура что и с вводом ЛОГИНА и ПАРОЛЯ
        sleep(4)  # Задержка больше, так как при правильных данных переход на странцу ПОЛЬЗОВАТЕЛЯ заниимет больше времени чем ЛОГИН -> ПАРОЛЬ
        
        try:
            self.elem = self.wait_element(dalay_s=5, by=By.ID, value='__next')
            self.b = self.elem.accessible_name
            print(f'**{self.elem.accessible_name}**')  #  accessible_name страницы ПОЛЬЗОВАТЕЛЯ = ''
        except Exception:
            pass
        
        self.a = ''
        self.assertEqual(self.elem.accessible_name, self.a)
        self.driver.close()
        
    
if __name__ == '__main__':
    unittest.main()
    



















