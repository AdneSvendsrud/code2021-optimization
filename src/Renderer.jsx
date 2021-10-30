import React, { useState } from "react";
import { Canvas } from "react-three-fiber";
import { OrbitControls, OrthographicCamera, Stats } from "@react-three/drei";
import Room from "./Objects/Room";
import Boundary from "./Objects/Boundary";
import ExampleBox from "./Objects/ExampleBox";
import { GridHelper } from "three";

const Renderer = (props) => {
  const { jsonValue } = props;
  let jsonObject;
  try {
    jsonObject = JSON.parse(jsonValue); // A javascript object containing the properties of jsonValue
  } catch (e) {
    // JSON.Parse only works on valid JSON code.
    // This error is thrown whenever the JSON is not valid, e.g. while editing it in the textarea
    console.info("JSON is not currently valid ", e);
  }

  // The rooms in jsonObject.rooms are turned into a list of <Room> components.
  let RoomsListHOC = [];
  // These two might need to be changed to [3] when our algo.py is run
  let [boundary_width, setBoundary_width] = useState(
    jsonObject.planBoundary[2]["x"]
  )
  let [boundary_height, setBoundary_height] = useState(
    jsonObject.planBoundary[2]["y"]
  )
  // ^^ 

  try {
    // Feilmeldinger:

    for (const [key, value] of Object.entries(jsonObject.rooms)) {
      RoomsListHOC.push(
        <Room
          key={key}
          width={value.width}
          height={value.height}
          anchorTopLeftX={value.anchorTopLeftX}
          anchorTopLeftY={value.anchorTopLeftY}
          text={value.type}
        />
      );
    }
  } catch (e) {
    // JSON.Parse only works on valid JSON code.
    // This error is thrown whenever the JSON is not valid, e.g. while editing it in the textarea
    console.info("JSON is not currently valid ", e);
  }

  return (
    <React.Fragment>
      <input type="text" value={boundary_width} onChange={(event) => setBoundary_width(Number(event.currentTarget.value))}></input>
      <button onClick={() => {setBoundary_width(boundary_width + 1); console.log(boundary_width)}}>
        Click me
      </button>
      <Canvas
        style={{
          height: 512,
          width: 512,
          backgroundColor: "#f6f6f6",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >

      <gridHelper args={[200, 20]} />
        {/* Lighting */}
        <ambientLight intensity={0.25} />
        <pointLight intensity={0.75} position={[500, 500, 1000]} />


        {/* EXAMPLE of a box on our plane */}
        <ExampleBox position={[5, 5, 5]} />

        {/* Drawing the floorplan boundary */}
        <Boundary width={boundary_width} height={boundary_height} />
        {/* Displaying the rooms */}
        {RoomsListHOC}
        
        {/* <ExampleBox /> {/* use example boxes if we have extra time \*\/} */}
        {/* Our Camera. Feel free to experiment (or change out to a PerspectiveCamera 👀?) */}
        <OrthographicCamera
          makeDefault
          zoom={4}
          top={512}
          bottom={-512}
          left={0}
          right={512}
          near={1}
          far={20000}
          position={[0, 512, 0]}
        />

        {/* Our Controls. Allows us to drag the view and pan around. Try holding down Shift when dragging. */}
        <OrbitControls enableRotate={true} keys={{LEFT: 'ArrowLeft', UP: 'ArrowUp', RIGHT: 'ArrowRight', BOTTOM: 'ArrowDown'}}/>
        
        
        {/* FPS counter */}
        {/* <Stats /> */}
      </Canvas>
    </React.Fragment>
  );
};

export default Renderer;
