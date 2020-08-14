import { Component } from 'preact';
import styles from './Reader.scss';

class Reader extends Component {
    render(props, state, context) {
        return <div class={styles.Reader}>
            {props.children}
        </div>;
    }
}

export default Reader
