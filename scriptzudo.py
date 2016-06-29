#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import yaml
import datetime
import os
import sys
import logging
import traceback

sys.path.append(os.getcwd())
base_url = 'http://academico.funcern.br/'
driver = webdriver.Firefox()
hdriver = WebDriverWait(driver, 15)
start_date = None
end_date = None
all_week_days = {
    'SEG/QUA': [0, 2],
    'TER/QUI': [1, 3],
    'SÁBADO': [5],
}
holidays = []
user = None
password = None
log = None
application_path = None


def prep_logs():
    global log
    log = logging.getLogger('academicozudo')
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    log.addHandler(ch)
    log.addHandler(fh)


def load_config():
    global holidays, start_date, end_date, user, password, application_path
    log.info('Carregando arquivo de configuracao...')
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    try:
        config_path = os.path.join(application_path, 'config.yaml')
        stream = open(config_path, 'r')
        yml = yaml.load(stream)
        holidays = yml['feriados']
        start_date = yml['data_inicio_semestre']
        end_date = yml['data_fim_semestre']
        user = yml['usuario']
        password = yml['senha']
        stream.close()
        log.info('Configuracao aplicada com sucesso.')
    except Exception:
        log.error('Erro ao abrir arquivo de configuracao config.yaml. Verifique e tente novamente.')
        raise


def start():
    log.info('Iniciando automacao...')
    iterate_classes()


# noinspection PyBroadException
def login():
    driver.get(base_url)
    driver.implicitly_wait(0)
    driver.find_element_by_name("j_username").clear()
    driver.find_element_by_name("j_username").send_keys(user)
    driver.find_element_by_name("j_password").clear()
    driver.find_element_by_name("j_password").send_keys(password)
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    driver.implicitly_wait(2)

    try:
        driver.find_element_by_css_selector("#corpo > p")
        return False
    except Exception:
        return True


def get_date_range(begin, end, skip=1):
    daycount = (end - begin).days
    for i in range(0, daycount, skip):
        yield begin + datetime.timedelta(days=i)


def get_class_dates(weekdays):
    dates = [d for d in get_date_range(start_date, end_date) if d.weekday() in weekdays and d not in holidays]
    return dates


def iterate_classes():
    trs = driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")
    for (index, tr) in enumerate(trs):
        tr = driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")[index]
        tds = tr.find_elements_by_tag_name("td")
        log.info('Entrando na turma %s / %s', tds[1].text, tds[0].text)
        tds[4].find_element_by_tag_name("a").click()
        register_lecture()
        log.info('Turma finalizada.')
    log.info('Automacao concluida.')


# noinspection PyBroadException
def check_class_finished():
    try:
        node = driver.find_element_by_xpath(
            "//*[@id=\"formListaAlunos:j_id49_body\"]/span/div/a")
        if node.text.startswith("Indicar final"):
            log.info('Esta turma atingiu a carga-horaria minima.')
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

        evaluation = False
        try:
            driver.implicitly_wait(1)
            if driver.find_element_by_css_selector(
                    "#painelDeEdicaoContentTable > tbody > tr:nth-child(2) > td > div > h3").text == 'Atenção!':
                evaluation = True
                log.info('Cadastro de aulas indisponivel.')

        except Exception:
            pass

        if evaluation:
            # fechar painel
            driver.find_element_by_id("j_id198:j_id199").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))

            log.info('Aplicando notas de participacao...')

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
                    pass

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
                    pass

            sleep(5)

            driver.find_element_by_id("j_id262:j_id263").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelNotasParticipacaoContainer")))
            log.info('Notas de participacao aplicadas. Continuando o processo...')

        else:
            log.info('Cadastrando aula %d para a data %s...', lecture_number + 1, week_day.strftime("%d/%m/%Y"))
            driver.find_element_by_id("j_id210:assunto").clear()
            driver.find_element_by_id("j_id210:assunto").send_keys("Gramática")
            driver.find_element_by_id("j_id210:assuntoPart").clear()
            driver.find_element_by_id("j_id210:assuntoPart").send_keys("Exercício")
            driver.find_element_by_id("j_id210:j_id228InputDate").clear()
            driver.find_element_by_id("j_id210:j_id228InputDate").send_keys(week_day.strftime("%d/%m/%Y"))

            driver.find_element_by_id("j_id210:j_id257").click()
            sleep(1)
            log.info('Aula cadastrada.')

            # fechar painel
            driver.find_element_by_id("j_id198:j_id199").click()
            hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))

    driver.find_element_by_id("j_id16").find_element_by_tag_name("a").click()


if __name__ == "__main__":
    try:
        prep_logs()
        load_config()
        try:
            if login():
                start()
            else:
                log.error('Usuario e/ou senha incorretos. Ajuste o arquivo de configuracao e tente novamente.')
        except Exception:
            log.error(
                'Uma falha generalizada forcou o script a encerrar. Pilha de excecao disponivel no arquivo exception.log.')
            with open(os.path.join(application_path, 'exception.log'), 'a') as fe:
                traceback.print_exc(file=fe)
        try:
            driver.quit()
        except Exception:
            pass
        print('Pressione Enter para sair...')
        input()
    except SystemExit as e:
        print('Pressione Enter para sair...')
        input()