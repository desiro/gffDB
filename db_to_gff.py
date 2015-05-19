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
import os
import sys
import re
import gffutils
import argparse


## main function
def main(gffFile, dataBase, all, features, fCount, fTypes, source, seqid, start, end, notes, schema, strand, order, reverse, within):
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    # initialize parameters
    featureList = None
    orderList = None
    searchTuple = None
    data = None
    
    # processing the feature list
    if features is not None:
        featureList = features.split(',')
    # process the order list
    if order is not None:
        orderList = order.split(',')
    # create search tuple if possible
    if seqid is not None and start is not None and end is not None:
        searchTuple = seqid + ':' + start + '-' + end
    
    # decides the main task
    if all is True or (order is not None and searchTuple is None and (seqid is not None or start is not None or strand != 'none')):
        data = searchAll(db, searchTuple, strand, featureList, orderList, reverse, within)
    elif order is None and (seqid is not None or start is not None or end is not None):
        data = searchRegion(db, seqid, start, end, strand, featureList, within)
    elif featureList is not None:
        data = searchFeatures(db, featureList, searchTuple, strand, orderList, reverse, within)
    elif source is not None: 
        data = searchAll(db, searchTuple, strand, featureList, orderList, reverse, within)
    else:
        schema = True
    
    # print data
    printData(db, data, gffFile, dataBase, all, features, fCount, fTypes, source, seqid, start, end, notes, schema, strand, order, reverse, within, searchTuple)


## get all the data
def searchAll(db, searchTuple, strand, featureList, orderList, reverse, within):
    data = db.all_features(limit=searchTuple, strand=strand, featuretype=featureList, order_by=orderList, reverse=reverse, completely_within=within)
    return data


## get region
def searchRegion(db, seqid, start, end, strand, featureList, within):
    data = db.region(seqid=seqid, start=start, end=end, strand=strand, featuretype=featureList, completely_within=within)
    return data


## get features
def searchFeatures(db, featureList, searchTuple, strand, orderList, reverse, within):
    # get feature
    data = db.features_of_type(featureList, limit=searchTuple, strand=strand, order_by=orderList, reverse=reverse, completely_within=within)
    return data


