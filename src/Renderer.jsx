import React from "react";
import { Canvas } from "react-three-fiber";
import { OrbitControls, OrthographicCamera, Stats } from "@react-three/drei";
import Room from "./Objects/Room";
import Boundary from "./Objects/Boundary";
import ExampleBox from "./Objects/ExampleBox";

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
  try {
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
      <Canvas
        style={{
          height: 1024,
          width: 1024,
          backgroundColor: "white",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.25} />
        <pointLight intensity={0.75} position={[500, 500, 1000]} />

        {/* Creates a 200x200 grid with 20 segments */}
        <gridHelper args={[200, 20]} />

        {/* EXAMPLE of a box on our plane */}
        {/* <ExampleBox position={[0, 5, 0]} /> */}

        {/* Drawing the floorplan boundary */}
        <Boundary width={100} height={100} />
        {/* Displaying the rooms */}
        {RoomsListHOC}

        {/* Our Camera. Feel free to experiment (or change out to a PerspectiveCamera 👀?) */}
        <OrthographicCamera
          makeDefault
          zoom={2}
          top={512}
          bottom={-512}
          left={512}
          right={-512}
          near={1}
          far={20000}
          position={[0, 512, 0]}
        />

        {/* Our Controls. Allows us to drag the view and pan around. Try holding down Shift when dragging. */}
        <OrbitControls />

        {/* FPS counter */}
        {/* <Stats /> */}
      </Canvas>
    </React.Fragment>
  );
};

export default Renderer;
