import zipfile
from bs4 import BeautifulSoup
#Requires both BS4 and LXML to be installed

#Open epub
#Convert html to markdown
#Prints mardown to .json files

page_number = 0

main_dict = {
    "number": 0,
    "text": "",
    "before": "",
    "after": "",
    "cross-references": [],
    "footnotes": []
}

toc_dict = {

}

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

    create_main_dict(1)

    #Iterates through the page file names and converts only the relevant pages into markdown
    for x in list_of_contents:
        if 5 <= i <= 35:

            #Converts the file name into output file location
            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')

            footnote_text = x
            footnote_text = footnote_text.replace("OEBPS", 'Footnotes')
            footnote_text = footnote_text.replace(".htm", '.json')

            #Creates the current output file
            main_file = main_text
            out_main = open(main_file, "w", encoding="utf-8")

            footnote_file = footnote_text
            out_footnote = open(footnote_file, "w", encoding="utf-8")

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
                                format_footnote(curr_soup.find("p", class_="footnote").contents, out_footnote)
                            else:
                                if curr_soup.find(class_="event"):
                                    chap_cont = curr_soup.find(class_="event").contents

                                    if check_is_next_dict(curr_soup.find(class_="event").contents, main_dict):
                                        if last_soup and last_soup.find(class_="lines_float"):
                                            temp_reference = main_dict["cross-references"].pop()
                                            create_main_dict(print_main_dict(out_main))
                                            main_dict["cross-references"].append(temp_reference)
                                            main_dict["before"] = curr_section

                                        else:
                                            create_main_dict(print_main_dict(out_main))
                                            main_dict["before"] = curr_section
                                    else:
                                        main_dict["before"] = curr_section

                                    if i == -1: print(chap_cont)

                                    add_text(chap_cont)

                                elif curr_soup.find(class_="event01"):
                                    chap_cont = curr_soup.find(class_="event01").contents

                                    if check_is_next_dict(chap_cont, main_dict):
                                        create_main_dict(print_main_dict(out_main))
                                        main_dict["before"] = curr_section
                                    else:
                                        main_dict["before"] = curr_section

                                    if i == -1: print(chap_cont)
                                    add_text(chap_cont)

                                elif curr_soup.find(class_="event1"):
                                    chap_cont = curr_soup.find(class_="event1").contents

                                    if i == -1: print(chap_cont)
                                    main_dict["text"] = main_dict["text"] + ">"
                                    add_text(chap_cont)

                                elif curr_soup.find(class_="event_indent"):
                                    chap_cont = curr_soup.find(class_="event_indent").contents

                                    if i == -1: print(chap_cont)
                                    add_text(chap_cont)

                                elif curr_soup.find(class_="hanging0"):
                                    chap_cont = curr_soup.find(class_="hanging0").contents

                                    if i == -1: print(chap_cont)
                                    main_dict["text"] = main_dict["text"]+"^"
                                    add_text(chap_cont)
                                    main_dict["text"] = main_dict["text"]+"^    \n"

                                elif curr_soup.find(class_="lines_float"):
                                    main_dict["cross-references"].append(curr_soup.find(class_="lines_float").contents[0].string)

                                elif curr_soup.h1:
                                    curr_section = curr_soup.h1['id']

                                elif curr_soup.h2:
                                    curr_section = curr_soup.h2['id']

                                elif curr_soup.find(class_="eventsection"):
                                    if "id" in curr_soup.find(class_="eventsection").attrs:
                                        curr_section = curr_soup.find(class_="eventsection")['id']

                                else:
                                    print("Prevet: "+ str(i)+" - " + str(curr_soup))
                            last_soup = curr_soup

            create_main_dict(print_main_dict(out_main))
            out_main.close()
            out_footnote.close()
        i = i + 1

        global page_number
        page_number = i


def check_is_next_dict(soup, curr):

    child = soup[0]
    if child.name == "strong" and child.string is None:
        child = child.contents[1]

    if child.string and child.string == str(curr["number"] + 1):
        return True
    else:
        return False


def check_if_dict_empty():

    if main_dict["text"] == "":
        return True
    else:
        return False


def print_main_dict(out):

    out.write("{\n")
    for x, y in main_dict.items():
        if x == "cross-references":
            out.write("\t" + str(x) + ": ")
            for z in main_dict["cross-references"]:
                if z != main_dict["cross-references"][len(main_dict["cross-references"])-1]:
                    out.write(str(z) + ", ")
                else:
                    out.write(str(z))
            out.write("\n")
        elif x == "footnotes":
            out.write("\t" + str(x) + ": ")
            for z in main_dict["footnotes"]:
                if z != main_dict["footnotes"][len(main_dict["footnotes"])-1]:
                    out.write(str(z) + ", ")
                else:
                    out.write(str(z))
            out.write("\n")
        else:
            out.write("\t" + str(x) + ": " + str(y) + "\n")
    out.write("}\n")

    return main_dict["number"]+1


def create_main_dict(num):

    main_dict["number"] = num
    main_dict["text"] = ""
    main_dict["before"] = ""
    main_dict["after"] = ""
    main_dict["cross-references"] = []
    main_dict["footnotes"] = []

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
        if page_number == -1: print("\t"+str(x)+": "+str(y)+"\n")
        out.write("\t"+str(x)+": "+str(y)+"\n")
    out.write("}\n")


def add_text(chap_list):

    for item in chap_list:
        check = not check_if_invalid_text(item, chap_list)

        text = stringify(item, 0)
        if page_number == -1:
            print(str(check) + "  " + str(item))

        if check:
            if text.isdigit():
                main_dict["footnotes"].append(text)
                main_dict["text"] = main_dict["text"] + "@"
            else:
                main_dict["text"] = main_dict["text"] + text

    main_dict["text"] = main_dict["text"] + " "

    return main_dict


def check_if_invalid_text(string, list_of_str):

    if string == "\n":
        if page_number == -1: print(1)
        return True
    elif string.string:
        if string.string.isdigit() and string == list_of_str[0]:
            if page_number == -1: print(2)
            return True
    else:
        return False


def stringify(x, i):
    curr = ""

    if len(x) != 0:
        for y in x:
            curr = curr + str(y)

    if page_number == -1: print(x)

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
            main_dict["footnotes"].append(y)
            temp = temp + "@"
        return temp
    elif "class" in x.attrs and "hlink" in x.attrs["class"]:
        if "id" in x.attrs:
            temp = x.attrs["id"]

            if x.contents and x.contents[0].name == "sup":
                for y in x.contents:
                    temp = "["+stringify(y, i) + "](" + x.contents[0].contents[0] + ")"
                return temp
            else: return "{"+temp+"}"
        elif "href" in x.attrs:
            temp = x.attrs["href"][x.attrs["href"].find('#'):]
            temp = temp[1:]

            for y in x.contents:
                temp = "[" + stringify(y, i) + "](" + temp + ")"
            return temp
    elif str(x) == "<br/>":
        if i == 0:
            return "    \n"
        else:
            j = 0
            temp = ""

            while j != i:
                temp = temp + "#"
                j += 1
            return "    \n" + temp
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

