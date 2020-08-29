import zipfile
from bs4 import BeautifulSoup
#Requires both BS4 and LXML to be installed

#Open epub
#Convert html to markdown
#Prints mardown to .json files

def main():
    table_of_contents = []
    list_of_contents = list()
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
    soup = BeautifulSoup(file, "html.parser")

    #Reads in the order of pages
    for link in soup.find_all('itemref'):
        table_of_contents.append(link.get('idref'))

    #Saes the order of the pages
    for x in table_of_contents:
        temp = soup.find(id=x)
        list_of_contents.append(temp.get('href'))

    curr_dict = create_main_dict(1)

    #Iterates through the page file names and converts only the relevant pages into markdown
    for x in list_of_contents:
        if 5 <= i <= 35:

            #Converts the file name into output file location
            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')

            #Creates the current output file
            main_file = main_text
            out_main = open(main_file, "w", encoding="utf-8")

            curr_section = ""

            #Opens the current page and reads each line in it
            with open("CatEpub/"+x, encoding="utf8") as f:
                file = f.readlines()
                last_soup = ""
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
                                        if last_soup and last_soup.find(class_="lines_float"):
                                            temp_reference = curr_dict["cross-references"].pop()
                                            curr_dict = create_main_dict(print_main_dict(curr_dict, out_main))
                                            curr_dict["cross-references"].append(temp_reference)
                                            curr_dict["before"] = curr_section

                                        else:
                                            curr_dict = create_main_dict(print_main_dict(curr_dict, out_main))
                                            curr_dict["before"] = curr_section
                                    else:
                                        curr_dict["before"] = curr_section

                                elif curr_soup.find(class_="event01"):
                                    if check_is_next_dict(curr_soup.find(class_="event01").contents, curr_dict):
                                        curr_dict = create_main_dict(print_main_dict(curr_dict, out_main))
                                        curr_dict["before"] = curr_section
                                    else:
                                        curr_dict["before"] = curr_section

                                elif curr_soup.find(class_="lines_float"):
                                    curr_dict["cross-references"].append(curr_soup.find(class_="lines_float").contents[0].string)

                                elif curr_soup.h1:
                                    print(curr_soup.h1['id'])
                                    curr_section = curr_soup.h1['id']

                                elif curr_soup.h2:
                                    print(curr_soup.h2['id'])
                                    curr_section = curr_soup.h2['id']

                                elif curr_soup.find(class_="eventsection"):
                                    if "id" in curr_soup.find(class_="eventsection").attrs:
                                        print(curr_soup.find(class_="eventsection")['id'])
                                        curr_section = curr_soup.find(class_="eventsection")['id']

                                #else:
                                    #print("Prevet")
                            last_soup = curr_soup

            curr_dict = create_main_dict(print_main_dict(curr_dict, out_main))
            out_main.close()
        i = i + 1


def check_is_next_dict(soup, curr):

    child = soup[0]
    if child.name == "strong" and child.string is None:
        child = child.contents[1]

    if child.string and child.string == str(curr["number"] + 1):
        return True
    else:
        return False


def check_if_dict_empty(curr) :

    if curr["text"] == "":
        return True
    else:
        return False

#def check_is_wrong_references():



def print_main_dict(curr, out):

    out.write("{\n")
    for x, y in curr.items():
        out.write("\t" + str(x) + ": " + str(y) + "\n")
    out.write("}\n")

    return curr["number"]+1


def create_main_dict(num):

    main_dict = {
        "number": 0,
        "text": "",
        "before": "",
        "after": "",
        "cross-references": [],
        "footnotes": []
    }

    main_dict["number"] = num

    return main_dict


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

