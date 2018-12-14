# SpecColl-CaD
experimenting with collections as data using the MSU exponent

## running the code
  This project can run as is, just download the code. the pdfreader file needs to be called in command line with the year you want to download as well as a position to start on the page. Call it using this format
  
  > python pdfReader.py 1895 0
  
  Since the university website only shows 15 items per page, you may need to run the program a couple times to get all the documents downloaded.
### 1890's words
<img src = /images/1890s_word_cloud.png>

### 2016 words
<img src = /images/2016_word_cloud_square.png>
  
## bag of words
  The basic bag of words analysis can concatenate all the text in the output folder into one file if you want a less granular dataset. Alternatively, if you would rather just run it on a single year, just make a file titled output.txt and paste the year to be analyzed in that file. 
  Once the file is processed it puts the bag in a format of (number of occurances) (word) with newlines between each occurrence, word pair. The bag is also available in sorted by occurrence and unsorted if either is easier to work with in a certain context. There is also functionality for making a venn diagram, dispalying shared words vs unique words, based on two separate bags as a way to highlight different types of analysis that could be done on this material.
  

<img src=/images/onldnew.png>
