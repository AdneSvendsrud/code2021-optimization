import { useRef } from "react";

// Example 3D Object 10x10x10 box
const ExampleBox = (props) => {
  let size = props.boxSize;
  const meshRef = useRef();

  return (
    // (Almost) all Three elements consist of meshes.
    // A mesh basically combines three things -
    // a geometry (the 3D object shape), a material (the
    // object's texture) and a position.
    <mesh ref={meshRef} {...props}>
      <boxGeometry args={size.map(e => e)} />
      <meshPhongMaterial attach="material" color={"white"} opacity={0.60} transparent/>
    </mesh>
  );
};

export default ExampleBox;
