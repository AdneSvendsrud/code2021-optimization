import React from "react";

// Formats raw JSON into a nicely tabbed version that looks good.
function prettyPrint(value: string) {
  let pretty = value;
  try {
    const obj = JSON.parse(pretty);
    pretty = JSON.stringify(obj, undefined, 4);
  } catch (e) {
    // JSON.Parse only works on valid JSON code.
    // This error is thrown whenever the JSON is not valid, e.g. while editing it in the textarea
    console.info("JSON is not currently valid ", e);
  }
  return pretty;
}

// Displays the JsonViewer
export const JsonViewer = (props) => {
  const { jsonValue, setJsonValue } = props;

  return (
    <React.Fragment>
      <textarea
        name="jsonValueArea"
        id="JsonValue"
        cols={120}
        rows={20}
        value={prettyPrint(jsonValue)}
        onChange={(e) => setJsonValue(e.target.value.replace(/'/g, '"'))}
      />
    </React.Fragment>
  );
};

export default JsonViewer;
