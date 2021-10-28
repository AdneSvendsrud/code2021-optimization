import { useRef } from "react";
import { getRandomColor } from "../getRandomColor";

const Room = (props) => {
  const { width, height, anchorTopLeftX, anchorTopLeftY } = props;

  const meshRef = useRef();
  const position = [width / 2 + anchorTopLeftX, 0, height / 2 + anchorTopLeftY];

  return (
    <mesh position={position} ref={meshRef} rotation-x={Math.PI * -0.5}>
      <planeBufferGeometry args={[width, height]} />
      <meshStandardMaterial color={getRandomColor()} />
    </mesh>
  );
};

export default Room;
