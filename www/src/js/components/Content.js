import { Component } from "preact";
import styles from "./Content.scss"
import Markdown from "./Markdown";

class Content extends Component {
    render(props, state, context) {
        return <div class={styles.Content}>
            <div class={styles.Text}>
                <Markdown/>
            </div>
        </div>;
    }
}

export default Content
