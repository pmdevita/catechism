import { Component } from "preact";
import styles from "./TOCRow.scss"

class TOCRow extends Component {
    constructor() {
        super();

        this.state = { open: false };

        this.toggle = this.toggle.bind(this);
        this.getButton = this.getButton.bind(this);
        this.getSections = this.getSections.bind(this);
    }

    toggle() {
        this.setState({ open: !this.state.open })
    }

    getButton(props) {
        return props.sections.length == 0 ?
            <button class={styles.ExpandButton}></button> :
            <button class={styles.ExpandButton} onclick={this.toggle}>{this.state.open ? "v" : ">"}</button>
    }

    getSections(props) {
        if (!this.state.open) return null;
        
        let index = 0;

        return props.sections.map(item => {
            let childIndexPath = [...props.indexPath]
            childIndexPath.push(index++);

            return <TOCRow style={{marginLeft: "28px"}} title={item.title} verse={item.verse} sections={item.sections} indexPath={childIndexPath}/>
        });
    }

    render(props, state, context) {
        return <div style={props.style}>
            <div class={styles.Row}>
                {this.getButton(props)}
                <a class={styles.Link} href={"#verse=" + props.verse}>
                    {props.title}
                </a>
            </div>
            {this.getSections(props)}
        </div>
    }
}

export default TOCRow
