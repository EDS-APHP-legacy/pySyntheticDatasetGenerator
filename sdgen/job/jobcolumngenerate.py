import logging
import subprocess
import numpy as np
import pandas as pd
from .job import Job
from dsfaker.generators import Generator, Randint, RandomSample, RandomDatetime
from dsfaker.generators.str import Regex
from dsfaker.generators.autoincrement import Autoincrement
from dsfaker.generators.distributions import Vonmises

class JobColumnGenerate(Job):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.column      = gen_params['column']
        self.size        = gen_params['size']
        self.seed        = gen_params['seed']
        self.percent_null        = gen_params['percentNull']
        self.value_null        = gen_params['valueNull']
        self.id          = f'{self.table}.{self.column}.generate'
        self.data_file = f"{self.dir_tmp}{self.table}.{self.column}.csv"

    def release(self) -> list:
        return [self.id]

    def __repr__(self) ->str:
        return self.id

    def run(self) :
        size = self.size
        while size:
            decr = min(size, self.batch_size) 
            pd.DataFrame(self.get_batch( int(self.size * ( 100 - self.percent_null) / 100) )).to_csv(self.data_file, header=False, index=False, mode="a", sep= ";")
            size -= decr

    def postprocessing(self) -> bool:
        self.add_null()
        self.shuffle()
        return bool

    def shuffle(self) -> bool:
        if self.percent_null > 0:
            subprocess.run([f"{self.dir_bash}sdgen.shuffle", "-i", self.data_file, "-s", str(self.seed) ], check=True)	
        return bool

    def remove_last(self) -> bool:
        if self.percent_null > 0:
            subprocess.run([f"{self.dir_bash}sdgen.head", "-i", self.data_file, "-s", str(int(self.size * ( self.percent_null) / 100)) ], check=True)	
        return bool

    def add_null(self) -> bool:
        if self.percent_null > 0:
            if self.value_null is None:
                pd.DataFrame( index=range(int(self.size * ( self.percent_null) / 100))).to_csv(self.data_file, header=False, index=False, mode="a", sep= ";")
            else:
                pd.DataFrame(self.value_null, index=range(int(self.size * ( self.percent_null) / 100)), columns=['single']).to_csv(self.data_file, header=False, index=False, mode="a", sep= ";")
        return bool
