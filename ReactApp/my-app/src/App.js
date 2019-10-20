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
  axios({
    url: `http://348404fd.ngrok.io/react?tid=${transactionid}`,
    method: "get",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    }
  }).then(({ data: coordinates_returned }) => {
    console.log("response", coordinates_returned);
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
