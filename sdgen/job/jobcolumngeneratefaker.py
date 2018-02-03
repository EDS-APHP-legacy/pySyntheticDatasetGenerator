import logging
import subprocess
import numpy as np
import pandas as pd
from faker import Faker, Factory
from .jobcolumngenerate import JobColumnGenerate

class JobColumnGenerateFaker(JobColumnGenerate):
    def __init__(self, gen_params:dict):
        super().__init__(gen_params)
        self.locale = gen_params["locale"]
        self.faker = Factory.create(self.locale)
        self.faker.seed(self.seed)
        self.is_thread_safe = True
        self.type = gen_params["genClass"]

    def get_single(self) -> object:
        if self.type == "name":
            return self.faker.name()
        if self.type == "firstname":
            return self.faker.first_name()
        if self.type == "lastname":
            return self.faker.last_name()
        if self.type == "prefix":
            return self.faker.prefix()
        if self.type == "countrycode":
            return self.faker.country_code()
        if self.type == "city":
            return self.faker.city()
        if self.type == "streetaddress":
            return self.faker.street_address()
        if self.type == "phonenumber":
            return self.faker.phone_number()
        raise(Exception(f'undefined Job{self.type!r}'))

    def get_batch(self, size:int) -> list:
        tmp = []
        for i in range(size):
            tmp.append(self.get_single())
        return tmp

