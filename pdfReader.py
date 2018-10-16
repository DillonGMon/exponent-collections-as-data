import urllib.request
import PyPDF2
import os
import requests
import re
import justext
import argparse

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
    writeToFile(fullText, outputname)
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
#gets all the exponent pdfs for a given academic year
def getURL():
   
    parser = argparse.ArgumentParser()
    parser.add_argument('dates')
    dates = parser.parse_args().dates
    filenames = []
    searchURL='http://arc.lib.montana.edu/msu-exponent/search.php?year='+'"'+dates+'"'
    print(searchURL)
    filename = dates +".txt"
    fileDownload(searchURL, filename)
    
    file = open(filename, "r")
    found = 0
    print("press y to download each file if it matches")
    for line in file:
        #print(dates)
        result= ''  #TO DO : find a solution to human error when submitting the exponent data 
        searchDates = re.search(dates, line)
        if searchDates:
            print(line)
            print(str(searchDates[0]))
            confirmation = input()
            if confirmation == 'y':
                
                  if re.search("exp\-M*[0-9]*\-[0-9]*\-[0-9]*\-[0-9]*\.pdf",line):
                    found +=1
                    result= re.search("exp\-M*[0-9]*\-[0-9]*\-[0-9]*\-[0-9]*\.pdf",line)

        
        if result != '':
            filenames.append(result[0])
    
    file.close()
    print(found)
    #filenames = list(filter(None, filenames))
    for item in filenames:
         print(item)
    #os.remove(filename)
    return filenames    
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
