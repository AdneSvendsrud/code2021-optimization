import { useRef } from "react";

const Boundary = (props) => {
  const { width, height } = props;

  const meshRef = useRef();
  const position = [width / 2, 0, height / 2];

  return (
    <mesh position={position} ref={meshRef} rotation-x={Math.PI * -0.5}>
      <planeBufferGeometry args={[width, height]} />
      <meshPhongMaterial color="#f6f6f6" opacity={0.7} transparent />
    </mesh>
  );
};

export default Boundary;
