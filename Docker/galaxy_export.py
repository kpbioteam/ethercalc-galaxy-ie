#!/usr/bin/python
import os
import csv
import json

from galaxy_ie_helpers import put


def csv_to_tsv(infile, outfile):
    with open(outfile, 'w+') as fout, open(infile, 'r') as fin:
        csv.writer(fout, delimiter="\t").writerows(csv.reader(fin))


def get_audit_trail(audit_file):
    try:
        with open('dump.json') as d, open(audit_file, 'w+') as fout:
            j = json.load(d)
            audit = j.get('audit-galaxy')
            for command in audit:
                fout.write(command.encode('UTF8') + '\n')
    except:
        with open(audit_file, 'w+') as fout:
            fout.write("no edits were made to your dataset")


if __name__ == "__main__":
    # get info on import dataset for naming
    hid = os.environ['DATASET_HID']
    audit_file = 'ethercalc audit trail for dataset '+hid
    export_file = 'ethercalc export on dataset '+hid

    # send worksheet to galaxy history
    csv_to_tsv('ethercalc_saved', export_file)

    # get audit trail of worksheet, output one command per line
    get_audit_trail(audit_file)

    # send outputs to Galaxy
    put(audit_file, file_type='txt')
    put(export_file, file_type='tabular')
