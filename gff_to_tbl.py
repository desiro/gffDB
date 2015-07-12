#!/usr/bin/python
# Script: gff_to_tbl.py
# Author: Daniel Desiro'
"""
Description:
    Converts ...

Usage:
    gff_to_tbl.py ... -o <input_gff_file> -n <output_gff_file> -s <string> 

Source:
    https://github.com/desiro/gffDB/blob/master/gff_to_tbl.py

"""
import os
import argparse
import re
import sys


## main function
def main(gff, tbl):
    # open the gff and tbl file
    with open(gff,'r') as gff_file:
        with open(tbl,'w') as tbl_file:
            lineNum = 1
            header = True
            topSeq = ""
            # process gff file
            for line in gff_file:
                if not re.match(r"\#",line):
                    line = line.strip()
                    lineList = line.split('\t')
                    # check if the gff file is consistent
                    if len(lineList) < 9:
                        print("Error: GFF file line " + str(lineNum) + " has less than 9 entries")
                        sys.exit()
                    seqname, source, feature, start, end, score, strand, frame, attribute = lineList
                    ## create tbl entry
                    # check if we have a new sequence name
                    if topSeq != seqname:
                        header = True
                    if header:
                        tbl_file.write(">Feature " + seqname + "\n")
                        topSeq = seqname
                        header = False
                    if strand == "+":
                        tbl_file.write(start + "\t" + end + "\t" + feature + "\n")
                    elif strand == "-":
                        tbl_file.write(end + "\t" + start + "\t" + feature + "\n")
                    # split attributes
                    ID, Name, Parent, Dbxref, Notes = getAttributes(attribute.split(';'))
                    # process features
                    # GFF       -> TBL tag conversion
                    # ID        -> transcropt_id
                    # Name      -> gene (for the gene feature)
                    # Name      -> locus_tag (for other features)
                    # Parent    -> protein_id
                    # frame     -> codon_start
                    # Dbxref    -> db_xref
                    # other     -> note
                    if (feature == "gene") and Name:
                        tbl_file.write("\t\t\t" + "gene" + "\t" + Name + "\n")
                    elif Name:
                        tbl_file.write("\t\t\t" + "locus_tag" + "\t" + Name + "\n")
                    if ID:
                        tbl_file.write("\t\t\t" + "transcript_id" + "\t" + ID + "\n")
                    if Parent:
                        tbl_file.write("\t\t\t" + "protein_id" + "\t" + Parent + "\n")
                    if frame != '.':
                        shift = str(int(frame)+1)
                        tbl_file.write("\t\t\t" + "codon_start" + "\t" + shift + "\n")
                    if Dbxref:
                        for ref in Dbxref:
                            tbl_file.write("\t\t\t" + "db_xref" + "\t" + ref + "\n")
                    if Notes:
                        tbl_file.write("\t\t\t" + "note" + "\t" + Notes + "\n")
                    # TODO:
                    # - product attributes -> tbl_file.write("\t\t\t" + "product" + "\t" + "" + "\n")
                    # - group features


## get specific attributes from the gff attribute list
def getAttributes(attList):
    ID = "";
    Name = "";
    Parent = "";
    Dbxref = [];
    Notes = "";
    # define attribute items
    for item in attList:
        attName, attText = item.split('=')
        if (attName == "ID") or (attName == "Id") or (attName == "id"):
            ID = attText
        elif (attName == "Name") or (((attName == "name") or (attName == "Gene") or (attName == "gene")) and (Name == "")):
            Name = attText
        elif (attName == "Parent") or (attName == "parent"):
            Parent = attText
        elif (attName == "Dbxref") or (attName == "dbxref") or (attName == "Db_xref") or (attName == "db_xref"):
            Dbxref = attText.split(',')
        else:
            if Notes:
                Notes = Notes + ";"
            Notes = Notes + item
    return ID, Name, Parent, Dbxref, Notes


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog = 'gff_to_tbl.py', description='Converts the source data of a gff file into a specified string.', prefix_chars='-+', epilog="")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--input_gff', '-i', dest='gff', required=True, help='input GFF file')
    parser.add_argument('--output_tbl', '-o', dest='tbl', required=True, help='output TBL file')
    
    options = parser.parse_args()    
    main(options.gff, options.tbl)