## print data
def printData(db, data, gffFile, dataBase, all, features, fCount, fTypes, source, seqid, start, end, notes, schema, strand, order, reverse, within, searchTuple):
    # open the gff file
    with open(gffFile,'w') as file:
        
        # prints header data
        file.write("# tool: https://github.com/desiro/gffDB/blob/master/db_to_gff.py" + "\n")
        file.write("# database: " + dataBase + "\n")
        if notes is not None:
            file.write("# " + "\n")
            file.write("# notes: " + "\n")
            commentList = notes.split('#')
            for i in commentList:
                file.write("#     " + i + "\n")
        
        # prints search data
        file.write("# " + "\n")
        file.write("# search: " + "\n")
        if all is True:
            file.write("#     --all = True" + "\n")
        if features is not None:
            file.write("#     --features = " + features + "\n")
        if seqid is not None:
            file.write("#     --seqid = " + seqid + "\n")
        if start is not None:
            file.write("#     --start = " + start + "\n")
        if end is not None:
            file.write("#     --end = " + end + "\n")
        if strand != 'none':
            file.write("#     --strand = " + strand + "\n")
        if order is not None:
            file.write("#     --order = " + order + "\n")
        if reverse is True:
            file.write("#     --reverse = True" + "\n")
        if within is True:
            file.write("#     --within = True" + "\n")
        if source is not None:
            file.write("#     --source = " + source + "\n")
        if schema is True:
            file.write("#     --schema = True" + "\n")
        if fTypes is True:
            file.write("#     --fTypes = True" + "\n")
        if fCount is not None:
            file.write("#     --fCount = " + fCount + "\n")
        
        # prints additional requested database information
        if fTypes is True:
            file.write("# " + "\n")
            featureTypes = db.featuretypes()
            printFtypes = ""
            for i in featureTypes:
                printFtypes += str(i)
                printFtypes += ", "
            file.write("# feature types: " + printFtypes +  "\n")
        if fCount is not None:
            file.write("# " + "\n")
            if fCount == 'all':
                fCount = None
            countFeatures = db.count_features_of_type(featuretype=fCount)
            file.write("# feature count: " + str(countFeatures) + "\n")
        if schema is True:
            file.write("# " + "\n")
            printSchema = db.schema().split('\n')
            file.write("# database schema: " + "\n")
            for i in printSchema:
                file.write("#     " + i + "\n")
        
        # prints gff data
        file.write("# " + "\n")
        for entry in data:
            if searchTuple is None and seqid is not None and entry.seqid != seqid:
                try:
                    next(data)
                except StopIteration:
                    pass
            elif searchTuple is None and start is not None and ((within is True and (int(entry.start) < int(start))) or (within is False and (int(entry.end) <= int(start)))):
                try:
                    next(data)
                except StopIteration:
                    pass
            elif searchTuple is None and end is not None and ((within is True and (int(entry.end) > int(end))) or (within is False and (int(entry.start) >= int(end)))):
                try:
                    next(data)
                except StopIteration:
                    pass
            elif source is not None and entry.source != source:
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
    parser.add_argument('--all', '-a', dest='all', action='store_true', help='returns all db entries')
    parser.add_argument('--features', '-f', dest='features', help='returns all entries with the requested features; can be a comma separated list')
    parser.add_argument('--fCount', '-fn', dest='fCount', help='returns the number occurrences of the requested feature at the top of the gff file; use \'all\' for counting all features in the database')
    parser.add_argument('--fTypes', '-ft', dest='fTypes', action='store_true', help='returns all feature types in the database at the top of the gff file')
    parser.add_argument('--source', '-so', dest='source', help='returns features with the requested source')
    parser.add_argument('--seqid', '-sq', dest='seqid', help='returns features with the requested seqid')
    parser.add_argument('--start', '-s', dest='start', help='only returns features that start with this region or after this region')
    parser.add_argument('--end', '-e', dest='end', help='only returns features that end with this region or before this region')
    parser.add_argument('--notes', '-n', dest='notes', help='adds specific notes at the top of the gff file; provide the comment in quotation mark and use # for new line')
    parser.add_argument('--schema', '-sc', dest='schema', action='store_true', help='returns the schema of the database at the top of the gff file, this is also the default output when you do not specify anything')
    parser.add_argument('--strand', '-r', dest='strand', default='none', choices=['none', '+', '-', '.'], help='returns only features in strand direction; \'.\' returns unstranded features')
    parser.add_argument('--order', '-o', dest='order', help='order results by fields; must be a comma separated list of field names (seqid, source, featuretype, start, end, score, strand, frame, attributes, extra); could slow down the search')
    parser.add_argument('--reverse', '-v', dest='reverse', action='store_true', help='sort in descending order; only use with --order option')
    parser.add_argument('--within', '-w', dest='within', action='store_true', help='forces the feature to be completely within the provided --start and/or --end option')
    
    options = parser.parse_args()
    main(options.gffFile, options.dataBase, options.all, options.features, options.fCount, options.fTypes, options.source, options.seqid, options.start, options.end, options.notes, options.schema, options.strand, options.order, options.reverse, options.within)


# optional:
# ---------
# 
# Interact with a FeatureDB:
# gffutils.FeatureDB.children(id[, level, ...]) 	Return children of feature id.
# gffutils.FeatureDB.parents(id[, level, ...]) 	Return parents of feature id.
# gffutils.FeatureDB.execute(query) 	Execute arbitrary queries on the db.
# gffutils.FeatureDB.iter_by_parent_childs([...])
# 
# Modify a FeatureDB:
# gffutils.FeatureDB.delete(features[, ...]) 	Delete features from database.
# gffutils.FeatureDB.add_relation(parent, ...) 	Manually add relations to the database.
# gffutils.FeatureDB.set_pragmas(pragmas) 	Set pragmas for the current database connection.
# 
# Operate on features:
# gffutils.FeatureDB.interfeatures(features[, ...]) 	Construct new features representing the space between features.
# gffutils.FeatureDB.children_bp(feature[, ...]) 	Total bp of all children of a featuretype.
# gffutils.FeatureDB.merge(features[, ...]) 	Merge overlapping features together.
# gffutils.FeatureDB.create_introns([...]) 	Create introns from existing annotations.
# gffutils.FeatureDB.bed12(feature[, ...]) 	Converts feature into a BED12 format.

