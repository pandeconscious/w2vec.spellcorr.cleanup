'''
Created on 10-Nov-2016

@author: harshit
'''

from pyxdameraulevenshtein import damerau_levenshtein_distance
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == "__main__":
    errorFile = open('../data/errorPairs.txt')
    noErrorFile = open('../data/noErrorPairs.txt')
    
    editDistError = []
    editDistNoError = []
    
    for line in errorFile.readlines():
        pair = line.strip().split(',')
        editDistError.append(damerau_levenshtein_distance(pair[0], pair[1]))
    
    for line in noErrorFile.readlines():
        pair = line.strip().split(',')
        editDistNoError.append(damerau_levenshtein_distance(pair[0], pair[1]))
        
    print "no error avg edit distance: ", np.array(editDistNoError).mean()
    print "error avg edit distance: ", np.array(editDistError).mean()
    
    maxEditDistance = max(np.array(editDistNoError).max(), np.array(editDistError).max())
   
    binEditDist = range(maxEditDistance+1)
    
    pp1 = PdfPages('../data/errorHists.pdf')
    pp2 = PdfPages('../data/noErrorHists.pdf')
    
    plt.hist(editDistError, bins=binEditDist, label='histogram for errors')
    plt.show()
    plt.close()
    
    plt.hist(editDistNoError, bins=binEditDist, label='histograms for no errors')
    plt.show()
    plt.close()
    
    
    errorFile.close()
    noErrorFile.close()