# -*- coding: utf-8 -*-

import os, sys, json
from os.path import dirname, abspath

ROOT_DIR = dirname(dirname(dirname(abspath(__file__))))


def qprint(msg):
    print(':: ' + msg, file=sys.stderr, flush=True)


def qopen(fname, mode='r', verbose=True):
    if verbose:
        if mode == 'w':
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

    return open(fname, mode)


def qcmd(cmd):
    qprint(cmd)
    retcode = os.system(cmd)
    if retcode:
        raise Exception('*ERROR*: non-zero return code: \n{}\n'.format(cmd))


# -------------------------------------------------------------------------

def down_ftp(url, redown=False):

    out_dir = '{}/dbsnp/data/download'.format(ROOT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    if not redown:
        cmd = 'wget -r -nc -np {} -P {}'.format(url, out_dir)
    else:
        cmd = 'wget -r -np {} -P {}'.format(url, out_dir)
    qcmd(cmd)


def down_database():
    down_ftp('ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606/database/')


def down_xml():
    down_ftp('ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606/XML/')


def down_json():
    down_ftp('ftp://ftp.ncbi.nih.gov/snp/.redesign/latest_release/JSON/')


def down():

    usage = ('USAGE:  python3  {}  database|xml|json  \n'.format(__file__))

    if len(sys.argv) != 2 or sys.argv[1] not in ['database', 'xml', 'json']:
        qprint(usage)
        sys.exit(0)

    option = sys.argv[1]
    if option == 'database':
        down_database()
    elif option == 'xml':
        down_xml()
    elif option == 'json':
        down_json()





if __name__ == '__main__':

    down()



# end
