import { Component, Fragment } from "preact";
import markdownTest from "../test/markdownTest";

const MarkdownRegEx = {
    header: new RegExp("^#+ "),
    list: new RegExp("^([\*|\\-|\+]) "),
    orderedList: new RegExp("^(\\d+)\. "),
    indent: new RegExp("^( +)\\S"),
    horizRule: new RegExp("^\\s*(-{3,})\\s*$"),
    quote: new RegExp("^(\\s*>).*$"),
    link: new RegExp("\\[(.*?)\\] *\\n? *\\(\\s*(.*?)\\s*\\)", "g"),
    emphasis: new RegExp("(\\*|_)(.*?)(\\*|_)", "g"),
    strongEmphasis: new RegExp("(\\*\\*|__)(.*?)(\\*\\*|__)", "g")
};

const MarkdownConsts = {
    HEADER: "HEADER",
    LIST: "LIST",
    PARAGRAPH: "PARAGRAPH",
    CODE: "CODE",
    ORDERED_LIST: "ORDERED_LIST",
    BREAK: "BREAK",
    HORIZONTAL_RULE: "HORIZONTAL_RULE",
    QUOTE: "QUOTE"
};

const LEVEL_TYPES = new Set([MarkdownConsts.LIST, MarkdownConsts.ORDERED_LIST, MarkdownConsts.QUOTE]);

function Header(props) {
    return h("h" + props.level.toString(), null, <Text>{props.children}</Text>);
}

function Link(props) {
    // Nesting Text is correct probably not great for performance
    return <a href={props.address}><Text>{props.children}</Text></a>;
}

function Emphasis(props) {
    return h(this.props.strong ? "strong" : "em", {}, <Text>{props.children}</Text>);
}

function replaceTextMarkup(list, regex, func) {
    // Go backwards to avoid index offset problems
    for (let i=list.length - 1;i>=0;i--) {
        if (typeof list[i] != 'string') {
            continue;
        }
        let replacements = [];
        for (const match of list[i].matchAll(regex)) {
            let replacement = func(match);
            replacements.push({"replacement": replacement, start: match.index, end: match.index + match[0].length});
        }
        for (const replacement of replacements.reverse()) {
            list.splice(i, 1, list[i].substr(0, replacement.start), replacement.replacement, list[i].substr(replacement.end));
        }
    }
    return list;
}

function Text(props) {
    let text = [props.children.trim()];
    text = replaceTextMarkup(text, MarkdownRegEx.link, (match) => {
        return <Link address={match[2]}>{match[1]}</Link>;
    })
    text = replaceTextMarkup(text, MarkdownRegEx.strongEmphasis, (match) => {
        return <Emphasis strong={true}>{match[2]}</Emphasis>;
    })
    text = replaceTextMarkup(text, MarkdownRegEx.emphasis, (match) => {
        console.log("hi", match);
        return <Emphasis>{match[2]}</Emphasis>;
    })
    return <>{text}</>
}

function List(props) {
    return h((props.ordered ? "ol" : "ul"), {}, props.list.map((data) => {
        if (typeof data === 'object') {
            return <List ordered={data.ordered} list={data.list}/>;
        } else {
            return <li><Text>{data}</Text></li>;
        }
    }))
}

function Paragraph(props) {
    return <p><Text>{props.list.join(" ")}</Text></p>;
}

function Quote(props) {
    return <blockquote><p>{props.list.join(" ")}</p></blockquote>;
}

function Code(props) {
    return <code>{props.list.join("\n")}</code>;
}

function Break(props) {
    return <br/>;
}

function HorizontalRule(props) {
    return <hr/>
}


class GroupManager {
    constructor() {
        this.groupStack = [];
        this.staged = null;
    }

    add(type, value, data) {
        this.staged = {"type": type, "value": value, "data": data}
    }

    doAdd() {
        if (this.staged === null) {
            return;
        }
        // If type matches, check if we can add it on to the last type's stack
        if (this.groupStack.length > 0) {
            if (this.groupStack[this.groupStack.length - 1].type === this.staged.type) {
                if (LEVEL_TYPES.has(this.staged.type)) {
                    if (this.groupStack[this.groupStack.length - 1].level === this.staged.data.level) {
                        this.groupStack[this.groupStack.length - 1].list.push(this.staged.value);
                        this.staged = null;
                        return;
                    }
                } else {
                    this.groupStack[this.groupStack.length - 1].list.push(this.staged.value);
                    this.staged = null;
                    return;
                }
            }
        }
        this.groupStack.push({"type": this.staged.type, "list": [this.staged.value], ...this.staged.data});
        this.staged = null;
    }

    isNotLastType(type) {
        if (this.groupStack.length > 0) {
            return this.groupStack[this.groupStack.length - 1].type !== type;
        }
        return false;
    }

    lastType() {
        if (this.groupStack.length > 0) {
            return this.groupStack[this.groupStack.length - 1].type;
        }
        return null;
    }

    pop() {
        return this.groupStack.pop()
    }

    length() {
        return this.groupStack.length;
    }

}

class Markdown extends Component {
    componentDidMount() {
        this.processMarkdown()
    }

