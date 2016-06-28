#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import yaml
import datetime

base_url = 'http://academico.funcern.br/'
driver = webdriver.Chrome()
hdriver = WebDriverWait(driver, 15)
start_date = datetime.date(2016, 2, 12)
end_date = datetime.date(2016, 6, 24)
all_week_days = {
    'SEG/QUA': [0, 2],
    'TER/QUI': [1, 3],
    'SÁBADO': [5],
}
holidays = [
    datetime.date(2016, 4, 21),
    datetime.date(2016, 5, 26),
    datetime.date(2016, 6, 22),
]
user = None
password = None


def load_config():
    global holidays, start_date, end_date, user, password
    stream = open('config.yaml', 'r')
    yml = yaml.load(stream)
    holidays = yml['feriados']
    start_date = yml['data_inicio_semestre']
    end_date = yml['data_fim_semestre']
    user = yml['usuario']
    password = yml['senha']
    stream.close()


def start():
    iterate_classes()


def setup():
    load_config()
    driver.get(base_url)
    driver.implicitly_wait(30)
    driver.find_element_by_name("j_username").clear()
    driver.find_element_by_name("j_username").send_keys(user)
    driver.find_element_by_name("j_password").clear()
    driver.find_element_by_name("j_password").send_keys(password)
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()


def get_date_range(begin, end, skip=1):
    daycount = (end - begin).days
    for i in range(0, daycount, skip):
        yield begin + datetime.timedelta(days=i)


def get_class_dates(weekdays):
    dates = [d for d in get_date_range(start_date, end_date) if d.weekday() in weekdays and d not in holidays]
    return dates


def iterate_classes():
    print('entrar na turma')
    trs = driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")
    for (index, tr) in enumerate(trs):
        tr = driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")[index]
        tr.find_elements_by_tag_name("td")[4].find_element_by_tag_name("a").click()
        register_lecture()


# noinspection PyBroadException
def check_class_finished():
    print("verificacao")
    try:
        node = driver.find_element_by_xpath(
            "//*[@id=\"formListaAlunos:j_id49_body\"]/span/div/a")
        if node.text.startswith("Indicar final"):
            return True
        else:
            return False
    except Exception:
        return False


# noinspection PyBroadException
def register_lecture():
    while not check_class_finished():
        lecture_number = int(
            driver.find_element_by_id("formListaAlunos:paginacao").find_element_by_tag_name("div").text.split()[0])
        lecture_week_days = all_week_days[driver.find_element_by_css_selector("#j_id35 > span").text]
        lecture_dates = get_class_dates(lecture_week_days)

        week_day = lecture_dates[lecture_number]

        hdriver.until(EC.visibility_of_element_located((By.ID, "formListaAlunos:linkCadastrar")))
        driver.find_element_by_id("formListaAlunos:linkCadastrar").click()
        hdriver.until(EC.visibility_of_element_located((By.ID, "painelDeEdicaoContainer")))
        print('Painel apareceu!')

        evaluation = False
        try:
            driver.implicitly_wait(1)
            if driver.find_element_by_css_selector(
                    "#painelDeEdicaoContentTable > tbody > tr:nth-child(2) > td > div > h3").text == 'Atenção!':
                evaluation = True
        except Exception:
            pass

        if evaluation:
            # fechar painel
            driver.find_element_by_id("j_id198:j_id199").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))
            print('Painel desapareceu!')

            print('tem que fazer a avaliação')
            driver.find_element_by_id("formListaAlunos:linkNotasParticipacao").click()

            sleep(2)
            buttons = driver.find_element_by_css_selector(
                "#formLancamentoNPs > div:nth-child(4)").find_elements_by_tag_name("input")

            for btn in buttons:
                try:
                    if btn.is_enabled() and btn.get_attribute("value").startswith("Lançar"):
                        btn.click()
                        driver.implicitly_wait(3)  # seconds
                        break
                except Exception:
                    print('erro no elemento')

            sleep(1)

            inputs = driver.find_element_by_id("formLancamentoNPs:j_id287").find_elements_by_tag_name("input")

            for input in inputs:
                if input.is_enabled():
                    input.clear()
                    input.send_keys("10.0")

            buttons = driver.find_element_by_css_selector(
                "#formLancamentoNPs > div:nth-child(4)").find_elements_by_tag_name("input")

            for btn in buttons:
                try:
                    if btn.is_enabled() and btn.get_attribute('value') != 'Cancelar':
                        btn.click()
                        driver.implicitly_wait(3)  # seconds
                except Exception:
                    print('erro no elemento')

            sleep(5)

            driver.find_element_by_id("j_id262:j_id263").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelNotasParticipacaoContainer")))
            print('Painel desapareceu!')

        else:
            print('vamos cadastrar a aula! =D')
            driver.find_element_by_id("j_id210:assunto").clear()
            driver.find_element_by_id("j_id210:assunto").send_keys("Gramática")
            driver.find_element_by_id("j_id210:assuntoPart").clear()
            driver.find_element_by_id("j_id210:assuntoPart").send_keys("Exercício")
            driver.find_element_by_id("j_id210:j_id228InputDate").clear()
            driver.find_element_by_id("j_id210:j_id228InputDate").send_keys(week_day.strftime("%d/%m/%Y"))

            driver.find_element_by_id("j_id210:j_id257").click()
            sleep(1)

            # fechar painel
            driver.find_element_by_id("j_id198:j_id199").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))
            print('Painel desapareceu!')

    driver.find_element_by_id("j_id16").find_element_by_tag_name("a").click()


if __name__ == "__main__":
    setup()
    start()