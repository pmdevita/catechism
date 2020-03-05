import zipfile
from bs4 import BeautifulSoup

#Open epub
#Convert html to markdown
#Prints mardown to .json files


def _init_():
    tableOfContetns = []
    listOfContetns = list()
    i = 0

    #Open the Epub and extracts it to folder
    epub = "Catechism.epub"
    zip = zipfile.ZipFile(epub)
    zip.extractall(path="CatEpub")

    #Opens up spine to find order of pages
    infile = "CatEpub/volume.opf"
    with open(infile, "r") as f:
        file = f.read()
    soup = BeautifulSoup(file, "lxml")

    #Reads in the order of pages
    for link in soup.find_all('itemref'):
        tableOfContetns.append(link.get('idref'))

    #Saes the order of the pages
    for x in tableOfContetns:
        temp = soup.find(id=x)
        listOfContetns.append(temp.get('href'))

    #Iterates through the page file names and converts only the relevant pages
    for x in listOfContetns:
        if 2 <= i <= 39:

            #Converts the file name into output file location
            currFile = x
            currFile = currFile.replace("OEBPS", 'OutDocs')
            currFile = currFile.replace(".htm", '.json')

            #Creates the current output file
            outfile = currFile
            out = open(outfile, "w", encoding="utf-8")

            with open("CatEpub/"+x, encoding="utf8") as f:
                file = f.readlines()
                for y in file:
                    CurrSoup = BeautifulSoup(y, "lxml")
                    if CurrSoup.body:
                        temp = ""
                        ChapCont = list(CurrSoup.strings)
                        if len(ChapCont) >= 0 and ChapCont[0] != "\n":
                            if CurrSoup.h1:
                                ChapCont = CurrSoup.h1.contents

                                temp = temp + "#"
                                for z in ChapCont:
                                    temp = temp + stringify(z, 1)
                                temp = temp + "\n"
                            elif CurrSoup.h2:
                                ChapCont = CurrSoup.h2.contents

                                temp = temp + "##"
                                for z in ChapCont:
                                    temp = temp + stringify(z, 2)
                                temp = temp + "\n"
                            elif CurrSoup.find("p", class_="footnote"):
                                ChapCont = CurrSoup.find("p", class_="footnote").contents

                                for z in ChapCont:
                                    if str(ChapCont[1]) == '<sup class="frac">*</sup>':
                                        if z == ChapCont[0]: temp = ""
                                    elif z == ChapCont[0]:
                                        temp = temp + "[^" + stringify(z.contents[0], 0) + "]: "
                                    elif z.string:
                                        temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            elif CurrSoup.find(class_="lines_float"):
                                ChapCont = CurrSoup.find(class_="lines_float").contents

                                temp = temp + "^"
                                for z in ChapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            elif CurrSoup.find(class_="event01"):
                                ChapCont = CurrSoup.find(class_="event01").contents

                                temp = temp + "<"
                                for z in ChapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            elif CurrSoup.find(class_="event1"):
                                ChapCont = CurrSoup.find(class_="event1").contents

                                for z in ChapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            else:
                                ChapCont = CurrSoup.contents[0].contents[0].contents

                                for z in ChapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"

                        out.write(temp)
            out.close()
        i = i + 1



def stringify(x, i):
    curr = ""

    if len(x) != 0:
        for y in x:
            curr = curr + str(y)

    if x.string == x:
        return str(x)
    elif str(x) == '<span class="small">' + curr + '</span>':
        temp = "__"

        for y in x.contents:
            temp = temp + stringify(y, i)
        return temp + "__"
    elif str(x) == '<em>' + curr + '</em>':
        temp = "*"

        for y in x.contents:
            temp = temp + stringify(y, i)
        return temp + "*"
    elif str(x) == '<strong>' + curr + '</strong>':
        temp = "**"

        for y in x.contents:
            temp = temp + stringify(y, i)
        return temp + "**"
    elif str(x) == '<sup class="frac">' + curr + '</sup>':
        temp = ""

        for y in x.contents:
            temp = temp + stringify(y, i)
        return "[^"+temp+"]"
    elif str(x) == "<br/>":
        if i == 0:
            return "\n"
        else:
            j = 0
            temp = ""

            while j != i:
                temp = temp + "#"
                j += 1
            return "\n" + temp
    elif len(x.contents) != 1:
        temp = ""

        for y in x.contents:
            temp = temp + stringify(y, i)
        return temp
    else:
        return stringify(x.contents[0], i)


_init_()
print("Finished!")