    processGroup(final, group) {
        // Process merging
        // Pre-processing for lists. Flatten hierarchy into a single list component
        for (let i = group.length() - 1; i >= 1; i--) {
            switch (group.groupStack[i].type) {
                case MarkdownConsts.LIST:
                case MarkdownConsts.ORDERED_LIST: // List merging
                    let finishedGroup = group.groupStack[i];
                    for (let j = i - 1; j >= 0; j--) {
                        if (!(group.groupStack[j].type === MarkdownConsts.LIST || group.groupStack[j].type === MarkdownConsts.ORDERED_LIST)) {
                            break;
                        }
                        if (group.groupStack[j].level < finishedGroup.level) {
                            group.groupStack[j].list.push({
                                "ordered": finishedGroup.type === MarkdownConsts.ORDERED_LIST,
                                "list": finishedGroup.list
                            });
                            group.groupStack.splice(i, 1);
                            break;
                        }
                    }
            }
        }
        // Now merge neighboring list components
        for (let i = group.length() - 1; i >= 1; i--) {
            switch (group.groupStack[i].type) {
                case MarkdownConsts.LIST:
                case MarkdownConsts.ORDERED_LIST: // List merging
                    let finishedGroup = group.groupStack[i];
                    for (let j = i - 1; j >= 0; j--) {
                        if (!(group.groupStack[j].type === MarkdownConsts.LIST || group.groupStack[j].type === MarkdownConsts.ORDERED_LIST)) {
                            break;
                        }
                        if (group.groupStack[j].level === finishedGroup.level) {
                            if (group.groupStack[j].type === finishedGroup.type) {
                                group.groupStack[j].list = group.groupStack[j].list.concat(finishedGroup.list);
                                group.groupStack.splice(i, 1);
                                break;
                            }
                        }
                    }
            }
        }
        // Merged, remove groups
        // Normal processing for all other components
        // Don't remove last group
        while (group.length() > 0) {
            let finishedGroup = group.groupStack.splice(0, 1)[0];
            switch (finishedGroup.type) {
                case MarkdownConsts.LIST:
                case MarkdownConsts.ORDERED_LIST:
                    final.push(<List ordered={finishedGroup.type === MarkdownConsts.ORDERED_LIST}
                                         list={finishedGroup.list}/>);
                    break;
                case MarkdownConsts.PARAGRAPH:
                    final.push(<Paragraph list={finishedGroup.list}/>);
                    break;
                case MarkdownConsts.CODE:
                    final.push(<Code list={finishedGroup.list}/>);
                    break;
                case MarkdownConsts.QUOTE:
                    final.push(<Quote list={finishedGroup.list}/>);
                    break;
            }
        }
    }

    processMarkdown(markdownString) {
        // console.log("hello", markdownString);
        let lines = markdownString.split("\n");
        let final = [];
        let group = new GroupManager(); // We group related lines together, like lists or paragraphs
        let type = null;
        let result = null;
        let indent = 0;
        // let lastLineBreak = false; // If the last line was a break, then if types match we have to force them apart
        let line;
        for (let i=0; i<lines.length; i++) {
            line = lines[i]; // Don't trim, we need indent on left and potentially, continue line >  < on right
            type = null;
            result = null;
            indent = 0;
            // Determine type of line and indent
            // Parse line starter
            if (line.trim() === "") {
                type = MarkdownConsts.BREAK;
            }
            // What level indent are we at?
            let results = MarkdownRegEx.indent.exec(line);
            if (results) {
                indent = Math.floor(results[1].length / 4);
                line = line.substring(results[1].length);
            }
            results = MarkdownRegEx.quote.exec(line);
            if (results && indent === 0) {
                console.log("matched quote", results, line);
                type = MarkdownConsts.QUOTE;
                group.add(MarkdownConsts.QUOTE, line.slice(results[1].length), {})
            }
            results = MarkdownRegEx.header.exec(line);
            if (results && indent === 0) {
                type = MarkdownConsts.HEADER;
                result = <Header level={results[0].length - 1}>{line.slice(results[0].length)}</Header>;
            }
            results = MarkdownRegEx.list.exec(line);
            if (results) {
                type = MarkdownConsts.LIST;
                group.add(MarkdownConsts.LIST, line.slice(results[0].length), {'level': indent});
            }
            results = MarkdownRegEx.orderedList.exec(line);
            if (results) {
                console.log(results);
                type = MarkdownConsts.ORDERED_LIST;
                group.add(MarkdownConsts.ORDERED_LIST, line.slice(results[0].length), {'level': indent, 'start': parseInt(results[1])});
            }
            results = MarkdownRegEx.horizRule.exec(line);
            if (results) {
                type = MarkdownConsts.HORIZONTAL_RULE;
                result = <HorizontalRule/>;
            }
            // Final processing to decide how to add it to the stack
            // If type is null, it indicates there was no special modifier for line type, making it a paragraph or a code block if indented
            if (type == null) {
                if (indent === 0) {
                    type = MarkdownConsts.PARAGRAPH;
                    group.add(MarkdownConsts.PARAGRAPH, line);
                } else {
                    type = MarkdownConsts.CODE;
                    group.add(MarkdownConsts.CODE, line)
                }
            }
            // If this line isn't to join the current group, complete it
            // If this line was a line break, make the group completed
            if (group.isNotLastType(type) || type === MarkdownConsts.BREAK) {
                this.processGroup(final, group);
            }
            if (result != null) {
                final.push(result);
            } else {
                group.doAdd();
            }
        }
        this.processGroup(final, group);
        // while (group.length() > 0) {
        //     final.push(group.groupStack.splice(0, 1)[0]);
        // }
        // console.log(final[0], final[1]);
        return final;
    }

    render() {
        return (
            <div className={"prose"}>
                {this.processMarkdown(markdownTest)}
                {/*{this.processMarkdown("**Note:** This document is itself written using Markdown; you\n can [see the source for it by adding '.text' to the URL](/projects/markdown/syntax.text).\n")}*/}
            </div>
        );
    }
}

export default Markdown;