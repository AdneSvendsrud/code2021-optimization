import React, { useState } from "react";
import JsonViewer from "./JsonViewer";
import Scene from "./Scene";

export const Wrapper = () => {
  const [jsonValue, setJsonValue] = useState(
    JSON.stringify({
      planBoundary: [
        {
          x: 0,
          y: 0,
        },
        {
          x: 100,
          y: 0,
        },
        {
          x: 100,
          y: 100,
        },
        {
          x: 0,
          y: 100,
        },
      ],

      rooms: {
        "1": {
          id: "1",
          width: 10,
          height: 10,
          anchorTopLeftX: 0,
          anchorTopLeftY: 0,
          type: "workRoom",
        },
        "2": {
          id: "2",
          width: 10,
          height: 10,
          anchorTopLeftX: 0,
          anchorTopLeftY: 0,
          type: "workRoom",
        },
        "3": {
          id: 3,
          width: 60,
          height: 50,
          anchorTopLeftX: 0,
          anchorTopLeftY: 0,
          type: "meetRoom",
        },
        "4": {
          id: 4,
          width: 20,
          height: 20,
          anchorTopLeftX: 0,
          anchorTopLeftY: 0,
          type: "openWork",
        },
      },
    })
  );
  const jsonObject = JSON.parse(jsonValue);
  console.log(jsonObject);

  return (
    <>
      <h1>StartCode Hachathon 2021</h1>
      <JsonViewer jsonValue={jsonValue} setJsonValue={setJsonValue} />
      <Scene jsonObject={jsonObject} />
    </>
  );
};

export default JsonViewer;
