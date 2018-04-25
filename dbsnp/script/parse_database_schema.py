# -*- coding: utf-8 -*-

import os, sys, json, gzip
from os.path import dirname, abspath, join
import re

ROOT_DIR = dirname(dirname(dirname(abspath(__file__))))


def qprint(msg):
    print(':: ' + msg, file=sys.stderr, flush=True)


def qopen(fname, mode='r', verbose=True):
    if verbose:
        if mode == 'w':
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

    if fname.endswith('.gz'):
        return gzip.open(fname, mode)
    else:
        return open(fname, mode)

# -------------------------------------------------------------------------

def print_schema(out_schema_list):


    out_dir = dirname(out_schema_list)
    os.makedirs(out_dir, exist_ok=True)

    schema_dir = ('{}/dbsnp/data/download/ftp.ncbi.nih.gov/snp/organisms/'
                  'human_9606/database/organism_schema'.format(ROOT_DIR))
    table_list = ['dbSNP_sup_table.sql.gz', 'human_9606_table.sql.gz']

    table_dict = {}
    table = None
    for table_name in table_list:
        table_name = join(schema_dir, table_name)
        for line in qopen(table_name):
            line = line.decode('ascii').rstrip()
            if line.startswith('CREATE TABLE'):
                table = re.findall(r'\[(.*?)\]', line)[0]
                if table not in table_dict:
                    table_dict[table] = []
            elif line.startswith('['):
                table_dict[table].append(line.split()[0][1:-1])

    fout = qopen(out_schema_list, 'w')
    for t in sorted(table_dict):
        print(t, ','.join(table_dict[t]), sep='\t', file=fout)
    fout.close()


if __name__ == '__main__':

    out_schema_list = '../data/proc/schema/schema.list'
    print_schema(out_schema_list)


# end
