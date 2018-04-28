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


def get_ancestral():

    data_dir = ('{}/dbsnp/data/download/ftp.ncbi.nih.gov/snp/organisms/'
                'human_9606/database/organism_data/'.format(ROOT_DIR))
    out_dir = ('{}/dbsnp/data/proc/ancestral_allele'.format(ROOT_DIR))

    os.makedirs(out_dir, exist_ok=True)
    fin_table = '{}/SNPAncestralAllele.bcp.gz'.format(data_dir)
    allele_map = {'6':'A', '7':'C', '2':'G', '4':'T'}

    current = {'bin_id': None, 'file': None, 'data': {},}
    qprint('reading ' + fin_table)
    nline = 0
    nsnp = 0
    for line in gzip.open(fin_table):
        snp_id, allele_id, batch_id = line.decode('ascii').split('\t')
        snp_id = snp_id.zfill(9)
        bin_id = snp_id[:3]
        allele = allele_map[allele_id]

        if current['bin_id'] != bin_id:

            if current['bin_id']:
                for snp_id in sorted(current['data']):
                    out = {
                        'allele_latest': current['data'][snp_id][-1],
                        'allele_list': current['data'][snp_id],
                    }
                    print(snp_id, json.dumps(out, sort_keys=True), sep='\t',
                          file=current['file'])
                    nsnp += 1
                current['file'].close()

            current['bin_id'] = bin_id
            current['file'] = qopen('{}/{}.aa.list'.format(out_dir, bin_id), 'w')
            current['data'] = {}

        if snp_id not in current['data']:
            current['data'][snp_id] = []
        current['data'][snp_id].append(allele)

        nline += 1
        # if nline == 1000:
        #     break

    for snp_id in sorted(current['data']):
        out = {
            'allele_latest': current['data'][snp_id][-1],
            'allele_list': current['data'][snp_id],
        }
        print(snp_id, json.dumps(out, sort_keys=True), sep='\t',
              file=current['file'])
        nsnp += 1
    current['file'].close()

    qprint('loaded {} SNPs'.format(nsnp))



def parse_database():

    usage = ('USAGE:  python3  {}  ancest  \n'.format(__file__))

    if len(sys.argv) != 2 or sys.argv[1] not in ['ancestral']:
        qprint(usage)
        sys.exit(0)


    option = sys.argv[1]
    if option == 'ancestral':
        get_ancestral()




if __name__ == '__main__':

    parse_database()


# end
