'''
Created on 05-Nov-2016

@author: harshit
'''

from pyxdameraulevenshtein import damerau_levenshtein_distance

def getWordsWithNonOverLapCharsWithDic(words, chars):
    words = []
    for w in words:
        for c in w:
            if c not in chars:
                words.append(w)
    return words

def getAllChars(setWords):
    allChars = set()
    for w in setWords:
        for c in w:
            allChars.add(c)
    return allChars

def getDicWords(fileName):
    dic = set()
    f = open(fileName)
    for line in f.readlines():
        dic.add(line.strip().lower())
    f.close()
    return dic
        
def getMisSpellMapping(fileName):
    map = {}
    f = open(fileName)
    currWord = ""
    for line in f.readlines():
        if line[0] == "$":
            currWord = line[1:].strip().lower()
        else:
            if currWord not in map:
                map[currWord] = [line.strip().lower()]
            else:
                map[currWord].append(line.strip().lower())
    f.close()
    return map


if __name__ == '__main__':
    dicWords = getDicWords("../data/wordsEn.txt")
    misspellMap = getMisSpellMapping("../data/missp.dat")

    wordsNotinDic = []

    print "total words that got misspelt: ", len(misspellMap.keys())
    counter = 0    
    for k in misspellMap.keys():
        if k not in dicWords:
            counter += 1
            wordsNotinDic.append(k)
            dicWords.add(k)
            
    print "num words that got misspelt but not in dic ", counter
    
    """
    for w in wordsNotinDic:
        del misspellMap[w]
    
    print "remaining words that got misspelt: ", len(misspellMap.keys())
    """
    
    allCharsInDic = getAllChars(dicWords)
    
    print allCharsInDic
    
    print "total chars in dic:", len(allCharsInDic)
    #print allCharsInDic
    
    wordsNotCharMatchWothDic = getWordsWithNonOverLapCharsWithDic(misspellMap.keys(), allCharsInDic)
   
    print "num of words that for misspelt but have non-overlapping character with dictionary:", len(wordsNotCharMatchWothDic)
    #print wordsNotCharMatchWothDic
    
    writer = open('../data/misspeltCorrectPairs.txt', 'w')
    writer2 = open('../data/misspeltCorrectPairsEditDist2.txt', 'w')
    writer3 = open('../data/misspeltCorrectPairsEditDist3.txt', 'w')
    writer4 = open('../data/misspeltCorrectPairsEditDist4.txt', 'w')
    writerabove4 = open('../data/misspeltCorrectPairsEditDistAbove4.txt', 'w')
    for k, v in misspellMap.items():
        for w in v:
            writer.write(w + "," + k+"\n")
            
            if damerau_levenshtein_distance(w, k) <= 2:
                writer2.write(w + "," + k+"\n")
            if damerau_levenshtein_distance(w, k) <= 3:
                writer3.write(w + "," + k+"\n")
            if damerau_levenshtein_distance(w, k) <= 4:
                writer4.write(w + "," + k+"\n")
            if damerau_levenshtein_distance(w, k) > 4:
                writerabove4.write(w + "," + k+"\n")
            
    
    writer.close()
    writer2.close()
    writer3.close()
    writer4.close()
    
    writer = open('../data/dicWordsSpaceSeparated.txt', 'w')
    for w in dicWords:
        for c in w:
            writer.write(c+" ")
        writer.write("\n")
    writer.close()
    
    writer = open('../data/wordsEnhancedEn.txt', 'w')
    for w in dicWords:
        writer.write(w+"\n")
    writer.close()
    
    
    
    