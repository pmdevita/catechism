import { Component } from "preact";
import markdownTest from "../test/markdownTest";

const MarkdownRegEx = {
    header: new RegExp("^#+ "),
    list: new RegExp("^([\*|\\-|\+]) "),
    orderedList: new RegExp("^(\\d+)\. "),
    blank: new RegExp("^\s*$"),
    indent: new RegExp("^( +)\\S")
};

const MarkdownConsts = {
    HEADER: "HEADER",
    LIST: "LIST",
    PARAGRAPH: "PARAGRAPH",
    CODE: "CODE",
    ORDERED_LIST: "ORDERED_LIST",
    BLANK: "BLANK"
};

const LEVEL_TYPES = new Set([MarkdownConsts.LIST, MarkdownConsts.ORDERED_LIST]);

function Header(props) {
    return h("h" + props.level.toString(), null, props.text);
}

function List(props) {
    return h((props.ordered ? "ol" : "ul"), {}, props.list.map((data) => {
        if (typeof data === 'object') {
            return <List ordered={data.ordered} list={data.list}/>;
        } else {
            return <li>{data}</li>;
        }
    }))
}

function Paragraph(props) {
    return <p>{props.list.join(">join<")}</p>
}

function Code(props) {
    return <code>{props.list.join("\n")}</code>
}


class GroupManager {
    constructor() {
        this.groupStack = [];
    }

    add(type, value, data) {
        this.staged = {"type": type, "value": value, "data": data}
    }

    doAdd() {
        // If type matches, add on to current group
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
        for (let i = group.length() - 1; i >= 1; i--) { // Now merge the flattened lists
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
            }
        }
    }

    processMarkdown(markdownString) {
        // console.log("hello", markdownString);
        let lines = markdownString.split("\n");
        let final = [];
        let group = new GroupManager();
        let type = null;
        let result = null;
        let indent = 0;
        let line;
        for (let i=0; i<lines.length; i++) {
            line = lines[i];
            type = null;
            result = null;
            indent = 0;
            // Parse line starter
            let results = MarkdownRegEx.indent.exec(line);
            if (results) {
                indent = Math.floor(results[1].length / 4);
                line = line.substring(results[1].length);
            }
            results = MarkdownRegEx.header.exec(line);
            if (results && indent === 0) {
                type = MarkdownConsts.HEADER;
                result = <Header level={results[0].length - 1} text={line.slice(results[0].length)}/>;
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
            results = MarkdownRegEx.blank.exec(line);
            if (results) {
                continue; // For now, paragraphs will need to know if there are two
            }
            if (type == null) {
                if (indent === 0) {
                    type = MarkdownConsts.PARAGRAPH;
                    group.add(MarkdownConsts.PARAGRAPH, line);
                } else {
                    type = MarkdownConsts.CODE;
                    group.add(MarkdownConsts.CODE, line)
                }
            }
            if (group.isNotLastType(type)) {
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
            <div>
                {this.processMarkdown(markdownTest)}
                {/*{this.processMarkdown("* asdf\n* asdf\n* asdf\n    * fasda\n    * fdsa\n* 1234\n* 1234\nasdfasdfasdf")}*/}
            </div>
        );
    }
}

export default Markdown;