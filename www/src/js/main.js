import { render, Component } from 'preact';

class App extends Component {
  render(props, state, context) {
    return <h1>Hello There</h1>
  }
}

render(<App/>, document.body)
