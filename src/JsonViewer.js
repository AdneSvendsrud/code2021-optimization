import React, { useState } from "react";

export const JsonViewer = (props) => {
  return (
    <>
      <textarea
        name="jsonValueArea"
        id="JsonValue"
        cols="120"
        rows="20"
        value={props.jsonValue}
        onChange={(e) => props.setJsonValue(e.target.value)}
      ></textarea>
    </>
  );
};

export default JsonViewer;
