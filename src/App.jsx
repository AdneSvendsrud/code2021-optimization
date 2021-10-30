import React, { useState } from "react";
import "./styles.css";
import Renderer from "./Renderer";
import JsonViewer from "./JsonViewer";

let jsonData = require('./basic_example_input.json');

export default function App() {
  // Storing the initial JSON value inside of a variable.
  // This basically gives us a (const jsonValue) and a (function setJsonValue) with which changes jsonValue
  const [jsonValue, setJsonValue] = useState(
    JSON.stringify(jsonData)
  );
  const [jsonValue2, setJsonValue2] = useState(
    JSON.stringify(require('./basic_example_input2.json'))
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
        <div className="App-container__renderer">
          <Renderer jsonValue={jsonValue} />
        </div>
      </div>
    </div>
  );
}
