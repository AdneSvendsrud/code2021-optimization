import React, { useState } from "react";

function prettyPrint(value) {
  var ugly = value;
  var obj = JSON.parse(ugly);
  var pretty = JSON.stringify(obj, undefined, 4);
  return pretty;
}

export const JsonViewer = (props) => {
  return (
    <>
      <textarea
        name="jsonValueArea"
        id="JsonValue"
        cols="120"
        rows="20"
        value={prettyPrint(props.jsonValue)}
        onChange={(e) => props.setJsonValue(e.target.value)}
      ></textarea>
    </>
  );
};

export default JsonViewer;
