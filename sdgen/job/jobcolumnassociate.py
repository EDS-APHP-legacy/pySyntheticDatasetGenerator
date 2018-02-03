import logging
import os
import subprocess
from .job import Job

class JobColumnAssociate(Job):
    def __init__(self,  gen_params: dict):
        super().__init__(gen_params)
        self.table = gen_params['table']
        self.id = f"{self.table}.associate"
        self.columns = gen_params['columns']
        self.depends = [f'{self.table}.{column}.generate' for column in self.columns]
        self.is_thread_safe = False

    def associate_columns(self) -> bool:
        out = open(f"{self.dir_result}{self.table}.csv", 'wb')
        cols = [self.dir_tmp + self.table + "." + str(x) + ".csv" for x in self.columns]
        cmd = [ "paste" , "-d", ";"] + cols 
        subprocess.run(cmd, stdout=out, check=True)	
        logging.debug(f"{' '.join(cmd)}")
        return True

    def release(self) -> list:
        return [self.id]


    def run(self) -> bool:
        self.associate_columns()
        return True
