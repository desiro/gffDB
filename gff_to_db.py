#!/usr/bin/python
# Script: gff_to_db.py
# Author: Daniel Desiro'
"""
Description:
    Convert a gff file into a new database or add it to a existing database.

Usage:
    gff_to_db.py -g <gff_file> -d <database_file>

Source:
    https://github.com/desiro/gffDB/blob/master/gff_to_db.py

"""
import os
import sys
import re
import gffutils
import argparse


def main(gffFile, dataBase, forceOv, backup, idSpec, mergeStrat, fieldKey):
    # creating a new database or adding to an excising one
    if not os.path.isfile(dataBase) or forceOv is True:
        createDB(gffFile,dataBase,forceOv,idSpec,mergeStrat, fieldKey)
    elif forceOv is False and os.path.isfile(dataBase):
        addToDB(gffFile,dataBase,idSpec,backup,mergeStrat, fieldKey)


def createDB(gffFile, dataBase, forceOv, idSpec, mergeStrat, fieldKey):
    # creating id specification list
    if fieldKey is not None:
        ids = ":" + fieldKey + ":"
    else:
        ids = re.split(r",*",idSpec)
    # creating a new database
    print("test")
    gffutils.create_db(gffFile, dbfn=dataBase, id_spec=ids, force=forceOv, verbose=False, merge_strategy=mergeStrat, force_gff=True, keep_order=True)


def addToDB(gffFile, dataBase, idSpec, backup, mergeStrat, fieldKey):
    # creating id specification list
    if fieldKey is not None:
        ids = ":" + fieldKey + ":"
    else:
        ids = re.split(r",*",idSpec)
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    print("test2")
    db.update(gffFile, make_backup=backup, id_spec=ids, verbose=False, merge_strategy=mergeStrat)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog = 'gff_to_db.py', description='Create a database from a gff file or add to an excisting database.', prefix_chars='-+', epilog="")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--gff', '-g', dest='gffFile', required=True, help='GFF file')
    parser.add_argument('--database', '-d', dest='dataBase', required=True, help='name of the database')
    parser.add_argument('--forceOV', '-f', dest='forceOv', action='store_true', help='forcefully overwrites an excisting database, else adds the data to it')
    parser.add_argument('--backup', '-b', dest='backup', action='store_true', help='creates a backup before adding to the database')
    parser.add_argument('--idSpec', '-i', dest='idSpec', default='ID,Name,transcript_id,gene_id,evidence', help='a coma seperated list for the construction of the primary key, the first arguments will be prioritized')
    parser.add_argument('--merge', '-m', dest='mergeStrat', default='error', choices=['merge', 'create_unique', 'error', 'warning'], help='merge strategy for duplicates')
    parser.add_argument('--fieldKey', '-k', dest='fieldKey', choices=['seqid', 'source', 'featuretype', 'start', 'end', 'score', 'strand', 'frame', 'attributes'], help='use GFF field value as primary key')
    
    options = parser.parse_args()
    main(options.gffFile, options.dataBase, options.forceOv, options.backup, options.idSpec, options.mergeStrat, options.fieldKey)


# optional:
# ---------
# transform: The transform kwarg is a function that accepts single gffutils.Feature object 
#            and that returns a (possibly modified) gffutils.Feature object. It is used to 
#            modify, on-the-fly, items as they are being imported into the database. It is 
#            generally used for files that don't fit the standard GFF3 or GTF specs.

