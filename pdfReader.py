import urllib.request
import PyPDF2
import os
import requests
import re
import justext
import argparse
import string
from spellchecker import SpellChecker


#to run the program, enter it in command line with the argument for the year to download

#takes in URL for the item page and the name of the file and downloads the corresponding pdf
def fileDownload(url,filename):             
    url = url+filename
    request = requests.get(url, stream = True)
    with open(filename, "wb") as f:
        f.write(request.content)

#reads a downloaded pdf and puts its content into txt format.
def readPDF(filename):
    x = 0
    outputname=""
    fullText=""
    pdf_file = open(filename, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    print(pdf_reader.numPages)
    outputname = re.sub(".pdf", ".txt",filename)
    print(outputname)
    while x<pdf_reader.numPages:
        page = pdf_reader.getPage(x)
        fullText+=page.extractText()
        #print(page.extractText())
        x+=1
    pdf_file.close()
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in fullText:
           if char not in punctuations:
               no_punct = no_punct + char.lower()
    writeToFile(no_punct, outputname)
    os.remove(filename)

#helper function that actually puts the text into a .txt 
def writeToFile(output, filename):
    if not os.path.exists('output'):
        os.makedirs('output')
    path = "output/"+filename
    
    file = open(path, "w", encoding ='ascii', errors= 'ignore')
    for line in output:
       
        file.write(line)
    
    file.close()
    #spellcheck(path)

#gets all the exponent pdfs for a given year.
def getURL():
   
    parser = argparse.ArgumentParser()
    parser.add_argument('dates')
    parser.add_argument('issues')
    dates = parser.parse_args().dates
    issues = parser.parse_args().issues
    filenames = []
    searchURL='http://arc.lib.montana.edu/msu-exponent/search.php?year='+'"'+dates+'"&start='+str(issues)+'&limit=15'
    print(searchURL)
    filename = dates +".txt"
    fileDownload(searchURL, filename)
    
    file = open(filename, "r")
    found = 0
    print("press y to add each file if it matches or n if it doesn't \n \n")
    for line in file:
        #print(dates)
        result= ''  
        searchDates = re.search("<dl.*/dl>", line)
        if searchDates:
           
                
            if re.search("exp\-M*[0-9]*\-[0-9]*\-[0-9]*\-[0-9]*\.pdf",searchDates[0]):
                 print(str(searchDates[0]))
                 #print(str(searchDates[0]))
                 confirmation = input()
                 if confirmation == 'y':
                    found +=1
                    result= re.search("exp\-M*[0-9]*\-[0-9]*\-[0-9]*\-[0-9]*\.pdf",searchDates[0])

        
        if result != '':
            filenames.append(result[0])
    
    file.close()
    print(found)
    #filenames = list(filter(None, filenames))
    for item in filenames:
         print(item)
    os.remove(filename)
    return filenames

def spellcheck(file):   #spellchecker library is incredibly slow and doesn't reliably correct most of the errors in the page: currently unused
    text = open(file, "r", encoding ='ascii', errors= 'ignore')
    spell = SpellChecker()
    count = 0
    for line in text:
        wordlist = re.split(' ', line)
        #print (wordlist)
        for word in wordlist:

            if word != spell.correction(word):
                print(word)
                count +=1
            #print(spell.correction(word))
            #print(spell.candidates(word))
            #print("--------------------")

    text.close()
    print(str(count) + " mispelled words")

    
def main():
    link = "http://arc.lib.montana.edu/msu-exponent/objects/"
    #filename='exp-M01-01-001-012.pdf'
    #fileDownload(link, filename)
    #readPDF(filename)

    filenames = getURL()
    for item in filenames:
        fileDownload(link, item)
        readPDF(item)
    print("done")


main()
