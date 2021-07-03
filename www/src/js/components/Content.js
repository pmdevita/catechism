import { Component } from "preact";
import styles from "./Content.scss"
import Markdown from "./Markdown";

class Content extends Component {
    render(props, state, context) {
        return <div class={"overflow-scroll h-full w-full"}>
            <div class={"m-auto"}>
                <Markdown/>
            </div>
        </div>;
    }
}

export default Content
