# This script exports ISI exported full citation data into Citeology standard format
# This script relies on the CitationMapper (https://github.com/henrikmidtiby/CitationMapper)
# Usage: python cg_citeology_export.py isi_plaintext_output.txt
# Written by Chris Ing, 2012

import operator
from citationmapbuilder import *
from sys import argv

def main():

    #First we build a citation map builder
    cmb = citationmapbuilder()

    if(len(sys.argv) > 1):
        for arg in sys.argv:
            #If there is an argument passed, use this as the citation datafile
            #and parse this file accordingly
            cmb.parsefile(str(arg))

            #An entire networkx data structure is created, but honestly we only care 
            #about the parsed data.
            #TODO: Remove citationmapbuilder dependency
            articles = cmb.articles.copy()

        #Do a first pass over the articles and delete anything we don't have a DOI for (sorry!)
        for key in articles.keys():
            if "DI" not in articles[key]:
                del articles[key]

        #The missing articles dictionary will tell us what are the top papers that are cited by the 
        #corpus that we don't have a DOI for. 
        missing_articles = {}

        #Loop over all the articles, and check to see if references and DOI's exist
        #Print out tab-delimited data to meet the specifications of Citeology
        for key, dict in articles.iteritems():
            if "DI" in dict and "CR" in dict:
                print "".join(dict["SO"]), "\t", "".join(dict["PY"]), "\t", "".join(dict["TI"]), "\t", 

                if "AB" in dict:
                    print "".join(dict["AB"]), "\t",
                else:
                    print "Abstract not found", "\t",

                for author in dict["AU"]:
                    print author, "~", 

                print "\t",
                print "".join(dict["DI"]), "\t",

                for reference in dict["CR"]:
                    converted_cr = cmb.newIdentifierInspiredByWos2Pajek(reference).upper()
                    if converted_cr in articles:
                        print "".join(articles[converted_cr]["DI"]), "\t",

                print "\n",


                #Below we populate the missing articles dictionary to help the user improve
                #their dataset
                ref_found = 0
                for reference in dict["CR"]:
                    #convert CR string into the article dictionary key
                    converted_cr = cmb.newIdentifierInspiredByWos2Pajek(reference).upper()

                    #Here we track to see how many references aren't in our database
                    if converted_cr in articles:
                        ref_found += 1

                    else:
                        if converted_cr in missing_articles:
                            missing_articles[converted_cr] += 1
                        else:
                            missing_articles[converted_cr] = 1

                #print key, ": ", ref_found, "/", len(dict["CR"]), " references found"

        #Now we sort the missing_articles dictionary by the number of references to it and print the top 50.
        #sorted_missing_articles = sorted(missing_articles.iteritems(), key=operator.itemgetter(1), reverse=True)
        #print sorted_missing_articles[0:50]

if __name__ == "__main__":
    main()
