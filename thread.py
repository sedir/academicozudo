#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from itertools import repeat
import datetime
import os
import sys
import logging
import traceback
from threading import Thread

sys.path.append(os.getcwd())

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)


class Threadzuda(Thread):
    def __init__(self, config, event_stop):
        self.base_url = 'http://academico.funcern.br/softEduc_GCI_academico/faces/paginas/restrito/redirecionamento.xhtml'
        self.log = logging.getLogger('academicozudo')

        self.holidays = None
        self.start_date = None
        self.end_date = None
        self.user = None
        self.password = None

        self.driver = None
        self.hdriver = None

        super(Threadzuda, self).__init__()
        self.config = config
        self.event_stop = event_stop

    def is_started(self):
        return self._started.is_set()

    def load_config(self):
        self.log.info('Carregando configuração...')

        try:
            self.holidays = [datetime.datetime.strptime(x.strip(), '%d/%m/%Y') for x in
                             self.config.holidays.strip().split('\n')]
            self.start_date = datetime.datetime.strptime(self.config.semester_start, '%d/%m/%Y')
            self.end_date = datetime.datetime.strptime(self.config.semester_end, '%d/%m/%Y')
            self.user = self.config.user
            self.password = self.config.password
            self.log.info('Configuração aplicada com sucesso.')

            self.driver = webdriver.Chrome()
            self.hdriver = WebDriverWait(self.driver, 15)
        except Exception:
            self.log.error('Erro ao carregar configuração. Verifique as informações e tente novamente.')
            raise

    def run(self):
        self.load_config()
        try:
            if self.login():
                self.log.info('Iniciando automação...')
                self.iterate_classes()
            else:
                self.log.error('Usuário e/ou senha incorretos. Ajuste o arquivo de configuração e tente novamente.')
        except Exception:
            self.log.error(
                'Uma falha generalizada forçou o script a encerrar. Pilha de exceção disponível no arquivo exception.log.')
            with open(os.path.join(application_path, 'exception.log'), 'a') as fe:
                traceback.print_exc(file=fe)
        finally:
            self.driver.quit()

    # noinspection PyBroadException
    def login(self):
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(0)
        self.driver.find_element_by_name("j_username").clear()
        self.driver.find_element_by_name("j_username").send_keys(self.user)
        self.driver.find_element_by_name("j_password").clear()
        self.driver.find_element_by_name("j_password").send_keys(self.password)
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.driver.implicitly_wait(2)

        try:
            self.driver.find_element_by_css_selector("#corpo > p")
            return False
        except Exception:
            return True

    @staticmethod
    def get_date_range(begin, end, skip=1):
        daycount = (end - begin).days
        for i in range(0, daycount, skip):
            yield begin + datetime.timedelta(days=i)

    def get_class_dates(self, weekdays, duplicate=False):
        dates = [d for d in Threadzuda.get_date_range(self.start_date, self.end_date) if
                 d.weekday() in weekdays and d not in self.holidays]
        if duplicate:
            dates = [x for item in dates for x in repeat(item, 2)]
        return dates

    def iterate_classes(self):
        trs = self.driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")
        for (index, tr) in enumerate(trs):
            tr = self.driver.find_element_by_id("formGeral:j_id28:tb").find_elements_by_tag_name("tr")[index]
            tds = tr.find_elements_by_tag_name("td")
            self.log.info('Entrando na turma %s / %s', tds[1].text, tds[0].text)
            tds[4].find_element_by_tag_name("a").click()
            self.register_lecture()
            self.log.info('Turma finalizada.')
            if (self.event_stop.is_set()):
                break
        self.log.info('Automação concluida.')

    # noinspection PyBroadException
    def check_class_finished(self):
        try:
            node = self.driver.find_element_by_xpath(
                "//*[@id=\"formListaAlunos:j_id49_body\"]/span/div/a")
            if node.text.startswith("Indicar final"):
                self.log.info('Esta turma atingiu a carga-horária mínima.')
                return True
            else:
                return False
        except Exception:
            return False

    # noinspection PyBroadException
    def register_lecture(self):
        while not self.check_class_finished() and not self.event_stop.is_set():
            lecture_number = int(
                self.driver.find_element_by_id("formListaAlunos:paginacao").find_element_by_tag_name(
                    "div").text.split()[0])
            lecture_week_days = self.config.all_week_days[
                self.driver.find_element_by_css_selector("#j_id35 > span").text]
            lecture_dates = self.get_class_dates(lecture_week_days, duplicate=5 in lecture_week_days)

            try:
                week_day = lecture_dates[lecture_number]
            except IndexError:
                break

            self.hdriver.until(EC.visibility_of_element_located((By.ID, "formListaAlunos:linkCadastrar")))
            self.driver.find_element_by_id("formListaAlunos:linkCadastrar").click()
            self.hdriver.until(EC.visibility_of_element_located((By.ID, "painelDeEdicaoContainer")))

            evaluation = False
            try:
                self.driver.implicitly_wait(1)
                if self.driver.find_element_by_css_selector(
                        "#painelDeEdicaoContentTable > tbody > tr:nth-child(2) > td > div > h3").text == 'Atenção!':
                    evaluation = True
                    self.log.info('Cadastro de aulas indisponível.')

            except Exception:
                pass

            if evaluation:
                self.driver.find_element_by_id("j_id198:j_id199").click()
                self.hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))

                self.log.info('Aplicando notas de participação...')

                self.driver.find_element_by_id("formListaAlunos:linkNotasParticipacao").click()

                sleep(2)
                buttons = self.driver.find_element_by_css_selector(
                    "#formLancamentoNPs > div:nth-child(4)").find_elements_by_tag_name("input")

                for btn in buttons:
                    try:
                        if btn.is_enabled() and btn.get_attribute("value").startswith("Lançar"):
                            btn.click()
                            self.driver.implicitly_wait(3)
                            break
                    except Exception:
                        pass

                sleep(1)

                inputs = self.driver.find_element_by_id("formLancamentoNPs:j_id287").find_elements_by_tag_name("input")

                for input in inputs:
                    if input.is_enabled():
                        input.clear()
                        input.send_keys("10.0")

                buttons = self.driver.find_element_by_css_selector(
                    "#formLancamentoNPs > div:nth-child(4)").find_elements_by_tag_name("input")

                for btn in buttons:
                    try:
                        if btn.is_enabled() and btn.get_attribute('value') != 'Cancelar':
                            btn.click()
                            self.driver.implicitly_wait(3)
                    except Exception:
                        pass

                sleep(5)

                self.driver.find_element_by_id("j_id262:j_id263").click()
                self.hdriver.until(EC.invisibility_of_element_located((By.ID, "painelNotasParticipacaoContainer")))
                self.log.info('Notas de participação aplicadas. Continuando o processo...')

            else:
                self.log.info('Cadastrando aula %d para a data %s...', lecture_number + 1,
                              week_day.strftime("%d/%m/%Y"))
                self.driver.find_element_by_id("j_id210:assunto").clear()
                self.driver.find_element_by_id("j_id210:assunto").send_keys(u"Gramática")
                self.driver.find_element_by_id("j_id210:assuntoPart").clear()
                self.driver.find_element_by_id("j_id210:assuntoPart").send_keys(u"Exercício")
                self.driver.find_element_by_id("j_id210:j_id228InputDate").clear()
                self.driver.find_element_by_id("j_id210:j_id228InputDate").send_keys(week_day.strftime("%d/%m/%Y"))

                self.driver.find_element_by_id("j_id210:j_id257").click()
                sleep(1)
                self.log.info('Aula cadastrada.')

                # close panel
                self.driver.find_element_by_id("j_id198:j_id199").click()
                self.hdriver.until(EC.invisibility_of_element_located((By.ID, "painelDeEdicaoContainer")))

        self.driver.find_element_by_id("j_id16").find_element_by_tag_name("a").click()
