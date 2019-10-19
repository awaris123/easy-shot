/*global google*/
import React, { Component } from "react";
import ReactDOM from "react-dom";
import ReactMap from "./components/ReactMap";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          <ReactMap />
        </p>
      </div>
    );
  }
}

export default App;
