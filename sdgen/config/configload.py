import logging
from yaml import load
from io import open
from ..exceptions import *


class ConfigLoad():
    def __init__(self, params: dict):
        self.config_yaml = params['config_yaml']
        self.dir_source = params['dir_source']

    def parse(self)-> bool:
        stream = open(self.config_yaml, 'r') 
        self.tables = load(stream)
        logging.debug(f'found {self!r}')
        return True

    def __str__(self) -> str:
        return str(self.tables)
    
    def __repr__(self) -> str:
        return f'{len(self.tables)} tables'


    def get_column_params(self, seed:int) -> list:
        tmp = []
        for table in self.tables:
            for column in table['createTable']['columns']:# prepare the generation jobs
                gen_params = {}
                gen_params['seed'] = seed
                gen_params['type'] = column['column']['type']
                if "genClass" in column['column']:
                    gen_params['genClass'] = column['column']['genClass']
                else:
                    gen_params['genClass'] = 'simple'
                gen_params['table'] = table['createTable']['tableName']
                if "source" in table['createTable']:
                    continue
                else:
                    gen_params['size']  = table['createTable']['tableSize']
                gen_params['column']=column['column']['name']
                if "percentNull" in column['column']:
                    gen_params['percentNull'] = column['column']['percentNull']
                else:
                    gen_params['percentNull'] = 0
                if "sequenceBegin" in column['column']:
                    gen_params['sequenceBegin'] = column['column']['sequenceBegin']
                else:
                    gen_params['sequenceBegin'] = 1
                if "valueNull" in column['column']:
                    gen_params['valueNull'] = column['column']['valueNull'] 
                else:
                    gen_params['valueNull'] = None
                if "regex" in column['column']:
                    gen_params['regex'] = column['column']['regex']
                else:
                    gen_params['regex'] = ''
                if "constraints" in column['column']:
                    if "referencedTable" in column['column']['constraints']:
                        gen_params['referencedTable'] = column['column']['constraints']['referencedTable']
                        gen_params['referencedColumn'] = column['column']['constraints']['referencedColumn']
                        if "lookupBegin" in column['column']['constraints']:
                            gen_params['lookupBegin'] = column['column']['constraints']['lookupBegin']
                        else:
                            gen_params['lookupBegin'] = 1
                        if "lookupEnd" in column['column']['constraints']:
                            gen_params['lookupEnd'] = column['column']['constraints']['lookupEnd']
                        else:
                            gen_params['lookupEnd'] = self.get_lookup_size(column['column']['constraints']['referencedTable'])
                tmp.append(gen_params)
                seed+=1
        return tmp


    def get_table_params(self) -> list:
        tmp = []
        for table in self.tables:
            tmp.append(self.gen_table_association(table))
            if "source" in table['createTable']:
                tmp.append(self.gen_table_dissociation(table))
        return tmp

    def gen_table_association(self, table) -> list:
        tmp = {}
        tmp['table'] = table['createTable']['tableName']
        tmp['columns'] = self.get_column_list(table)
        tmp['genClass'] = 'associate'
        return tmp

    def gen_table_dissociation(self, table) -> list:
        tmp = {}
        tmp['table'] = table['createTable']['tableName']
        tmp['columns'] = self.get_column_list(table)
        tmp['source'] = table['createTable']['source']
        tmp['genClass'] = 'dissociate'
        return tmp

    def get_column_list(self, table):
        tmp = []
        for column in table['createTable']['columns']:
            tmp.append(column['column']['name'])
        return tmp

    def get_lookup_size(self, lookup_table)-> int:
        for table in self.tables:
            if table['createTable']['tableName'] == lookup_table:
                if "tableSize" in table['createTable']:
                    return table['createTable']['tableSize']
                else:
                    return self.calculate_table_size(table['createTable']['tableName'])
        raise ConfigYamlFKException(f"Bad reference to {lookup_table}")

    def calculate_table_size(self, file_name) -> int:
        file = open(f"{self.dir_source}{file_name}.csv","r")
        return sum(1 for row in file)
