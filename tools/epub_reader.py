import zipfile
from bs4 import BeautifulSoup

#Open epub
#Convert html to markdown
#Prints mardown to .json files

def main():
    table_of_contents = []
    list_of_contents = list()
    temp_dict = {
      "number": 0,
      "text": "",
      "before": "",
      "after": "",
      "cross-references": [],
      "footnotes": []
    }
    i = 0
    j = 0

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

    curr_dict = temp_dict.copy()

    #Iterates through the page file names and converts only the relevant pages into markdown
    for x in list_of_contents:
        if 2 <= i <= 39:

            #Converts the file name into output file location
            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')

            #Creates the current output file
            main_file = main_text
            out_main = open(main_file, "w", encoding="utf-8")

            #Opens the current page and reads each line in it
            with open("CatEpub/"+x, encoding="utf8") as f:
                file = f.readlines()
                for y in file:

                    #Turn current line into beautiful soup
                    curr_soup = BeautifulSoup(y, "lxml")
                    
                    #Check if current line is part of the body of the page
                    if curr_soup.body:
                        temp = ""
                        
                        chap_cont = list(curr_soup.strings)
                        if len(chap_cont) >= 0 and chap_cont[0] != "\n":
                            #format_main(curr_soup.find("p", class_="footnote").contents, out_footnote)
                            if 3 <= i <= 38 and curr_soup.find("p", class_="footnote"):
                                footnote_text = x
                                footnote_text = footnote_text.replace("OEBPS", 'Footnotes')
                                footnote_text = footnote_text.replace(".htm", '.json')

                                footnote_file = footnote_text
                                out_footnote = open(footnote_file, "w", encoding="utf-8")

                                format_footnote(curr_soup.find("p", class_="footnote").contents, out_footnote)

                                out_footnote.close()
                            else:
                                if curr_soup.find(class_="event"):
                                    if check_is_next_dict(curr_soup.find(class_="event").contents, curr_dict):
                                        temp_par = print_main_dict(curr_dict, out_main)
                                        curr_dict = temp_dict.copy()
                                        curr_dict["number"] = temp_par
                                elif curr_soup.find(class_="event01"):
                                    if check_is_next_dict(curr_soup.find(class_="event01").contents, curr_dict):
                                        temp_par = print_main_dict(curr_dict, out_main)
                                        curr_dict = temp_dict.copy()
                                        curr_dict["number"] = temp_par
                                #else:

            out_main.close()
        i = i + 1


def check_is_next_dict(soup, curr, ):
    d = soup[0]
    if d.name == "strong" and d.string is None:
        d = d.contents[1]

    if d.string:
        print(d.string, curr["number"])
    if d.string and d.string == str(curr["number"] + 1):
        return True
    else:
        return False


def print_main_dict(curr, out):

    out.write("{\n")
    for x, y in curr.items():
        print(x, y)
        out.write("\t" + str(x) + ": " + str(y) + "\n")
    out.write("}\n")

    return curr["number"]+1


def format_footnote(string, out):
    foot_dict = {
        "number": 0,
        "text": ""
    }

    foot_dict["text"] = string

    temp = ""

    for z in foot_dict["text"]:
        if str(foot_dict["text"][1]) == '<sup class="frac">*</sup>':
            if z == foot_dict["text"][0]: temp = ""
        elif z == foot_dict["text"][0]:
            foot_dict["number"] = z.string
        elif z.string:
            temp = temp + stringify(z, 0)
    foot_dict["text"] = temp

    out.write("{\n")
    for x, y in foot_dict.items():
        out.write("\t"+str(x)+": "+str(y)+"\n")
    out.write("}\n")


#def format_main(string, out):


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
    #elif str(x) == '<sup class="frac">' + curr + '</sup>':
    #    temp = ""

    #   for y in x.contents:
    #        temp = temp + stringify(y, i)
    #   return "[^" + temp + "]"
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
print("Finished!")

