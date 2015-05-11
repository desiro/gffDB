#!/usr/bin/python
# Script: gffutilsBuild.py
# Author: Daniel Desiro'
# Testcall: 

# imports
import os
import sys
import getopt
import re
import gffutils


""" This function 
    - 
    - Parameters:   
    - Returns:      - 
"""
def searchGene(dataBase,searchString):
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    # get the gene
    data = db[searchString]
    return data


""" This function 
    - 
    - Parameters:   
    - Returns:      - 
"""
def getAll(dataBase,parameters):
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    # get the gene
    data = db.all_features(parameters)
    return data


""" This function 
    - 
    - Parameters:   
    - Returns:      - 
"""
def searchRegion(dataBase,searchString,parameters):
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    # concatenate strings
    if parameters:
        param = searchString + "," + parameters
    else:
        param = searchString
    # get the gene
    data = db.region(param))
    return data


""" This function 
    - 
    - Parameters:   
    - Returns:      - 
"""
def searchType(dataBase,searchString,parameters):
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    # concatenate strings
    if parameters:
        param = searchString + "," + parameters
    else:
        param = searchString
    # get the gene
    data = db.features_of_type(searchString)
    return data


""" This function prints the data
    - 
    - Parameters:   
    - Returns:      - 
"""
def printItems(data,output):
    # prints the data to file
    with open(output,'w') as file:
        for i in data:
            file.write(i)


""" This function handles the command line arguments.
    - Options are: -t or --task, -d or --database
    - Displays error message for incorrect arguments.
    - input has to be a gff file
    - for Region please provide a compatible search strin like "chr1:1-100"
    - Parameters:   argv:   command line argument
    - Returns:      taskType:   search for a "gene", "all" (features), "regions", (feature) "type"
                    dataBase:   name of the data base
                    search:     name of gene, name of chromosome and its region, feature type
                    output:     name of output file
"""
def handleOptions(argv):
    taskType = ""
    dataBase = ""
    searchString = ""
    output = ""
    parameters = ""
    # try to open needed files and return error if not possible
    try:
        opts, args = getopt.getopt(argv,"t:d:s:o:p:",["task=","database=","search","output","parameters"])
    except getopt.GetoptError:
        print "gffutilsBuild.py --t <gene/all/region/type> --d <dataBase> --s <string> --o <output> --p <string> \n"
        sys.exit(2)
    # separates input parameters
    for opt, arg in opts:
        if opt in ("--t","-task"):
            taskType = arg
        if opt in ("--d","-database"):
            dataBase = arg
        if opt in ("--s","-search"):
            searchString = arg
        if opt in ("--o","-output"):
            output = arg
        elif opt in ("--p","-parameters"):
            parameters = arg
    return taskType, dataBase, searchString, output, parameters


""" The main function of the script.
    - Parameters:   argv:   command line argument
    - Returns:      -
"""
def main(argv):
    # controls the input parameters and returns the input data
    taskType, dataBase, searchString, output, parameters = handleOptions(argv)
    # decides the task
    if taskType = "gene":
        data = searchGene(dataBase,searchString)
    if taskType = "all":
        data = getAll(dataBase,parameters)
    if taskType = "region":
        data = searchRegion(dataBase,searchString,parameters)
    elif taskType = "type":
        data = searchType(dataBase,searchString)
    # prints the results
    printItems(data,output)


if __name__ == "__main__":
    main(sys.argv[1:])

