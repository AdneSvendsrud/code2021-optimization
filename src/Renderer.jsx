import React, { useState } from "react";
import { Canvas } from "react-three-fiber";
import { OrbitControls, OrthographicCamera, Stats } from "@react-three/drei";
import Room from "./Objects/Room";
import Boundary from "./Objects/Boundary";
import ExampleBox from "./Objects/ExampleBox";
import { GridHelper, Vector3} from "three";

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

  let [perspective, changePerspective] = useState(new Vector3(0, 512, 0));
  let [buttonText_3d, changeButtonText] = useState("3D");

  // These two might need to be changed to [3] when our algo.py is run
  let [boundary_width, setBoundary_width] = useState(
    jsonObject.planBoundary[2]["x"]
  );
  let [boundary_height, setBoundary_height] = useState(
    jsonObject.planBoundary[2]["y"]
  );
  let [boundary_size, setBoundary_size] = useState(
    Math.max(boundary_height, boundary_width)
  );
  // ^^ 

  try {
    // Feilmeldinger:

    for (const [key, value] of Object.entries(jsonObject.rooms)) {
      let tall = Math.ceil(Math.random()*6) + 4
      RoomsListHOC.push(
        <>
        <Room
          key={key}
          width={value.width}
          height={value.height}
          anchorTopLeftX={value.anchorTopLeftX}
          anchorTopLeftY={value.anchorTopLeftY}
          text={value.type}
        />
        <ExampleBox
         key={key, "examplebox"}
         boxSize={[value.width, tall, value.height]}
         position={[value.anchorTopLeftX + value.width/2, tall/2, value.anchorTopLeftY + value.height/2]}
        />
        </>
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
      <button onClick={() => {setBoundary_width(boundary_width + 1)}}>
        Click me
      </button>
      <button onClick={() => {
        
        if (perspective.x != 0 || perspective.z != 0) {
         changePerspective(new Vector3(0, 512, 0))
        } else {
         changePerspective(new Vector3(500, 512, 1200))}
        }}>
        {buttonText_3d}
      </button>

      <Canvas
        style={{
          height: 512,
          width: 512,
          backgroundColor: "black",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >

      <gridHelper position={new Vector3(boundary_size/2, 0, boundary_size/2)} args={[boundary_size, 20]} />
        {/* Lighting */}
        <ambientLight intensity={0.25} />
        <pointLight intensity={0.75} position={[500, 500, 1000]} />


        {/* EXAMPLE of a box on our plane */}
        {/* <ExampleBox boxSize={[15, 10, 10]} position={[7.5, 5, 5]} /> */}

        {/* Drawing the floorplan boundary */}
        <Boundary width={boundary_width} height={boundary_height} />
        {/* Displaying the rooms */}
        {RoomsListHOC}
        
        {/* <ExampleBox /> {/* use example boxes if we have extra time \*\/} */}
        {/* Our Camera. Feel free to experiment (or change out to a PerspectiveCamera 👀?) */}
        {/* TODO: FIX CAMERA, change all args to a list/object of args */}
        <OrthographicCamera
          makeDefault
          zoom={2}
          top={512}
          bottom={-512}
          left={0}
          right={512}
          near={1}
          far={20000}
          position={perspective}
        />

        {/* Our Controls. Allows us to drag the view and pan around. Try holding down Shift when dragging. */}
        <OrbitControls enableRotate={true} />
        
        
        {/* FPS counter */}
        {/* <Stats /> */}
      </Canvas>
    </React.Fragment>
  );
};

export default Renderer;
