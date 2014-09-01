"""

    Algorithm:
    
    Take input N from user which specifies how many files the source file needs
    to be split into.
    
    1. Get the number of ClinVarSet tags in the XML file (NumClinVarSet)
    
    2. Divide NumClinVarSet by N to get number of ClinVarSets per file (NumPerFile)
    
    3. Initialize a counter variable say ClintVarCounter. 
    
    3. Loop through XML file and check for string '<ClinVarSet'.
    
    4. If found, then start reading records into a list.
    
    5. When a '</ClinVarSet>' end tag is found, increment the ClintVarCounter by 1.
    
    6. When ClintVarCounter == NumPerFile, write records into file. Append a timestamp to filename.
    
    7. When generating the last file, dont perform previous check. Just write the remaining records into
       the last file.
       
"""

import sys
import multiprocessing as mp
from transform_clinvar_xml_to_json import transform_clinvar
from datetime import datetime

def transform_parallel(src_file, num_files):
    """ Simple parallel execution. """
    for i in range(5):
        process = mp.Process(target=transform_clinvar, args=(src_file, 'targetfile'))
        process.start()

if __name__ == '__main__':
    """ Args: source file, num of files """
    transform_parallel(sys.argv[1], sys.argv[2])
