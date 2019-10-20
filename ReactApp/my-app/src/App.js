/*global google*/
import React, { Component, useState, useEffect } from "react";
import ReactDOM from "react-dom";
import ReactMap from "./components/ReactMap";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams
} from "react-router-dom";
import axios from "axios";

function Child() {
  const [coordinatesSrc, setCoordinateSrc] = useState(0);
  const [coordinatesDest, setCoordinateDest] = useState(1);
  useEffect(() => {
    setCoordinateSrc([41.878982, -87.625581]);
    setCoordinateDest([41.85258, -87.65141]);
  }, []);
  // We can use the `useParams` hook here to access
  // the dynamic pieces of the URL.
  let { transactionid } = useParams();
  console.log("transactionid is: ", transactionid);
  axios.get(`/api/${transactionid}`).then(({ data: coordinates_returned }) => {
    console.log("user", coordinates_returned);
    setCoordinateSrc(coordinates_returned);
  });

  return (
    <div>
      <h3>TRANCTION ID: {transactionid}</h3>
      <ReactMap source={coordinatesSrc} destination={coordinatesDest} />
    </div>
  );
}

class App extends Component {
  state = {
    id: null
  };

  render() {
    return (
      <div>
        <Router>
          <div>
            <ul>
              <li>
                <Link to="/modus-create">Modus Create</Link>
              </li>
            </ul>
            <Switch>
              <Route path="/:transactionid" children={<Child />} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
///<ReactMap />
