import { Component } from "preact";
import TOCRow from './TOCRow';

class TOC extends Component {
    constructor() {
        super();

        this.state = { 
            toc: [
                {"title": "Part 1: The Profession of Faith", "verse": 1, "sections": [
                    {"title": "Section 1", "verse": 60, "sections": [
                        {"title": "Chapter 1", "verse": 120, "sections": [
                            {"title": "Article 1", "verse": 240, "sections": []}
                        ]}
                    ]},
                    {"title": "Section 2", "verse": 180, "sections": [
                        {"title": "Chapter 1", "verse": 240, "sections": []},
                        {"title": "Chapter 2", "verse": 260, "sections": []}
                    ]},
                    {"title": "Section 3", "verse": 300, "sections": []}
                ]},
                {"title": "Part 2: The Celebration of the Christian Mystery", "verse": 500, "sections": []},
                {"title": "Part 3: Life in Christ", "verse": 1000, "sections": []},
                {"title": "Part 4: Christian Prayer", "verse": 1500, "sections": []}
            ]
        };

        this.draw = this.draw.bind(this);
    }

    draw() {
        let index = 0;
        return this.state.toc.map(item =>
            <TOCRow title={item.title} verse={item.verse} sections={item.sections} indexPath={[index]}/>
        );
    }

    render(props, state, context) {
        return <div class="overflow-scroll h-full w-80 bg-gray-50 border-r border-gray-100 ">
            <h3 class="m-0 p-4 pt-16">Table of Contents</h3>
            {this.draw()}
        </div>;
    }
}

export default TOC
