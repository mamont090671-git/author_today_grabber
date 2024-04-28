#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
import sys
import re
#   TODO    подключаем внешний файл с переменными и настройками
import grabber

text_elem = ''
text_button = ''
prefs = {}
desired_cap = {
    'browserName': 'android',
    'device': 'Samsung Galaxy Note 9',
    'realMobile': 'true',
    'os_version': '8.1',
    'name': 'Bstack-[Python] Sample Test'
}
texts_nameBook = {}
elements = 0

#   TODO    Грабит указанную страницу в текстовый файл
class AuthorTodayClass:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        if grabber.disable_notification:
            #
            prefs["profile.default_content_setting_values.notifications"] = 2
        if grabber.disable_image:
            #
            prefs["profile.managed_default_content_settings.images"] = 2
        if grabber.web_hidden:
            #
            chrome_options.add_argument("--headless")
        if grabber.start_maximized:
            #
            chrome_options.add_argument("start-maximized")
        if grabber.mobileEmulation:
            #
            chrome_options.add_experimental_option("mobileEmulation", desired_cap)
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver_chrome = webdriver.Chrome(options=chrome_options)
        self.out_file = open(grabber.file_name, 'w')
        self.login = grabber.login
        self.password = grabber.password

    def Read_cookies(self):
        # Загружаем куки с использованием pickle
        try:
            with open('cookies.pkl', 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver_chrome.add_cookie(cookie)
            return True
        except IndexError as e0:
            print('Error: ', e0)
            return False

    def Save_cookies(self):
        #   TODO    Сохраняем куки с помощью pickle
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(self.driver_chrome.get_cookies(), file)
        return True

    def Author_today_login(self):
        #        driver.get('https://author.today')
        time.sleep(2)
        #   TODO    Логинимся на сайте со своими учетными данными
        try:
            self.driver_chrome.find_element(By.LINK_TEXT, 'Войти').click()  # TODO    находим кнопку Вход
            time.sleep(1)
            el0 = self.driver_chrome.find_element(By.NAME, 'Login')  # TODO    Находим поле ввода логина
            el0.click()
            el0.send_keys(self.login)  # TODO    Вводим логин
            time.sleep(1)
            el0 = self.driver_chrome.find_element(By.NAME, 'Password')  # TODO    Находим поле ввода пароля
            el0.click()
            el0.send_keys(self.password)  # TODO    Вводим пароль
            self.driver_chrome.find_element(By.NAME, 'RememberMe').click()  # TODO    Находим чекбокс Запомни меня
            time.sleep(1)
            self.driver_chrome.find_element(By.CSS_SELECTOR, 'button.mt-lg').click()  # TODO    Находим кнопку Войти

            time.sleep(1)
            self.Save_cookies()

            print('Enter')
        #        driver.get(url)  # TODO    переходим на страницу книги
        except IndexError as e1:
            #
            print('Error login/Password: ', e1)

    def Copy_Book(self):
        global text_button
        global text_elem
        print('Load Book')
        '''
        title = driver0.title.split(',')
        title0 = title[0][6:]
#       title0 = title0[6:]
        author = title[2][1:]
        h = author.find(' читать онлайн')
        author = author[:h]
        print(title0)
        print(author)
        #    out_file.write(title + '\n')
        '''
        '''
        #   TODO    открываем боковое меню
        driver0.find_element(By.CSS_SELECTOR, 'button.btn.btn-brd.btn-with-icon.btn-only-icon-xs').click()
        time.sleep(1)
        #   TODO    Получаем автора
        try:
            author0 = driver0.find_element(By.CSS_SELECTOR, 'div.book-author a')
            print(str(author0.text))
        except IndexError as e:
            #
            print('Error: ', e)
        #   TODO    Обновляем страницу
        driver0.refresh()
        time.sleep(2)
        '''
        #   TODO    копируем книгу по главам в цикле
        ch = True
        while ch:
            text_button = ''
            #   TODO    находим текст главы
            try:
                #   TODO    находим блок текста
                elem = self.driver_chrome.find_element(By.CLASS_NAME, 'text-container')
            except IndexError as e:
                print('error text-container: ', e)
                continue
            text_elem = elem.text
            #   TODO    обходим либо защиту, либо ошибку в некоторых книгах
            text_elem = text_elem.replace('\u0301', '-')
            #   TODO    Проверка наличия текста
            if text_elem != '':
                #
                print('Text ok!')
            else:
                print('Empty!!!')
                time.sleep(1)
                continue
            #        time.sleep(2)
            #   TODO    Записываем главу в файл
            try:
                #
                self.out_file.write(text_elem + '\n\n')
            except IndexError as e:
                #
                print('file write error: ', e)
            time.sleep(3)
            #   TODO    Ищем кнопку перехода к следующей главе
            try:
                #
                el = self.driver_chrome.find_element(By.CLASS_NAME, 'next')
                text_button = str(el.text)
            except:
                print('Find Button Error - Class: "next"')
                ch = False  # на выход из цикла
            #   TODO    Проверяем текст кнопки перехода
            if text_button != '':
                #
                print('Button: ' + text_button)
            else:
                #
                print('Find Button Text Error')
            time.sleep(2)
            #   TODO   Если ссылка не ведет на следующую книгу, то переходим по ссылке
            if text_button.find('Следующая книга') == -1:
                #
                try:
                    self.driver_chrome.find_element(By.PARTIAL_LINK_TEXT, text_button).click()
                except:
                    ch = False
                    print('Error next Button click')
            else:
                print('End of the book')
                ch = 0
            time.sleep(1)
        #   TODO    закрываем файл
        self.out_file.close()

    def Grabber(self):
        if grabber.url_enable:
            self.driver_chrome.get(grabber.url)
            time.sleep(2)
        else:
            self.driver_chrome.get('https://author.today')
        #    driver.implicitly_wait(5)
        #   TODO    Если есть куки
        if self.Read_cookies():
            self.driver_chrome.refresh()
            print('Read_cookies')
        #   TODO    Если нет, то проходим авторизацию и сохраняем куки
        else:
            #        driver.get('https://author.today')
            #   TODO    Логинимся на сайте со своими учетными данными
            self.Author_today_login()
        time.sleep(2)
        #   TODO    Если есть аргумент, то копируем книгу
        if len(sys.argv) == 1:
            fb2 = TxtToFB2()
            self.Copy_Book()
            fb2.Fb2()
        else:
#            Test0()
            self.Copy_Book()
        #   TODO    выгружаем драйвер
        self.driver_chrome.quit()
#   TODO    Класс преобразования полученного текстового файла в fb2
class TxtToFB2:
    def __init__(self):
        self.tmp = open(grabber.tmp_file, 'w', encoding='utf-8')
        with open(grabber.file_name, 'r') as file:
            self.lines = file.readlines()
        file.close()

    @staticmethod
    def text_to_str_of_index_multi(insert_text=None, string=None, text_to_find=None):
        matches = re.finditer(text_to_find, string)
        index_array = [match.start() for match in matches]
        x = 0
        for i in index_array:
            i = i + x
            string = string[:i] + insert_text + string[i:]
            x += len(insert_text)
        return string

    @staticmethod
    def Text_to_str_of_index(insert_text=None, string=None, text_to_find=None):
        index = string.find(text_to_find)
        return string[:index] + insert_text + string[index:]

    def Fb2(self):
        y = 1
        for line in self.lines:
            line = line.replace('\n', '')
            z = line.find('Глава ')
            if z == 0:
                str_line = '<strong><p>' + line + '</p></strong>\n' if y % 2 == 0 else \
                    '</section>\n<section><strong><title>' + line + '</title></strong>\n'
                y += 1
                self.tmp.write(str_line)
            else:
                self.tmp.write('<p>' + line + '</p>\n')
        self.tmp.close()
        tmp = open(grabber.tmp_file, 'r', encoding='utf-8').read()
        fb2_head = open('head.txt', 'r', encoding='utf-8').read()
        fb2 = open(grabber.fb2_file_out, 'w', encoding='utf-8')
        fb2.write(TxtToFB2.Text_to_str_of_index(tmp, fb2_head, '</body>'))


if __name__ == '__main__':
    at = AuthorTodayClass()
    at.Grabber()
'''
def Test0(driver0=None):
    global texts_nameBook
    global elements
    print('test')
    try:
        driver0.find_element(By.PARTIAL_LINK_TEXT, 'Моя библиотека').click()
    except IndexError as e1:
        print('Error: ', e1)
    try:
        elements = driver0.find_elements(By.CSS_SELECTOR, 'h4.bookcard-title')
    except IndexError as e2:
        print('Error: ', e2)
    for element in elements:
        text = element.text
        s = driver0.find_element(By.LINK_TEXT, text)
        s0 = str(s.get_attribute('href')).replace('work', 'reader')
        #        print(text + ' - ', s0)
        texts_nameBook[text] = s0
    grabber.url = texts_nameBook['Легенда о Лазаре 9. Враг моего врага']
    driver0.get(grabber.url)
    driver0.find_element(By.CSS_SELECTOR, 'button.btn.btn-brd.btn-with-icon.btn-only-icon-xs').click()
    time.sleep(2)
    driver0.find_element(By.XPATH, '//li[text()="Глава 1"]').click()
    cur_url = driver0.current_url
    print(cur_url)

    time.sleep(2)
'''
