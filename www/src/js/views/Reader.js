import { Component } from 'preact';
import styles from './Reader.scss';
import TOC from '../components/TOC';
import Content from '../components/Content';

class Reader extends Component {
    render(props, state, context) {
        return <div class="flex h-full text-gray-900">
            <TOC/>
            <Content/>
        </div>;
    }
}

export default Reader
