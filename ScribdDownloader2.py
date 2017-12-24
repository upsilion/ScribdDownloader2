import requests
from bs4 import BeautifulSoup
import os
 

#InputURL = "https://www.scribd.com/document/327402575/100-Mini-Selective-Maths-Test"

InputURLs = raw_input("Please enter the Scribd item you wish to download (If multiple, please seperate by commas): ")

InputList = InputURLs.split(",")


def Download(FolderName, FinalURL):
    ImageNameScraped = os.path.split(FinalURL)[1]
    ImageName = "Page " + ImageNameScraped[:ImageNameScraped.rfind("-")] + ".jpg"
    print ImageName

    while True:
        try:
            r2 = requests.get(FinalURL)

            with open(str(FolderName + "\\" + ImageName), "wb") as f:  #please note, the image name here is for our scarping not prestnation
                f.write(r2.content)

            break

        except requests.exceptions.MissingSchema as e:
            print "ERROR OCCURED: " + str(e)
            os.system("pause")
            pass



for InputURL in InputList:
    #making the output folder
    FolderName = InputURL[InputURL.rfind("/")+1:].replace("-"," ")
    print FolderName
    if not os.path.exists(FolderName):
        os.mkdir(FolderName)


    r = requests.get(InputURL)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    #print data.encode("ascii","ignore")
    #print soup
    #print soup.find_all('script')


    String_soup = str(soup)

    origIndex = String_soup.find("orig=")
    while origIndex >-1:
        print origIndex
        origIndex += 6
        EndIndex = String_soup.find('"', origIndex+1)

        Download(FolderName, String_soup[origIndex:EndIndex])
        origIndex = String_soup.find("orig=", origIndex+1)


    for each in soup.find_all("script"):
        stringEach = str(each)
        print stringEach
        #os.system("pause")
        startIndex = stringEach.find("pageParams.contentUrl")
        print startIndex
        #therefore real index

        if startIndex > -1:
            RealIndex = startIndex + 25
            EndIndex = stringEach.find('"', RealIndex) #note this can cause bugs

            PageURL = stringEach[RealIndex:EndIndex]
            print PageURL

            #yay we now have the link to a link

            #it is now time to use that link to get to the REAL link

            doc = requests.get(PageURL)
            try:
                doc_data = str(doc.text)
            except UnicodeEncodeError:
                doc_data = str(doc.text.encode("ascii","ignore"))

            FinalURLIndex = doc_data.rfind("orig=\\") + 7 # +6 for the len(orig=\) +1 for extra '"' in string
            FinalURLEndIndex = doc_data.find('"', FinalURLIndex+1) -1 #-1 to compensate for the extra / at the end of the URL
            FinalURL = doc_data[FinalURLIndex:FinalURLEndIndex]
            print FinalURL
            #now that we have the REAL final URL, its time to SAVE THAT IMAGE!
        
            Download(FolderName, FinalURL)
        

        #NOTE
        #for some ones, that are completely viewable in the first place, they have a weird structure that while might not break the program, will not be picked up by the program
        #basically, it lists the source JPG file directly in the HTML instead of some weird hoops
        # it should be easy as this is the only place with "orig=" in the html so it should just be fine to download these directly first
        # but thius is to do

