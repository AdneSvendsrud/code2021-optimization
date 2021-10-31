import React, { useState } from "react";
import "./styles.css";
import Renderer from "./Renderer";
import JsonViewer from "./JsonViewer";

let jsonData = require('./basic_example_input.json');

let jsonlist = ["basic_example_input.json", "json2", "json3"]
let index = 0;

let data = {json1: {boundaries: null, coordinates: [0, 1]}, json2: {}, json3: {boundaries: "here", coordinates: [1, 2]}}

console.log(data[jsonlist[index]])

export default function App() {
  // Storing the initial JSON value inside of a variable.
  // This basically gives us a (const jsonValue) and a (function setJsonValue) with which changes jsonValue
  const [jsonValue, setJsonValue] = useState(
    JSON.stringify(require(`./${jsonlist[index]}`))
  );
  const [jsonValue2, setJsonValue2] = useState(
    JSON.stringify(require('./basic_example_input2.json'))
  );
  const [jsonValue3, setJsonValue3] = useState(
    JSON.stringify(require('./basic_example_input3.json'))
  );
  const [jsonValue4, setJsonValue4] = useState(
    JSON.stringify(require('./basic_example_input4.json'))
  );

  return (
    <div className="App">
      <h1>ArealizeAi</h1>
      <div className="App-container">
        <div className="App-container__renderer">
          <Renderer jsonValue={jsonValue} />
        </div>
        <div className="App-container__renderer">
          <Renderer jsonValue={jsonValue2} />
        </div>
      </div>
    </div>
  );
}
