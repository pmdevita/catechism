import zipfile
from bs4 import BeautifulSoup

#Open epub
#Convert html to markdown
#Prints mardown to .json files


def main():
    table_of_contents = []
    list_of_contents = list()
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
        table_of_contents.append(link.get('idref'))

    #Saes the order of the pages
    for x in table_of_contents:
        temp = soup.find(id=x)
        list_of_contents.append(temp.get('href'))

    #Iterates through the page file names and converts only the relevant pages into markdown
    for x in list_of_contents:
        if 2 <= i <= 39:

            #Converts the file name into output file location
            currFile = x
            currFile = currFile.replace("OEBPS", 'OutDocs')
            currFile = currFile.replace(".htm", '.json')

            #Creates the current output file
            outfile = currFile
            out = open(outfile, "w", encoding="utf-8")

            #Opens the current page and reads each line in it
            with open("CatEpub/"+x, encoding="utf8") as f:
                file = f.readlines()
                for y in file:
                    
                    #Turn current line into beautiful soup
                    currSoup = BeautifulSoup(y, "lxml")
                    
                    #Check if current line is part of the body of the page
                    if currSoup.body:
                        temp = ""
                        
                        chapCont = list(currSoup.strings)
                        if len(chapCont) >= 0 and chapCont[0] != "\n":
                            if currSoup.h1:
                                chapCont = currSoup.h1.contents

                                temp = temp + "#"
                                for z in chapCont:
                                    temp = temp + stringify(z, 1)
                                temp = temp + "\n"
                            elif currSoup.h2:
                                chapCont = currSoup.h2.contents

                                temp = temp + "##"
                                for z in chapCont:
                                    temp = temp + stringify(z, 2)
                                temp = temp + "\n"
                            elif currSoup.find("p", class_="footnote"):
                                chapCont = currSoup.find("p", class_="footnote").contents

                                for z in chapCont:
                                    if str(chapCont[1]) == '<sup class="frac">*</sup>':
                                        if z == chapCont[0]: temp = ""
                                    elif z == chapCont[0]:
                                        temp = temp + "[^" + stringify(z.contents[0], 0) + "]: "
                                    elif z.string:
                                        temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            elif currSoup.find(class_="lines_float"):
                                chapCont = currSoup.find(class_="lines_float").contents

                                temp = temp + "^"
                                for z in chapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            elif currSoup.find(class_="event01"):
                                chapCont = currSoup.find(class_="event01").contents

                                temp = temp + "<"
                                for z in chapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            elif currSoup.find(class_="event1"):
                                chapCont = currSoup.find(class_="event1").contents

                                for z in chapCont:
                                    temp = temp + stringify(z, 0)
                                temp = temp + "\n"
                            else:
                                chapCont = currSoup.contents[0].contents[0].contents

                                for z in chapCont:
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


if __name__ == "__main__":
    main()
