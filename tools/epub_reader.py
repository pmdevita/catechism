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
    "title": "",
    "page": "",
    "sections": [],
    "tabs": 1,
    "name": ""
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
        global page_number
        if 5 <= i <= 35:

            #Converts the file name into output file location
            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')
            main_text = main_text.replace("Chur_9780307953704_epub_", '')
            main_text = main_text.replace("_r1", '')

            footnote_text = x
            footnote_text = footnote_text.replace("OEBPS", 'Footnotes')
            footnote_text = footnote_text.replace(".htm", '.json')
            footnote_text = footnote_text.replace("Chur_9780307953704_epub_", '')
            footnote_text = footnote_text.replace("_r1", '')

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

                    if y == "</tr>\n": main_dict["text"] = main_dict["text"] + "|    "
                    
                    #Check if current line is part of the body of the page
                    if curr_soup.body:

                        chap_cont = list(curr_soup.strings)

                        if len(chap_cont) >= 0 and chap_cont[0] != "\n":
                            if 5 <= i <= 38 and curr_soup.find("p", class_="footnote"):
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

                                    add_text(chap_cont)

                                elif curr_soup.find(class_="event01"):
                                    chap_cont = curr_soup.find(class_="event01").contents

                                    if check_is_next_dict(chap_cont, main_dict):
                                        create_main_dict(print_main_dict(out_main))
                                        main_dict["before"] = curr_section
                                    else:
                                        main_dict["before"] = curr_section

                                    add_text(chap_cont)

                                elif curr_soup.find(class_="event1"):
                                    chap_cont = curr_soup.find(class_="event1").contents

                                    main_dict["text"] = main_dict["text"] + ">"
                                    add_text(chap_cont)

                                elif curr_soup.find(class_="event_indent"):
                                    chap_cont = curr_soup.find(class_="event_indent").contents

                                    add_text(chap_cont)

                                elif curr_soup.find(class_="hanging0"):
                                    chap_cont = curr_soup.find(class_="hanging0").contents

                                    main_dict["text"] = main_dict["text"]+"^"
                                    add_text(chap_cont)
                                    main_dict["text"] = main_dict["text"]+"^    "

                                elif curr_soup.find(class_="section_article1"):
                                    chap_cont = curr_soup.find(class_="section_article1").contents

                                    main_dict["text"] = main_dict["text"] + "|-|"
                                    add_text(chap_cont)
                                    main_dict["text"] = main_dict["text"] + "|-| "

                                elif curr_soup.td:
                                    chap_cont = curr_soup.td.contents

                                    main_dict["text"] = main_dict["text"] + "| "
                                    add_text(chap_cont)
                                    main_dict["text"] = main_dict["text"] + " "

                                elif curr_soup.find(class_="lines_float"):
                                    main_dict["cross-references"].append(curr_soup.find(class_="lines_float").contents[0].string)

                                elif curr_soup.h1:
                                    curr_section = curr_soup.h1['id']

                                elif curr_soup.h2:
                                    curr_section = curr_soup.h2['id']

                                elif curr_soup.find(class_="eventsection"):
                                    if "id" in curr_soup.find(class_="eventsection").attrs:
                                        curr_section = curr_soup.find(class_="eventsection")['id']

                            last_soup = curr_soup

            create_main_dict(print_main_dict(out_main))
            out_main.close()
            out_footnote.close()
        elif i == 3:

            out_toc = open("OutDocs/toc.json", "w", encoding="utf-8")

            out_toc.write("[\n")
            read_toc(x, out_toc)
            out_toc.write("]")

            out_toc.close()
        elif 36 <= i <= 38:

            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')
            main_text = main_text.replace("Chur_9780307953704_epub_", '')
            main_text = main_text.replace("_r1", '')

            main_file = main_text
            out_main = open(main_file, "w", encoding="utf-8")

            with open("CatEpub/" + x, encoding="utf8") as f:
                file = f.readlines()

                out_main.write('{\n')

                for y in file:
                    curr_soup = BeautifulSoup(y, "lxml")

                    if curr_soup.body:

                        chap_cont = list(curr_soup.strings)

                        if len(chap_cont) >= 0 and chap_cont[0] != "\n":
                            if curr_soup.h1:
                                out_main.write('\ttext: "#'+stringify(curr_soup.h1, 1)+'"\n')
                            elif curr_soup.find(class_="nonindent"):
                                out_main.write('\ttext: "##'+stringify(curr_soup.find(class_="nonindent"), 1)+'"\n')
                            elif curr_soup.find(class_="nonindent2"):
                                out_main.write('\ttext: "' + stringify(curr_soup.find(class_="nonindent2"), 1) + '"\n')
                            elif curr_soup.find(class_="primary"):
                                out_main.write('\ttext: "   ' + stringify(curr_soup.find(class_="primary"), 1) + '"\n')
                            elif curr_soup.find(class_="secondary"):
                                out_main.write('\ttext: "      ' + stringify(curr_soup.find(class_="secondary"), 1) + '"\n')
                            elif curr_soup.find(class_="tertiary"):
                                out_main.write('\ttext: "         ' + stringify(curr_soup.find(class_="tertiary"), 1) + '"\n')
                            else:
                                for z in chap_cont:
                                    out_main.write("\t"+z)
                                print(curr_soup.contents[0].contents[0].contents[0])

            out_main.write("}")
            out_main.close()
        elif 39 == i:

            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')
            main_text = main_text.replace("Chur_9780307953704_epub_", '')
            main_text = main_text.replace("_r1", '')

            main_file = main_text
            out_main = open(main_file, "w", encoding="utf-8")

            with open("CatEpub/" + x, encoding="utf8") as f:
                file = f.readlines()

                out_main.write('{\n')

                for y in file:
                    curr_soup = BeautifulSoup(y, "lxml")

                    if y == "</tr>\n": out_main.write("|    ")

                    if curr_soup.body:

                        chap_cont = list(curr_soup.strings)

                        if len(chap_cont) >= 0 and chap_cont[0] != "\n":
                            if curr_soup.h1:
                                out_main.write('\ttext: "#'+stringify(curr_soup.h1, 0)+'"\n')
                            elif curr_soup.find(class_="nonindent2"):
                                out_main.write('\ttext: "' + stringify(curr_soup.find(class_="nonindent2"), 0) + '"\n')
                                out_main.write('\ttext: "')
                            elif curr_soup.td:
                                out_main.write('   ' + stringify(curr_soup.td, 0))
                                if chap_cont[0] == "Revelation":
                                    out_main.write('"\n')
                                elif "</tr>" in y:
                                    out_main.write('"\n\ttext: "')

            out_main.write("}")
            out_main.close()
        elif 4 == i:
            main_text = x
            main_text = main_text.replace("OEBPS", 'OutDocs')
            main_text = main_text.replace(".htm", '.json')
            main_text = main_text.replace("Chur_9780307953704_epub_", '')
            main_text = main_text.replace("_r1", '')

            footnote_text = x
            footnote_text = footnote_text.replace("OEBPS", 'Footnotes')
            footnote_text = footnote_text.replace(".htm", '.json')
            footnote_text = footnote_text.replace("Chur_9780307953704_epub_", '')
            footnote_text = footnote_text.replace("_r1", '')

            main_file = main_text
            out_main = open(main_file, "w", encoding="utf-8")

            footnote_file = footnote_text
            out_footnote = open(footnote_file, "w", encoding="utf-8")

            with open("CatEpub/" + x, encoding="utf8") as f:
                file = f.readlines()

                out_main.write('{\n')

                intro_dict = main_dict.copy()
                intro_dict["number"] = 0
                print(intro_dict)

                for y in file:
                    curr_soup = BeautifulSoup(y, "lxml")

                    if curr_soup.body:
                        chap_cont = list(curr_soup.strings)

                        if len(chap_cont) >= 0 and chap_cont[0] != "\n":
                            if curr_soup.h1:
                                out_main.write('\ttext: "#'+stringify(curr_soup.h1, 0)+'"\n')
                            elif curr_soup.find(class_="nonindent0"):
                                out_main.write(
                                    '\ttext: "##' + stringify(curr_soup.find(class_="nonindent0"), 0) + '"\n')
                            elif curr_soup.find(class_="center0"):
                                out_main.write(
                                    '\ttext: "<center>' + stringify(curr_soup.find(class_="center0"), 0) + '</center>"\n')
                            elif curr_soup.find(class_="indent0"):
                                out_main.write(
                                    '\ttext: "   ' + stringify(curr_soup.find(class_="indent0"), 0) + '"\n')
                            elif curr_soup.find(class_="section0"):
                                out_main.write(
                                    '\ttext: "###' + stringify(curr_soup.find(class_="section0"), 0) + '"\n')
                            elif curr_soup.find(class_="footnote"):
                                format_footnote(curr_soup.find("p", class_="footnote").contents, out_footnote)
                            else:
                                for z in chap_cont:
                                    out_main.write("\t" + z)
                                print(curr_soup.contents[0].contents[0].contents[0])

            out_main.write("}")
            out_main.close()

        i = i + 1

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


