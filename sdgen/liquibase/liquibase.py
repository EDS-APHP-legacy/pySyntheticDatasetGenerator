import yaml as yaml
from io import open
import subprocess
from boltons.iterutils import remap


class Liquibase():
    def __init__(self, config: list, params:dict):
        self.config = config    
        self.params = params
        self.liquibase_file = self.params['dir_result'] + "generate_schema.yml"
    
    def translate(self) -> str:
        databaseChangeLog = {}
        precondition = []
        self.lq = {'databaseChangeLog': [{'changeSet':[{'id':1}, {'changes': self.generate_drop_table() + self.config  + self.generate_bulk_load() + self.generate_fk()}]}]}

    def generate_fk(self)-> list:
        tmp = []
        for create_table in self.config:
            for column in create_table['createTable']['columns']:
                if "constraints" in column['column'] and "referencedColumn" in column['column']['constraints']:
                    obj = {'addForeignKeyConstraint': [
                        {'baseColumnNames': column['column']['name']},
                        {'baseTableName': create_table['createTable']['tableName']},
                        {'referencedColumnNames':column['column']['constraints']['referencedColumn']},
                        {'referencedTableName': column['column']['constraints']['referencedTable']},
                        {'constraintName':f'fk_{create_table["createTable"]["tableName"]}_{column["column"]["constraints"]["referencedTable"]}_{column["column"]["name"]}'}
                        ]}
                    tmp.append(obj)
        return tmp
                
    def generate_drop_table(self) -> list:
        tmp = []
        for create_table in self.config:
            obj = {'sql':[{'sql':f"DROP TABLE IF EXISTS {create_table['createTable']['tableName']} CASCADE;"}]}
            tmp.append(obj)
        return tmp

    def generate_bulk_load(self) -> list:
        tmp = []
        for create_table in self.config:
            obj = {'sql':[{'sql':f"COPY {create_table['createTable']['tableName']} FROM '{self.params['dir_result']}{create_table['createTable']['tableName']}.csv' CSV DELIMITER ';'"}]}
            tmp.append(obj)
        return tmp
        
    def to_yaml(self) -> bool:
        self.lq = self.purify()
        with open( self.liquibase_file, 'w') as outfile:
            yaml.dump(self.lq, outfile, default_flow_style=False)

    def purify(self):#remove what liquibase do not needs...via bash...
        bad_keys = set(['regex','valueNull', 'sequenceBegin', 'source', 'genClass', 'referenceColumn', 'percentNull', 'tableSize', 'referencedTable', 'referencedColumn'])
        drop_keys = lambda path, key, value: key not in bad_keys
        clean = remap(self.lq, visit=drop_keys)
        return clean
