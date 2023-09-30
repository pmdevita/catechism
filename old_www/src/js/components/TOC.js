import { Component } from "preact";
import TOCRow from './TOCRow';
import styles from "./TOC.scss"

class TOC extends Component {
    constructor() {
        super();

        this.state = {
            hidden: false,
            toc: [
                {title: "Part 1: The Profession of Faith", verse: 1, sections: [
                    {title: "Section 1", verse: 60, sections: [
                        {title: "Chapter 1", verse: 120, sections: [
                            {title: "Article 1", verse: 240, sections: []}
                        ]}
                    ]},
                    {title: "Section 2", verse: 180, sections: [
                        {title: "Chapter 1", verse: 240, sections: []},
                        {title: "Chapter 2", verse: 260, sections: []}
                    ]},
                    {title: "Section 3", verse: 300, sections: []}
                ]},
                {title: "Part 2: The Celebration of the Christian Mystery", verse: 500, sections: []},
                {title: "Part 3: Life in Christ", verse: 1000, sections: []},
                {title: "Part 4: Christian Prayer", verse: 1500, sections: []}
            ]
        };

        this.drawRows = this.drawRows.bind(this);
        this.hide = this.hide.bind(this);
    }

    drawRows() {
        let index = 0;
        return this.state.toc.map(item =>
            <TOCRow title={item.title} verse={item.verse} sections={item.sections} indexPath={[index]}/>
        );
    }

    hide() {
        this.setState({ hidden: true });
    }

    render(props, state, context) {
        return state.hidden ? <div/> : 
            <div class="overflow-auto h-full w-80 bg-black bg-opacity-2 border-r">
                <div class="flex items-center p-2 pl-4"> 
                    <div class="flex-1 font-medium">Catechism of the Catholic Church</div>
                    <div class="flex flex-shrink-0 p-2 rounded-md cursor-pointer hover:bg-black hover:bg-opacity-5" onclick={this.hide}>
                        <span class="material-icons">menu_open</span>
                    </div>
                </div>
                <div class="p-4 pt-12 font-serif font-bold text-xl">Table of Contents</div>
                {this.drawRows()}
            </div>;
    }
}

export default TOC
