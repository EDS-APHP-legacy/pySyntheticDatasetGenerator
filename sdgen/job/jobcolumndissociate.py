import logging
import subprocess
from .job import Job

class JobColumnDissociate(Job):
    def __init__(self, gen_params: dict):
        super().__init__(gen_params)
        self.depends = []
        self.table = gen_params['table']
        self.id = f"{self.table}.dissociate"
        self.columns = gen_params['columns']
        self.is_thread_safe = False

    def dissociate_column(self, col_index: int, col_name: str) -> bool:
        subprocess.run([f"{self.dir_bash}sdgen.cut_column", 
            "-i", 
            f"{self.dir_source}{self.table}.csv", 
            "-o",
            f"{self.dir_tmp}{self.table}.{col_name}.csv",
            "-c",
            f"{col_index!s}"])	
        return True

    def dissociate_columns(self) -> bool:
        logging.debug(f"dissociating {self.table}")
        for idx, col in enumerate(self.columns):
            logging.debug(f"dissociating {self.table}.{col}")
            self.dissociate_column(idx+1, col)
        return True

    def release(self) -> list:
        return [f'{self.table}.{column}.generate' for column in self.columns] + [self.id]

    def run(self) -> bool:
        self.dissociate_columns()
        return True
