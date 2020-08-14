import { render, Component, Fragment } from 'preact';
import Reader from "./views/Reader";

class App extends Component {
  render(props, state, context) {
    return <Reader><span>test child</span></Reader>
  }
}

render(<App/>, document.body)
