const markdownTest = "# Markdown: Syntax\n" +
    "\n" +
    "*   [Overview](#overview)\n" +
    "    *   [Philosophy](#philosophy)\n" +
    "    *   [Inline HTML](#html)\n" +
    "    *   [Automatic Escaping for Special Characters](#autoescape)\n" +
    "*   [Block Elements](#block)\n" +
    "    *   [Paragraphs and Line Breaks](#p)\n" +
    "    *   [Headers](#header)\n" +
    "    *   [Blockquotes](#blockquote)\n" +
    "    *   [Lists](#list)\n" +
    "    *   [Code Blocks](#precode)\n" +
    "    *   [Horizontal Rules](#hr)\n" +
    "*   [Span Elements](#span)\n" +
    "    *   [Links](#link)\n" +
    "    *   [Emphasis](#em)\n" +
    "    *   [Code](#code)\n" +
    "    *   [Images](#img)\n" +
    "*   [Miscellaneous](#misc)\n" +
    "    *   [Backslash Escapes](#backslash)\n" +
    "    *   [Automatic Links](#autolink)\n" +
    "\n" +
    "\n" +
    "**Note:** This document is itself written using Markdown; you\n" +
    "can [see the source for it by adding '.text' to the URL](/projects/markdown/syntax.text).\n" +
    "\n" +
    "----\n" +
    "\n" +
    "## Overview\n" +
    "\n" +
    "### Philosophy\n" +
    "\n" +
    "Markdown is intended to be as easy-to-read and easy-to-write as is feasible.\n" +
    "\n" +
    "Readability, however, is emphasized above all else. A Markdown-formatted\n" +
    "document should be publishable as-is, as plain text, without looking\n" +
    "like it's been marked up with tags or formatting instructions. While\n" +
    "Markdown's syntax has been influenced by several existing text-to-HTML\n" +
    "filters -- including [Setext](http://docutils.sourceforge.net/mirror/setext.html), [atx](http://www.aaronsw.com/2002/atx/), [Textile](http://textism.com/tools/textile/), [reStructuredText](http://docutils.sourceforge.net/rst.html),\n" +
    "[Grutatext](http://www.triptico.com/software/grutatxt.html), and [EtText](http://ettext.taint.org/doc/) -- the single biggest source of\n" +
    "inspiration for Markdown's syntax is the format of plain text email.\n" +
    "\n" +
    "## Block Elements\n" +
    "\n" +
    "### Paragraphs and Line Breaks\n" +
    "\n" +
    "A paragraph is simply one or more consecutive lines of text, separated\n" +
    "by one or more blank lines. (A blank line is any line that looks like a\n" +
    "blank line -- a line containing nothing but spaces or tabs is considered\n" +
    "blank.) Normal paragraphs should not be indented with spaces or tabs.\n" +
    "\n" +
    "The implication of the \"one or more consecutive lines of text\" rule is\n" +
    "that Markdown supports \"hard-wrapped\" text paragraphs. This differs\n" +
    "significantly from most other text-to-HTML formatters (including Movable\n" +
    "Type's \"Convert Line Breaks\" option) which translate every line break\n" +
    "character in a paragraph into a `<br />` tag.\n" +
    "\n" +
    "When you *do* want to insert a `<br />` break tag using Markdown, you\n" +
    "end a line with two or more spaces, then type return.\n" +
    "\n" +
    "### Headers\n" +
    "\n" +
    "Markdown supports two styles of headers, [Setext] [1] and [atx] [2].\n" +
    "\n" +
    "Optionally, you may \"close\" atx-style headers. This is purely\n" +
    "cosmetic -- you can use this if you think it looks better. The\n" +
    "closing hashes don't even need to match the number of hashes\n" +
    "used to open the header. (The number of opening hashes\n" +
    "determines the header level.)\n" +
    "\n" +
    "\n" +
    "### Blockquotes\n" +
    "\n" +
    "Markdown uses email-style `>` characters for blockquoting. If you're\n" +
    "familiar with quoting passages of text in an email message, then you\n" +
    "know how to create a blockquote in Markdown. It looks best if you hard\n" +
    "wrap the text and put a `>` before every line:\n" +
    "\n" +
    "> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,\n" +
    "> consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.\n" +
    "> Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.\n" +
    "> \n" +
    "> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse\n" +
    "> id sem consectetuer libero luctus adipiscing.\n" +
    "\n" +
    "Markdown allows you to be lazy and only put the `>` before the first\n" +
    "line of a hard-wrapped paragraph:\n" +
    "\n" +
    "> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,\n" +
    "consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.\n" +
    "Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.\n" +
    "\n" +
    "> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse\n" +
    "id sem consectetuer libero luctus adipiscing.\n" +
    "\n" +
    "Blockquotes can be nested (i.e. a blockquote-in-a-blockquote) by\n" +
    "adding additional levels of `>`:\n" +
    "\n" +
    "> This is the first level of quoting.\n" +
    ">\n" +
    "> > This is nested blockquote.\n" +
    ">\n" +
    "> Back to the first level.\n" +
    "\n" +
    "Blockquotes can contain other Markdown elements, including headers, lists,\n" +
    "and code blocks:\n" +
    "\n" +
    "> ## This is a header.\n" +
    "> \n" +
    "> 1.   This is the first list item.\n" +
    "> 2.   This is the second list item.\n" +
    "> \n" +
    "> Here's some example code:\n" +
    "> \n" +
    ">     return shell_exec(\"echo $input | $markdown_script\");\n" +
    "\n" +
    "Any decent text editor should make email-style quoting easy. For\n" +
    "example, with BBEdit, you can make a selection and choose Increase\n" +
    "Quote Level from the Text menu.\n" +
    "\n" +
    "\n" +
    "### Lists\n" +
    "\n" +
    "Markdown supports ordered (numbered) and unordered (bulleted) lists.\n" +
    "\n" +
    "Unordered lists use asterisks, pluses, and hyphens -- interchangably\n" +
    "-- as list markers:\n" +
    "\n" +
    "*   Red\n" +
    "*   Green\n" +
    "*   Blue\n" +
    "\n" +
    "is equivalent to:\n" +
    "\n" +
    "+   Red\n" +
    "+   Green\n" +
    "+   Blue\n" +
    "\n" +
    "and:\n" +
    "\n" +
    "-   Red\n" +
    "-   Green\n" +
    "-   Blue\n" +
    "\n" +
    "Ordered lists use numbers followed by periods:\n" +
    "\n" +
    "1.  Bird\n" +
    "2.  McHale\n" +
    "3.  Parish\n" +
    "\n" +
    "It's important to note that the actual numbers you use to mark the\n" +
    "list have no effect on the HTML output Markdown produces. The HTML\n" +
    "Markdown produces from the above list is:\n" +
    "\n" +
    "If you instead wrote the list in Markdown like this:\n" +
    "\n" +
    "1.  Bird\n" +
    "1.  McHale\n" +
    "1.  Parish\n" +
    "\n" +
    "or even:\n" +
    "\n" +
    "3. Bird\n" +
    "1. McHale\n" +
    "8. Parish\n" +
    "\n" +
    "you'd get the exact same HTML output. The point is, if you want to,\n" +
    "you can use ordinal numbers in your ordered Markdown lists, so that\n" +
    "the numbers in your source match the numbers in your published HTML.\n" +
    "But if you want to be lazy, you don't have to.\n" +
    "\n" +
    "To make lists look nice, you can wrap items with hanging indents:\n" +
    "\n" +
    "*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\n" +
    "    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,\n" +
    "    viverra nec, fringilla in, laoreet vitae, risus.\n" +
    "*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.\n" +
    "    Suspendisse id sem consectetuer libero luctus adipiscing.\n" +
    "\n" +
    "But if you want to be lazy, you don't have to:\n" +
    "\n" +
    "*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\n" +
    "Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,\n" +
    "viverra nec, fringilla in, laoreet vitae, risus.\n" +
    "*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.\n" +
    "Suspendisse id sem consectetuer libero luctus adipiscing.\n" +
    "\n" +
    "List items may consist of multiple paragraphs. Each subsequent\n" +
    "paragraph in a list item must be indented by either 4 spaces\n" +
    "or one tab:\n" +
    "\n" +
    "1.  This is a list item with two paragraphs. Lorem ipsum dolor\n" +
    "    sit amet, consectetuer adipiscing elit. Aliquam hendrerit\n" +
    "    mi posuere lectus.\n" +
    "\n" +
    "    Vestibulum enim wisi, viverra nec, fringilla in, laoreet\n" +
    "    vitae, risus. Donec sit amet nisl. Aliquam semper ipsum\n" +
    "    sit amet velit.\n" +
    "\n" +
    "2.  Suspendisse id sem consectetuer libero luctus adipiscing.\n" +
    "\n" +
    "It looks nice if you indent every line of the subsequent\n" +
    "paragraphs, but here again, Markdown will allow you to be\n" +
    "lazy:\n" +
    "\n" +
    "*   This is a list item with two paragraphs.\n" +
    "\n" +
    "    This is the second paragraph in the list item. You're\n" +
    "only required to indent the first line. Lorem ipsum dolor\n" +
    "sit amet, consectetuer adipiscing elit.\n" +
    "\n" +
    "*   Another item in the same list.\n" +
    "\n" +
    "To put a blockquote within a list item, the blockquote's `>`\n" +
    "delimiters need to be indented:\n" +
    "\n" +
    "*   A list item with a blockquote:\n" +
    "\n" +
    "    > This is a blockquote\n" +
    "    > inside a list item.\n" +
    "\n" +
    "To put a code block within a list item, the code block needs\n" +
    "to be indented *twice* -- 8 spaces or two tabs:\n" +
    "\n" +
    "*   A list item with a code block:\n" +
    "\n" +
    "        <code goes here>\n" +
    "\n" +
    "### Code Blocks\n" +
    "\n" +
    "Pre-formatted code blocks are used for writing about programming or\n" +
    "markup source code. Rather than forming normal paragraphs, the lines\n" +
    "of a code block are interpreted literally. Markdown wraps a code block\n" +
    "in both `<pre>` and `<code>` tags.\n" +
    "\n" +
    "To produce a code block in Markdown, simply indent every line of the\n" +
    "block by at least 4 spaces or 1 tab.\n" +
    "\n" +
    "This is a normal paragraph:\n" +
    "\n" +
    "    This is a code block.\n" +
    "\n" +
    "Here is an example of AppleScript:\n" +
    "\n" +
    "    tell application \"Foo\"\n" +
    "        beep\n" +
    "    end tell\n" +
    "\n" +
    "A code block continues until it reaches a line that is not indented\n" +
    "(or the end of the article).\n" +
    "\n" +
    "Within a code block, ampersands (`&`) and angle brackets (`<` and `>`)\n" +
    "are automatically converted into HTML entities. This makes it very\n" +
    "easy to include example HTML source code using Markdown -- just paste\n" +
    "it and indent it, and Markdown will handle the hassle of encoding the\n" +
    "ampersands and angle brackets. For example, this:\n" +
    "\n" +
    "    <div class=\"footer\">\n" +
    "        &copy; 2004 Foo Corporation\n" +
    "    </div>\n" +
    "\n" +
    "Regular Markdown syntax is not processed within code blocks. E.g.,\n" +
    "asterisks are just literal asterisks within a code block. This means\n" +
    "it's also easy to use Markdown to write about Markdown's own syntax.\n" +
    "\n" +
    "```\n" +
    "tell application \"Foo\"\n" +
    "    beep\n" +
    "end tell\n" +
    "```\n" +
    "\n" +
    "## Span Elements\n" +
    "\n" +
    "### Links\n" +
    "\n" +
    "Markdown supports two style of links: *inline* and *reference*.\n" +
    "\n" +
    "In both styles, the link text is delimited by [square brackets].\n" +
    "\n" +
    "To create an inline link, use a set of regular parentheses immediately\n" +
    "after the link text's closing square bracket. Inside the parentheses,\n" +
    "put the URL where you want the link to point, along with an *optional*\n" +
    "title for the link, surrounded in quotes. For example:\n" +
    "\n" +
    "This is [an example](http://example.com/) inline link.\n" +
    "\n" +
    "[This link](http://example.net/) has no title attribute.\n" +
    "\n" +
    "### Emphasis\n" +
    "\n" +
    "Markdown treats asterisks (`*`) and underscores (`_`) as indicators of\n" +
    "emphasis. Text wrapped with one `*` or `_` will be wrapped with an\n" +
    "HTML `<em>` tag; double `*`'s or `_`'s will be wrapped with an HTML\n" +
    "`<strong>` tag. E.g., this input:\n" +
    "\n" +
    "*single asterisks*\n" +
    "\n" +
    "_single underscores_\n" +
    "\n" +
    "**double asterisks**\n" +
    "\n" +
    "__double underscores__\n" +
    "\n" +
    "### Code\n" +
    "\n" +
    "To indicate a span of code, wrap it with backtick quotes (`` ` ``).\n" +
    "Unlike a pre-formatted code block, a code span indicates code within a\n" +
    "normal paragraph. For example:\n" +
    "\n" +
    "Use the `printf()` function.\n";

export default markdownTest;