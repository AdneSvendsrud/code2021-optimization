import React from "react";
import { Canvas } from "react-three-fiber";
import { OrbitControls, OrthographicCamera, Stats } from "@react-three/drei";
import Room from "./Objects/Room";
import Boundary from "./Objects/Boundary";
import ExampleBox from "./Objects/ExampleBox";
import { GridHelper, Vector3} from "three";
import { data } from "./App"

const Renderer = (props) => {
  const { jsonValue } = props;

  let jsonObject;
    try {
        jsonObject = data[jsonValue]
    } catch (e) {
    // JSON.Parse only works on valid JSON code.
    // This error is thrown whenever the JSON is not valid, e.g. while editing it in the textarea
    console.info("JSON is not currently valid ", e);
    }

    /* console.log("jsonobject: ", jsonObject, jsonObjectIndex, jsonValue, data) */
  
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
{/*       <input type="text" value={boundary_width} onChange={(event) => setBoundary_width(Number(event.currentTarget.value))}></input>
      <button onClick={() => {setBoundary_width(boundary_width + 1)}}>
        Prin
      </button> */}

        
        <div className="strokeme">
        <button onClick={() => {
            if (perspective.x != 0 || perspective.z != 0) {
            changePerspective(new Vector3(0, 512, 0))
            } else {
            changePerspective(new Vector3(500, 512, 1200))}
            }}>
            {buttonText_3d}
        </button> {/* <br />
        Please select your wanted iteration from the last 10: <br />
          <input type="radio" id="0" name="iterationindex" value="0" onChange={(event) => console.log(event.target.value)}/>
          <label htmlFor="0">1</label>
          <input type="radio" id="1" name="iterationindex" value="1" />
          <label htmlFor="1">2</label>
          <input type="radio" id="2" name="iterationindex" value="2" />
          <label htmlFor="2">3</label>
          <input type="radio" id="3" name="iterationindex" value="3" />
          <label htmlFor="3">4</label>
          <input type="radio" id="4" name="iterationindex" value="4" />
          <label htmlFor="4">5</label>
          <input type="radio" id="5" name="iterationindex" value="5" />
          <label htmlFor="5">6</label>
          <input type="radio" id="6" name="iterationindex" value="6" />
          <label htmlFor="6">7</label>
          <input type="radio" id="7" name="iterationindex" value="7" />
          <label htmlFor="7">8</label>
          <input type="radio" id="8" name="iterationindex" value="8" />
          <label htmlFor="8">9</label>
          <input type="radio" id="9" name="iterationindex" value="9" />
          <label htmlFor="9">10</label><br /> */}
        </div>

      <Canvas
        style={{
          height: 612,
          width: 612,
          backgroundColor: "black",
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
        
        <OrthographicCamera
          makeDefault
          zoom={3}
          top={50}
          bottom={-50}
          left={50}
          right={50}
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