def read_toc(infile, outfile):

    tab_order = {"PROLOGUE": 0, "PART": 0, "SECTION": 1, "CHAPTER": 2, "ARTICLE": 3, "Paragraph": 4, "other": 5}
    dict_list = []

    with open("CatEpub/" + infile, encoding="utf8") as f:
        file = f.readlines()

        for y in file:
            curr_soup = BeautifulSoup(y, "lxml")

            if curr_soup.body:

                chap_cont = list(curr_soup.strings)

                if len(chap_cont) >= 0 and chap_cont[0] != "\n":
                    if curr_soup.find(class_="toc_chap") or curr_soup.find(class_="toc_sec1") or \
                            curr_soup.find(class_="toc_hang") or curr_soup.find(class_="toc_sec4") or \
                            curr_soup.find(class_="toc_part1"):
                        string_title = ""
                        temp_title = ""

                        for j in curr_soup.a.contents:
                            string_title = string_title + j.string

                        for j in curr_soup.a.contents:
                            temp_title = temp_title + stringify(j, 0)

                        temp_page = curr_soup.a.attrs["href"]
                        temp_page = temp_page.replace("Chur_9780307953704_epub_", '')
                        temp_page = temp_page.replace("_r1.htm", '')

                        if string_title == "PROLOGUE":

                            toc_dict["page"] = str(temp_page)

                            toc_dict["title"] = stringify(curr_soup.a.contents[0], 0)

                            toc_dict["name"] = string_title
                            dict_list.append(toc_dict)
                        elif string_title.find("PART") == 0:
                            clear_toc(outfile)
                            dict_list = []

                            toc_dict["page"] = str(temp_page)

                            toc_dict["title"] = stringify(curr_soup.a.contents[0], 0)

                            toc_dict["name"] = "PART"
                            dict_list.append(toc_dict)
                        else:

                            if string_title.find("SECTION") == 0:
                                curr_name = "SECTION"
                            elif string_title.find("CHAPTER") == 0:
                                curr_name = "CHAPTER"
                            elif string_title.find("ARTICLE") == 0:
                                curr_name = "ARTICLE"
                            elif string_title.find("Paragraph") == 0:
                                curr_name = "Paragraph"
                            else:
                                curr_name = "other"

                            if tab_order.get(curr_name) > tab_order.get(dict_list[-1]["name"]):
                                curr_toc = create_toc_dict(dict_list[-1]["tabs"] + 1)
                                dict_list[-1]["sections"].append(curr_toc)
                                dict_list.append(curr_toc)
                            elif tab_order.get(curr_name) < tab_order.get(dict_list[-1]["name"]):
                                while tab_order.get(curr_name) <= tab_order.get(dict_list[-1]["name"]):
                                    dict_list.pop()

                                curr_toc = create_toc_dict(dict_list[-1]["tabs"] + 1)
                                dict_list[-1]["sections"].append(curr_toc)
                                dict_list.append(curr_toc)
                            else:
                                curr_toc = create_toc_dict(dict_list[-1]["tabs"])
                                if len(dict_list) >= 2: dict_list[-2]["sections"].append(curr_toc)
                                else: toc_dict["sections"].append(curr_toc)

                            temp_page = temp_page[temp_page.find('#'):]
                            temp_page = temp_page.replace("#", '')

                            curr_toc["page"] = str(temp_page)

                            curr_toc["title"] = temp_title

                            curr_toc["name"] = curr_name

    clear_toc(outfile)


