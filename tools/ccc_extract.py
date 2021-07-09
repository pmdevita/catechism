from zipfile import ZipFile
from argparse import ArgumentParser
from pprint import pprint
import json
import re
from bs4 import BeautifulSoup, NavigableString

argparse = ArgumentParser()
argparse.add_argument("epub")

INCLUDE_HEADERS = True

page_index = {}
page_order = []


# Regex to remove weird spaces
# 3rd case is for removing the colon in verse 2821
spaces_regex = re.compile("(\s{4,}|  |:\xa0\xa0\xa0)")
spaces_test = re.compile("(:\xa0\xa0\xa0)")
ellipsis = re.compile("( … )")
ellipsis_end = re.compile("( …)")
ellipsis_start = re.compile("(… )")
nbsp = re.compile("( )")


def process_text(tag, verse=False, footnotes=False):
    """

    :param tag: BS4 tag to process text from
    :param verse: Whether or not to process number at beginning, set to true if this is a known verse start
    :param footnotes: Whether or not to keep the footnotes
    :return: cleaned text from tag
    """
    # Process verse number and remove extra spaces
    if verse:
        if tag.contents[0].name == 'strong':
            if tag.contents[0].string is None:
                print("hi")
                del tag.contents[0].contents[0]  # Sometimes there is an extra tag in here besides the navigable string
            tag.contents[0].string = tag.contents[0].string + "."

    # Strip footnotes
    if not footnotes:
        for i in tag.find_all("a", class_="hlink"):
            try:
                int(i.get_text())
                i.extract()
            except ValueError:
                pass

    # Quote usually
    if len(tag.contents) == 1:
        if not isinstance(tag.contents[0], NavigableString):
            if tag.contents[0].name == "span" and 'small' in tag.contents[0].get('class', []):
                # thing = tag.contents[0].get('class')
                # print(tag.contents[0].get('class'))
                pass
    # Process small class spans J<span class="small">ESUS.</span>
    else:
        for i in tag.find_all("span", class_="small"):
            if i.string is None:
                print("hi")
                continue
            i.string = i.string.lower()

    # Process odd spaces
    text = spaces_regex.sub(" ", tag.get_text())
    # and ellipses
    text = ellipsis.sub(" … ", text)
    text = ellipsis_start.sub("… ", text)
    text = ellipsis_end.sub(" …", text)
    # All useful NSBP markers have been fixed, remove the rest
    text = nbsp.sub("", text)
    return text


def extract(file):
    with ZipFile(file, 'r') as zip:
        # pprint(zip.namelist())

        # Index pages and get order
        with zip.open('volume.opf') as f:
            b = BeautifulSoup(f, "lxml-xml")
            # print(b.package.manifest)
            for child in b.package.manifest.children:
                if isinstance(child, NavigableString):
                    continue
                # print(child, child.attrs)
                page_index[child['id']] = child['href']
            for child in b.package.spine.children:
                if isinstance(child, NavigableString):
                    continue
                page_order.append(child['idref'])
            print(page_index)
            print(page_order)

        # start = False   # Have we skipped the beginning stuff yet?
        # search_string = "For this reason, at every time and in every place, God draws close to man."
        verses = []     # Full collection of verses
        new_verse = ""  # Variable to assemble verses with
        start_page_index = page_order.index("prl")  # Start at the prologue

        for page in page_order[start_page_index:]:
            with zip.open(page_index[page], 'r') as f:
                soup = BeautifulSoup(f, 'lxml')

                # Process the pre-body tags in a page
                for child in soup.body.children:
                    # print(child)
                    if isinstance(child, NavigableString):
                        continue

                    # print(child.name, child.get('class', None))

                    # Large (biggest) header
                    if child.name == 'h1' and 'chapter' in child.get('class', []) and INCLUDE_HEADERS:
                        new_verse += "# {}\n".format(child.get_text())
                    elif child.name == 'h2' and 'section' in child.get('class', []) and INCLUDE_HEADERS:
                        new_verse += "## {}\n".format(child.get_text())
                    elif child.name == 'div' and 'outline' in child.get('class', []):
                        new_verse = parse_outline_section(child, verses, new_verse)

        # pprint(verses)
        # for i in verses:
        #     print(i)
        # verses = []
        return verses

