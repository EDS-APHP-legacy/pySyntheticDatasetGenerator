import sdgen as sdg
from sdgen.job import Job,  JobColumnGenerate, JobColumnDissociate, JobColumnAssociate, JobColumnGenerateSimpleText, JobFactory
import os
from sdgen.jobpool import JobPool
from sdgen.config import ConfigLoad
from sdgen.liquibase import Liquibase
import logging
import argparse


parser=argparse.ArgumentParser(
    description='''SDGEN aims at generating dataset from yaml table description. It only works on linux by now''',
    epilog="""All's well that ends well.""")
parser.add_argument('--conf', type=str,  help='The yaml config file', required=True)
parser.add_argument('--tmp', type=str,  default="tmp/", help='The temporary directory', required=False)
parser.add_argument('--result', type=str, default="output/", help='The resulting csv directory', required=False)
parser.add_argument('--source', type=str, default='input/', help='The source csv directory', required=False)
parser.add_argument('--core', type=int, default=1, help='Number of processes')
parser.add_argument('--seed', type=int, default=1, help='Seed used')
parser.add_argument('--locale', type=str, default="en", help='locale')
parser.add_argument('--batchsize', type=int, default=1000000, help='Number of rows generated before swap to disk')
args=parser.parse_args()


logging.basicConfig(level=logging.INFO)


logging.info("Step Loading")
params = dict()
params['locale']      = args.locale
params['config_yaml'] = args.conf
working_directory = os.getcwd()
params['dir_result']  = working_directory + "/" + args.result
params['dir_source']  = working_directory + "/" + args.source
params['dir_tmp']     = working_directory + "/" + args.tmp
params['dir_bash']    = working_directory + "/" + "bash/"
params['batch_size']  = args.batchsize

logging.info("Step Generate")
jp = JobPool(nb_core=args.core)

lq = ConfigLoad(params)
lq.parse()

for gen_params in lq.get_column_params(args.seed) + lq.get_table_params():
    jp.available.append(JobFactory.factory({**gen_params,  **params}))

logging.debug(jp)
jp.run_all()

logging.info("Step liquibase")
a = Liquibase(lq.tables, params)
a.translate()
a.to_yaml()
