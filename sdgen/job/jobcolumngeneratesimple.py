import logging
import subprocess
import numpy as np
import pandas as pd
from dsfaker.generators import Generator, Randint, RandomSample, RandomDatetime
from dsfaker.generators.str import Regex
from dsfaker.generators.autoincrement import Autoincrement
from dsfaker.generators.distributions import Vonmises
from .jobcolumngenerate import JobColumnGenerate

class JobColumnGenerateSimple(JobColumnGenerate):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)

    def get_batch(self, size:int) -> list:
        return self.gen.get_batch(size)
