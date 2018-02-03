import logging
import subprocess
from .jobcolumngeneratesimpletext import *
from .jobcolumngeneratefaker import *
from .jobcolumnassociate import JobColumnAssociate
from .jobcolumndissociate import JobColumnDissociate

class JobFactory(object):

    def factory(gen_params:dict):
        if gen_params['genClass'] == 'associate': return JobColumnAssociate(gen_params)
        if gen_params['genClass'] == 'dissociate': return JobColumnDissociate(gen_params)
        if gen_params['genClass'] == 'lookup': return JobColumnGenerateSimpleLookup(gen_params)
        if gen_params['genClass'] == 'sequence': return JobColumnGenerateSimpleSequence(gen_params)
        if gen_params['genClass'] == 'simple': 
            if gen_params['type'] == 'VARCHAR': return JobColumnGenerateSimpleText(gen_params)
            if gen_params['type'] == 'INTEGER': return JobColumnGenerateSimpleInt32(gen_params)
            #if gen_params['type'] == 'int64': return JobColumnGenerateSimpleInt64()
            if gen_params['type'] == 'REAL': return JobColumnGenerateSimpleFloat32(gen_params)
            #if gen_params['type'] == 'float64': return JobColumnGenerateSimpleFloat64()
            if gen_params['type'] == 'DATE': return JobColumnGenerateSimpleDate(gen_params)
            if gen_params['type'] == 'TIMESTAMP': return JobColumnGenerateSimpleDatetime(gen_params)
            if gen_params['type'] == 'BOOLEAN': return JobColumnGenerateSimpleBoolean(gen_params)
        return JobColumnGenerateFaker(gen_params)

    factory = staticmethod(factory)

