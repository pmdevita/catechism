import { Component } from "preact";
import styles from "./Content.scss"
import Markdown from "./Markdown";
import {getText} from "../api";

class Content extends Component {
    state = {
        text: []
    }

    componentDidMount() {
        getText(0, 100).then((data) => this.setState({text: data}))
    }

    render(props, state, context) {
        return <div class={"overflow-auto h-full"}>
            <div class={"m-auto"}>
                {state.text.map(t => <Markdown text={t}/>)}
            </div>
        </div>;
    }
}

export default Content
