#!/usr/bin/python
# Script: db_to_gff.py
# Author: Daniel Desiro'
"""
Description:
    Get information from a gffutils database and create a new gff file.

Usage:
    db_to_gff.py -g <gff_file> -d <database_file>

Source:
    https://github.com/desiro/gffDB/blob/master/db_to_gff.py

"""
import gffutils
import argparse


## main function
def main(gffFile, dataBase, batchSearch, all, features, source, seqid, start, end, strand, within):
    # opening the database
    try:
        db = gffutils.FeatureDB(dbfn=dataBase)
    except:
        print("can't open database")
    
    # getting all data
    if all:
        data = db.all_features()
        printData(data, gffFile, source, 'w')
    # getting data from batch file
    elif batchSearch:
        with open(batchSearch,'r') as batch:
            first = True
            for line in batch:
                b_feature, b_seqid, b_start, b_end, b_strand, b_within = line.split('\t')
                if b_within == 't' or b_within == 'true' or b_within == 'T' or b_within == 'True' or b_within == 'w' or b_within == 'within':
                    b_within_bool = True
                else:
                    b_within_bool = False
                data = db.region(seqid=b_seqid, start=b_start, end=b_end, strand=b_strand, featuretype=b_feature, completely_within=b_within_bool)
                if first:
                    printData(data, gffFile, source, 'w')
                    first = False
                else:
                    printData(data, gffFile, source, 'a')
    # getting single request
    else:
        featureList = None
        if features:
            featureList = features.split(',')
        data = db.region(seqid=seqid, start=start, end=end, strand=strand, featuretype=featureList, completely_within=within)
        printData(data, gffFile, source, 'w')


## print data
def printData(data, gffFile, source, write):
    # open the gff file
    with open(gffFile,write) as file:
        for entry in data:
            if source and entry.source != source:
                try:
                    next(data)
                except StopIteration:
                    pass
            else:
                file.write(str(entry) + "\n")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog = 'db_to_gff.py', description = 'Get information from a gffutils database and create a new gff file.', prefix_chars='-+', epilog="")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--gff', '-g', dest='gffFile', required=True, help='GFF file name')
    parser.add_argument('--database', '-d', dest='dataBase', required=True, help='gffutils database')
    parser.add_argument('--batch', '-b', dest='batchSearch', help='tabular file with search data; format: feature - seqid - start - end - strand - within; values can be empty; always provide 5 tabs; use t/T/true/True/w/within for within, let it empty or something else for not within')
    parser.add_argument('--all', '-a', dest='all', action='store_true', help='returns all db entries')
    parser.add_argument('--features', '-f', dest='features', help='returns all entries with the requested features; can be a comma separated list')
    parser.add_argument('--source', '-so', dest='source', help='returns features with the requested source')
    parser.add_argument('--seqid', '-sq', dest='seqid', help='returns features with the requested seqid')
    parser.add_argument('--start', '-s', dest='start', help='only returns features that start with this region or after this region')
    parser.add_argument('--end', '-e', dest='end', help='only returns features that end with this region or before this region')
    parser.add_argument('--strand', '-r', dest='strand', choices=['+', '-', '.'], help='returns only features in strand direction; \'.\' returns unstranded features')
    parser.add_argument('--within', '-w', dest='within', action='store_true', help='forces the feature to be completely within the provided --start and/or --end region')
    
    options = parser.parse_args()
    main(options.gffFile, options.dataBase, options.batchSearch, options.all, options.features, options.source, options.seqid, options.start, options.end, options.strand, options.within)