def clear_toc(out):

    print_toc(toc_dict, out)

    toc_dict["title"] = ""
    toc_dict["page"] = ""
    if toc_dict["sections"]:
        toc_dict["sections"].clear()
    toc_dict["tabs"]: 1

    return toc_dict


def print_toc(old_dict, out):

    for x in range(old_dict["tabs"]):
        out.write("\t")
    out.write('{"title": "' + old_dict["title"]+'"')
    out.write(', "page": "' + old_dict["page"]+'"')
    out.write(', "sections": [')
    if old_dict["sections"]:
        out.write("\n")
        for x in old_dict["sections"]:
            print_toc(x, out)
        if old_dict["tabs"] >= 1:
            for x in range(old_dict["tabs"]):
                out.write("\t")
        out.write("    ]},\n")
    else:
        if old_dict["tabs"] <= 1:
            for x in range(old_dict["tabs"]+1):
                out.write("\t")
        out.write("]},\n")


def create_toc_dict(tabs):

    temp_dict = {
        "title": "",
        "page": "",
        "sections": [],
        "tabs": tabs,
        "name": ""
    }

    return temp_dict


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
    elif str(x) == '<span class="underline">' + curr + '</span>':
        temp = "++"

        for y in x.contents:
            temp = temp + stringify(y, i)
        return temp + "++"
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
            elif i == 1:
                for y in x.contents:
                    temp = "[" + stringify(y, i) + "](" + temp + ")"
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
            return "    "
        else:
            j = 0
            temp = ""

            while j != i:
                temp = temp + "#"
                j += 1
            return "    " + temp
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

