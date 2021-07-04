import { Component } from "preact";
import styles from "./TOCRow.scss"

class TOCRow extends Component {
    constructor() {
        super();

        this.state = {
            open: false,
            selected: false
        };

        this.toggle = this.toggle.bind(this);
        this.getButton = this.getButton.bind(this);
        this.getSections = this.getSections.bind(this);
        this.goTo = this.goTo.bind(this);
    }

    toggle() {
        this.setState({ open: !this.state.open });
        // this.parent.children.closeAll()
    }

    getButton(props) {
        return props.sections.length == 0 ?
            <div class={styles.NoButton}></div> :
            <div class={styles.ExpandButton} onclick={this.toggle}>{
                this.state.open ? 
                    <span class="material-icons">expand_more</span> :     
                    <span class="material-icons">chevron_right</span>
                }
            </div>
    }

    getSections(props) {
        if (!this.state.open) return null;
        
        let index = 0;

        return props.sections.map(item => {
            let childIndexPath = [...props.indexPath];
            childIndexPath.push(index++);

            return <TOCRow title={item.title} verse={item.verse} sections={item.sections} indexPath={childIndexPath} parent={this}/>
        });
    }

    goTo(props) {
        // this.deselectAll(props);
        this.setState({ selected: true });

        // get verses starting from props.verse
    }

    render(props, state, context) {
        // selected style
        // let highlight = state.selected ? "bg-white" : "";
        let highlight = "";
        
        // open styles
        // let bold = state.open ? "font-medium" : "";
        // let faded = state.open ? "" : "opacity-40";
        // let bold = state.selected ? "font-medium" : "";
        // let faded = state.selected ? "" : "opacity-40";
        let bold = "";
        let faded = "";

        return <div>
            <div class={"flex w-full items-center cursor-pointer hover:bg-black hover:bg-opacity-4 border-b " + highlight + " " + faded} onclick={() => this.goTo(props)}>
                <div style={{width: ((props.indexPath.length - 1) * 2.6).toString() + "rem"}}/>
                {this.getButton(props)}
                <div class={"w-full p-4 pl-0 text-left " + bold}>
                    {props.title}
                </div>
            </div>
            {this.getSections(props)}
        </div>
    }
}

export default TOCRow
