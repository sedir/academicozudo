#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime

base_url = 'http://academico.funcern.br/'
driver = webdriver.Chrome()
hdriver = WebDriverWait(driver, 15)
data_base = datetime.date(2016, 2, 12)
data_fim = datetime.date(2016, 6, 24)
dias = {
    'SEG/QUA': [0, 2],
    'TER/QUI': [1, 3],
    'SÁBADO': [5],
}
feriados = [
    datetime.date(2016, 4, 21),
    datetime.date(2016, 5, 26),
    datetime.date(2016, 6, 22),
]


def date_range(start, stop, skip=1):
    daycount = (stop - start).days
    for i in range(0, daycount, skip):
        yield start + datetime.timedelta(days=i)


def get_dias_aula(dias):
    weekdays = [d for d in date_range(data_base, data_fim) if d.weekday() in dias and d not in feriados]
    return weekdays


def login():
    driver.get(base_url)
    driver.implicitly_wait(30)
    driver.find_element_by_name("j_username").clear()
    driver.find_element_by_name("j_username").send_keys("paulotasso")
    driver.find_element_by_name("j_password").clear()
    driver.find_element_by_name("j_password").send_keys("pauloyu1")
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()

def entrar_na_turma():
    print('entrar na turma')
    trs = driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")
    for (index, tr) in enumerate(trs):
        tr = driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")[index]
        tr.find_elements_by_tag_name("td")[4].find_element_by_tag_name("a").click()
        cadastrar_aula()


def verificar_fim_aulas():
    print("verificacao")
    try:
        node = driver.find_element_by_xpath(
            "//*[@id=\"formListaAlunos:j_id49_body\"]/span/div/a")
        print(node)
        if node.text.startswith("Indicar final"):
            return True
        else:
            return False
    except Exception:
        return False

def cadastrar_aula():

    while not verificar_fim_aulas():
        aulanumero = int(driver.find_element_by_id("formListaAlunos:paginacao").find_element_by_tag_name("div").text.split()[0])
        dias_semana = dias[driver.find_element_by_css_selector("#j_id35 > span").text]
        aulas = get_dias_aula(dias_semana)
        print(aulanumero)
        print(dias_semana)
        print(aulas)
        print(aulas[aulanumero])

        aula = aulas[aulanumero]

        hdriver.until(EC.visibility_of_element_located((By.ID, "formListaAlunos:linkCadastrar")))
        driver.find_element_by_id("formListaAlunos:linkCadastrar").click()
        hdriver.until(EC.visibility_of_element_located((By.ID, "painelDeEdicaoContainer")))
        print('Painel apareceu!')

        avaliacao = False
        try:
            driver.implicitly_wait(1)
            if driver.find_element_by_css_selector("#painelDeEdicaoContentTable > tbody > tr:nth-child(2) > td > div > h3").text == 'Atenção!':
                avaliacao = True
        except Exception:
            pass

        if avaliacao:
            # fechar painel
            driver.find_element_by_id("j_id198:j_id199").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))
            print('Painel desapareceu!')

            print('tem que fazer a avaliação')
            driver.find_element_by_id("formListaAlunos:linkNotasParticipacao").click()

            sleep(2)
            buttons = driver.find_element_by_css_selector("#formLancamentoNPs > div:nth-child(4)").find_elements_by_tag_name("input")

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
            driver.find_element_by_id("j_id210:j_id228InputDate").send_keys(aula.strftime("%d/%m/%Y"))

            driver.find_element_by_id("j_id210:j_id257").click()
            sleep(1)

            # fechar painel
            driver.find_element_by_id("j_id198:j_id199").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))
            print('Painel desapareceu!')

    driver.find_element_by_id("j_id16").find_element_by_tag_name("a").click()


if __name__ == "__main__":
    login()
    entrar_na_turma()
