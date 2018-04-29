# -*- coding: utf-8 -*-
'''This program gets a list of bin_ids from the bcp file.

bin_id is defined as the first 3-character of zero-prefixed snp_id
e.g. rs1234567 => snp_id = 001234567 => bin_id = 001
'''
import os, sys, json, gzip


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



def get_bin_id(fin_bcp_name, fout_bin_list):

    bin_set = set()
    for line in qopen(fin_bcp_name):
        snp_id = line.decode('ascii').rstrip().split('\t')[0]
        bin_id = snp_id.zfill(9)[:3]
        bin_set.add(bin_id)

    fout = qopen(fout_bin_list, 'w')
    for bin_id in sorted(bin_set):
        print(bin_id, file=fout)
    fout.close()


if __name__ == '__main__':

    fin_bcp_name, fout_bin_list = sys.argv[1:3]
    get_bin_id(fin_bcp_name, fout_bin_list)


# end
