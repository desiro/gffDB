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
def createDB(gffFile,dataBase,forceOv,idSpec):
    # creating id specification list
    ids = re.split(r",*",idSpec)
    # creating a new database
    print("test")
    db = gffutils.create_db(gffFile, dbfn=dataBase, id_spec=ids, force=forceOv, verbose=False, merge_strategy="create_unique", force_gff=True, keep_order=True)


""" This function 
    - 
    - Parameters:   
    - Returns:      - 
"""
def addToDB(gffFile,dataBase,idSpec,backup):
    # creating id specification list
    ids = re.split(r",*",idSpec)
    # opening the database
    db = gffutils.FeatureDB(dbfn=dataBase)
    db = FeatureDB.update(gffFile, make_backup=backup, id_spec=ids, verbose=False, merge_strategy="create_unique", force_gff=True, keep_order=True)


""" This function handles the command line arguments.
    - Options are: -t or --task, -g or --gffFile
    - Displays error message for incorrect arguments.
    - input has to be a gff file
    - Parameters:   argv:   command line argument
    - Returns:      taskType:   either "create" a new db or "add" to a existing one
                    gffFile:    gff file with the protein data
                    dataBase:   name of the data base
                    forceOv:    forcefully overwrites an existing db
"""
def handleOptions(argv):
    taskType = ""
    gffFile = ""
    dataBase = ""
    idSpec = "ID,Name,transcript_id,gene_id,evidence"
    forceOv = False
    backup = False
    # try to open needed files and return error if not possible
    try:
        opts, args = getopt.getopt(argv,"t:g:d:i:fb",["task=","gffFile=","database=","idSpec","force","backup"])
    except getopt.GetoptError:
        print "gffutilsBuild.py --t <create/add> --f <gffFile> --d <dataBase> \n"
        sys.exit(2)
    # separates input parameters
    for opt, arg in opts:
        if opt in ("--t","-task"):
            taskType = arg
        if opt in ("--g","-gffFile"):
            gffFile = arg
        if opt in ("--d","-database"):
            dataBase = arg
        if opt in ("--i","-idSpec"):
            idSpec = arg
        if opt in ("--f","-force"):
            forceOv = True
        elif opt in ("--b","-backup"):
            backup = True
    return taskType, gffFile, dataBase, forceOv, idSpec, backup


""" The main function of the script.
    - Parameters:   argv:   command line argument
    - Returns:      -
"""
def main(argv):
    # controls the input parameters and returns the input data
    taskType, gffFile, dataBase, forceOv, idSpec, backup = handleOptions(argv)
    # decides the task and creates or adds the data
    if taskType == "create":
        createDB(gffFile,dataBase,forceOv,idSpec)
    elif taskType == "add":
        addToDB(gffFile,dataBase,idSpec,backup)


if __name__ == "__main__":
    main(sys.argv[1:])

