import logging
import subprocess
import numpy as np
import pandas as pd
from dsfaker.generators import Generator, Randint, RandomSample, RandomDatetime
from dsfaker.generators.str import Regex
from .jobcolumngeneratesimple import JobColumnGenerateSimple
from dsfaker.generators import Generator, Randint, RandomSample, RandomDatetime
from dsfaker.generators.str import Regex
from dsfaker.generators.autoincrement import Autoincrement
from dsfaker.generators.distributions import Vonmises

class JobColumnGenerateSimpleText(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.regex       = gen_params['regex']
        self.is_thread_safe = False
        self.gen =  Regex(self.regex, seed=self.seed)

class JobColumnGenerateSimpleSequence(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.sequenceBegin = gen_params['sequenceBegin']
        self.gen = Autoincrement(start=self.sequenceBegin, step=1, dtype=np.int32)

class JobColumnGenerateSimpleDate(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.gen = RandomDatetime(Vonmises(mu=0, kappa=1.8, seed=self.seed), start=np.datetime64("2011-06-15"), end=np.datetime64("2019-01-01"),unit="D")

class JobColumnGenerateSimpleDatetime(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.gen = RandomDatetime(Vonmises(mu=0, kappa=1.8, seed=self.seed), start=np.datetime64("2011-06-15 00:00:00"), end=np.datetime64("2019-01-01 00:00:00"),unit="s")

class JobColumnGenerateSimpleFloat32(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.gen = RandomSample(seed=self.seed)

class JobColumnGenerateSimpleInt32(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.gen = Randint(1, 1000, seed=self.seed)

class JobColumnGenerateSimpleBoolean(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.gen = Randint(0, 1, seed=self.seed)

class JobColumnGenerateSimpleLookup(JobColumnGenerateSimple):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.is_thread_safe = True
        self.base_table = gen_params['referencedTable']
        self.base_column = gen_params['referencedColumn']
        self.depends = [f"{self.base_table}.{self.base_column}.generate"]
        self.gen = Randint(gen_params['lookupBegin'], gen_params['lookupEnd']+1, seed=self.seed)
    
    def postprocessing(self) -> bool:
        subprocess.run([f"{self.dir_bash}sdgen.lookup", 
            "-l", 
            f"{self.dir_tmp}{self.table}.{self.column}.csv", 
            "-r",
            f"{self.dir_tmp}{self.base_table}.{self.base_column}.csv"
            ])	
        self.add_null()
        self.shuffle()
        return bool
