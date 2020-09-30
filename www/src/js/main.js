import { render, Component, Fragment } from 'preact';
import "preact/debug";
import Reader from "./views/Reader";

class App extends Component {
  render(props, state, context) {
    return <Reader/>
  }
}

render(<App/>, document.body)
