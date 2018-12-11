# -*- coding: utf-8 -*-
import yaml
import datetime
import os
import sys

import files


class Configuration:

    def __init__(self):
        self.all_week_days = {
            'SEG/QUA': [0, 2],
            'TER/QUI': [1, 3],
            'SÁBADO': [5],
        }
        self.holidays = None
        self.semester_start = None
        self.semester_end = None
        self.user = None
        self.password = None

    def save(self, file=files.get_root_file('config.yaml')):
        with open(file, 'w') as f:
            f.write(yaml.dump(self))

    @staticmethod
    def load(file=files.get_root_file('config.yaml')):
        # determine if application is a script file or frozen exe
        try:
            config_path = files.get_root_file(file)
            stream = open(config_path, 'r')

            config = yaml.load(stream)
        except:
            config = Configuration()

        return config
