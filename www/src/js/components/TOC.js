import { Component } from "preact";
import styles from "./TOC.scss"

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
    }

    getContent() {
        return this.traverse(this.state.toc);
    }

    traverse(item) {
        const listItems = item.map(item =>
            <li>{item.title}{this.traverse(item.sections)}</li>
        );
        return <ul>{listItems}</ul>
    }

    render(props, state, context) {
        return <div class={styles.TOC}>
            <h1>Table of Contents</h1>
            {this.getContent()}
        </div>;
    }
}

export default TOC
