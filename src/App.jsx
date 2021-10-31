import React, { useState } from "react";
import "./styles.css";
import Renderer from "./Renderer";
import JsonViewer from "./JsonViewer";

let jsonlist = ["evo_final_solution.json", "evo_0.json"];

/* for (let i=0; i<=11; i++){
  jsonlist.append(`evo_${i}.json`)
} */


let index = 0;
let data = []

for (let i in jsonlist){
  data.push(JSON.parse(JSON.stringify(require(`./${jsonlist[i]}`))))
}

console.log(data)

export default function App() {
  // Storing the initial JSON value inside of a variable.
  // This basically gives us a (const jsonValue) and a (function setJsonValue) with which changes jsonValue
  return (
    <div className="App">
      <h1>Arealize Start Code Hackathon 2021</h1>
      <div className="App-container">
        <div className="App-container__renderer">
          <Renderer jsonValue={0} />
        </div>
        <div className="App-container__renderer">
          <Renderer jsonValue={1} />
        </div>
      </div>
    </div>
  );
}

export { data };