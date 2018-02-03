import logging
import subprocess

class Job():
    def __init__(self, gen_params:dict):
        self.depends     = []
        self.table       = gen_params['table']
        self.dir_tmp = gen_params['dir_tmp']
        self.batch_size = gen_params['batch_size']
        self.dir_result = gen_params['dir_result']
        self.dir_bash = gen_params['dir_bash']
        self.dir_source = gen_params['dir_source']
        self.is_thread_safe= False
        self.id = f'{self.table}.generate'

    def __str__(self):
        return f"My job id is: {self.id} and I depend on:{self.depends}"

    def __repr__(self) ->str:
        return self.id

    def release(self) -> list:
        return [self.id]

    def postprocessing(self) -> bool:
        return True

