import React, { useState } from "react";
import { Canvas } from "react-three-fiber";
import { OrbitControls, OrthographicCamera, Stats } from "@react-three/drei";
import Room from "./Objects/Room";
import Boundary from "./Objects/Boundary";
import ExampleBox from "./Objects/ExampleBox";
import { GridHelper, Vector3} from "three";
import { data } from "./App"

let i = 0;

const Renderer = (props) => {
    let [jsonObjectIndex, setJsonIndex] = useState(props['jsonValue']);
    let jsonObject;

    try {
        jsonObject = data[jsonObjectIndex]
    } catch (e) {
        // JSON.Parse only works on valid JSON code.
        // This error is thrown whenever the JSON is not valid, e.g. while editing it in the textarea
        console.info("JSON is not currently valid ", e);
    }
  
    // The rooms in jsonObject.rooms are turned into a list of <Room> components.
    let RoomsListHOC = [];

    let [perspective, changePerspective] = useState(new Vector3(0, 512, 0));

    // the plan wass to change this between "2d" and "3D" but the camera didnt cooperate
    let [buttonText_3d, changeButtonText] = useState("3D");

    // Find the floor boundaries dynamically
    let [boundary_width, setBoundary_width] = useState(
        jsonObject.planBoundary[3]["x"]
    );
    let [boundary_height, setBoundary_height] = useState(
        jsonObject.planBoundary[3]["y"]
    );
    let [boundary_size, setBoundary_size] = useState(
        Math.max(boundary_height, boundary_width)
    );

    try {
        // fill the room list with 2d and 3d objects of the rooms
        for (const [key, value] of Object.entries(jsonObject.rooms)) {
        let tall = Math.ceil(Math.random()*6) + 4
        RoomsListHOC.push(
            <>
            <Room
            key={key, "roombox"}
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
        <React.Fragment >            
            <div className="strokeme">
            <button onClick={() => {
                if (perspective.x != 0 || perspective.z != 0) {
                changePerspective(new Vector3(0, 512, 0))
                } else {
                changePerspective(new Vector3(500, 512, 1200))}
                }}>
                {buttonText_3d}
            </button> <br />
            
            {
                (i === 0) ? 
                    <></>:
                <>
                Please select your wanted iteration from the last 10: <br />
                <input type="radio" id="1" name="iterationindex" value="1" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="1">1</label>
                  <input type="radio" id="2" name="iterationindex" value="2" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="2">2</label>
                  <input type="radio" id="3" name="iterationindex" value="3" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="3">3</label>
                  <input type="radio" id="4" name="iterationindex" value="4" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="4">4</label>
                  <input type="radio" id="5" name="iterationindex" value="5" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="5">5</label>
                  <input type="radio" id="6" name="iterationindex" value="6" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="6">6</label>
                  <input type="radio" id="7" name="iterationindex" value="7" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="7">7</label>
                  <input type="radio" id="8" name="iterationindex" value="8" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="8">8</label>
                  <input type="radio" id="9" name="iterationindex" value="9" onChange={(event) => setJsonIndex(event.target.value)}/>
                  <label htmlFor="9">9</label><br /></>}
            
            
{/*               <input type="radio" id="0" name="iterationindex" value="0" onChange={(event) => setJsonIndex(event.target.value)}/>
              <label htmlFor="0">1</label> */}
              
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
            
            <OrthographicCamera
            makeDefault
            zoom={3}
            top={50}
            bottom={-50}
            left={50}
            right={50}
            near={1}
            far={20000}
            position={perspective}
            />

            {/* Our Controls. Allows us to drag the view and pan around. Try holding down Shift when dragging. */}
            <OrbitControls enableRotate={true} />
            
            
            {/* FPS counter */}
            {/* <Stats /> */}
        </Canvas>
        {i++}
        </React.Fragment>
        
    );
};

export default Renderer;