def parse_outline_section(outline, verses, new_verse):
    # Process the main content section in the page

    # Flag used to indicate the previous tag was a cross reference and that this a continuation of the last verse
    last_type = []

    for child in outline:
        # print(child)
        if isinstance(child, NavigableString):
            continue

        print(child.name, child.get('class', None))

        # The following are parse rules for the different tags that occur in the text

        # Large (biggest) header
        if child.name == 'h1' and 'chapter' in child.get('class', []) and INCLUDE_HEADERS:
            new_verse += "# {}\n".format(child.get_text())
            last_type.append("header")
        # IN BRIEF header
        elif child.name == 'h2' and 'section' in child.get('class', []) and INCLUDE_HEADERS:
            new_verse += "### {}\n".format(child.get_text())
            last_type.append("header")
        # Text without verse
        elif child.name == 'div' and 'event1' in child.get('class', []):
            # if length is only one,
            is_quote = False
            if len(child.contents) == 1:
                # Quote
                if child.contents[0].name == 'span' and 'small' in child.contents[0].get('class', []):
                    is_quote = True
                    new = child.span
                    template = ">{}\n"
                    # If the last addition was also a quote, separate it by character turn
                    if len(last_type) > 0:
                        if last_type[len(last_type) - 1] == "quote":
                            template = ">\n>{}\n"
                        # If it was a quote broken by cross reference, append it
                        elif len(last_type) > 1:
                            if last_type[len(last_type) - 1] == "cross reference" \
                                    and last_type[len(last_type) - 2] == "quote":
                                template = ">{}\n"
                    append = True
                    # One quote appeared after a header, go figure
                    if last_type:
                        append = last_type[len(last_type) - 1] != "header"
                    last_type.append("quote")
            # New text paragraph
            if not is_quote:
                template = "{}\n"
                append = False
                # Double check for quote broken by cross reference
                if len(last_type) > 1:
                    if last_type[len(last_type) - 1] == "cross reference" \
                            and last_type[len(last_type) - 2] == "quote":
                        template = ">{}\n"
                        append = True
                        last_type.append("quote")
                    else:
                        last_type.append("text")
                else:
                    last_type.append("text")

            # print(child)
            text = process_text(child)
            print(text)
            if append:
                verses[len(verses) - 1] += template.format(text)
            else:
                new_verse += template.format(text)
        # Subsection header
        elif child.name == 'div' and 'eventsection' in child.get('class', []) and INCLUDE_HEADERS:
            new_verse += "#### {}\n".format(process_text(child))
            last_type.append("header")
        # Sub-subsection header
        elif child.name == 'div' and 'eventsection0' in child.get('class', []) and INCLUDE_HEADERS:
            new_verse += "##### {}\n".format(process_text(child))
            last_type.append("header")
        # Verse
        elif child.name == 'div' and 'event' in child.get('class', []):
            # If this verse lacks a number and follows a cross-reference, we'll append it
            append = child.contents[0].name != 'strong' and last_type[len(last_type) - 1] == "cross reference"
            new = process_text(child, verse=True, footnotes=False)
            if append:
                verses[len(verses) - 1] += " {}\n".format(new)
            else:
                # A single sentence that is strong might be a header
                if child.contents[0].name == 'strong' and len(child.contents) == 1:
                    new_verse += "#### {}\n".format(new)
                else:
                    new_verse += "{}\n".format(new)
                    last_type.append("verse")
                verses.append(new_verse)
                new_verse = ""
        # IN BRIEF verses
        elif child.name == 'div' and 'event01' in child.get('class', []):
            # If this verse lacks a number and follows a cross-reference, we'll append it
            append = child.contents[0].name != 'strong' and last_type[len(last_type) - 1] == "cross reference"
            new = process_text(child, verse=True, footnotes=False)
            if append:
                verses[len(verses) - 1] += " {}\n".format(new)
            else:
                new_verse += "{}\n".format(new)
                verses.append(new_verse)
                new_verse = ""
            last_type.append("verse")
        # Cross-reference
        elif child.name == 'div' and 'lines_float' in child.get('class', []):
            last_type.append("cross reference")
        # Paragraph headers
        elif child.name == 'div' and 'event_big' in child.get('class', []):
            new_verse += "### {}\n".format(process_text(child))
            last_type.append("header")

        if len(last_type) > 5:
            last_type.pop(0)

    return new_verse


def export(verses, json_mode=True):
    if json_mode:
        with open("catechism.json", "w") as f:
            json.dump(verses, f)
    else:
        with open("catechism.md", "w") as f:
            f.write("\n".join(verses))


if __name__ == '__main__':
    args = argparse.parse_args()
    verses = extract(args.epub)
    export(verses)



