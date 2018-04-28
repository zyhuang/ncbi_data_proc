# -*- coding: utf-8 -*-

import os, sys, json
import gzip
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


# -------------------------------------------------------------------------


def get_ancestral(query_bin_id):
    '''query_bin_id = 0..999'''

    allele_map = {'6':'A', '7':'C', '2':'G', '4':'T'}

    data_dir = ('{}/dbsnp/data/download/ftp.ncbi.nih.gov/snp/organisms/'
                'human_9606/database/organism_data/'.format(ROOT_DIR))
    out_dir = ('{}/dbsnp/data/proc/ancestral_allele'.format(ROOT_DIR))
    os.makedirs(out_dir, exist_ok=True)

    fin_table = '{}/SNPAncestralAllele.bcp.gz'.format(data_dir)
    query_bin_id = query_bin_id.zfill(3)
    fout_list = '{}/{}.aa.list'.format(out_dir, query_bin_id)

    min_snp_id = int(query_bin_id + '000000')
    max_snp_id = int(query_bin_id + '999999')
    qprint('query range = {}-{}'.format(min_snp_id, max_snp_id))

    data = {}
    qprint('reading ' + fin_table)
    for line in gzip.open(fin_table):
        snp_id, allele_id, batch_id = line.decode('ascii').split('\t')
        if int(snp_id) < min_snp_id:
            continue
        if int(snp_id) > max_snp_id:
            break
        snp_id = snp_id.zfill(9)
        allele = allele_map[allele_id]
        if snp_id not in data:
            data[snp_id] = []
        data[snp_id].append(allele)

    qprint('loaded {} SNPs'.format(len(data)))

    fout = qopen(fout_list, 'w')
    for snp_id in sorted(data):
        out = {
            'allele_latest': data[snp_id][-1],
            'allele_list': data[snp_id],
        }
        print(snp_id, json.dumps(out, sort_keys=True), sep='\t',
              file=fout)
    fout.close()


if __name__ == '__main__':

    query_bin_id = sys.argv[1]
    get_ancestral(query_bin_id)


# end
