import React, { Component, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import JsonViewer from "./JsonViewer";

// Our Scene class. This is where all of our threejs code is located.
class Scene extends Component {
  constructor(props) {
    console.log("props are", props);
    super(props);
    this.state = {
      jsonObject: props.jsonObject,
    };
  }

  componentWillMount() {
    window.addEventListener("resize", this.handleWindowResize);
  }

  componentDidMount() {
    this.setupScene();
  }

  // Setting up the scene itself (Camera, angles, fov, effects)
  setupScene = () => {
    this.width = this.container.clientWidth;
    this.height = this.container.clientHeight;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const fov = 60;
    const aspect = this.width / this.height;
    const near = 0.0001;
    const far = Number.MAX_SAFE_INTEGER;
    let camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    camera.position.z = 5;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color("gray");
    scene.add(camera);

    // // // Just an example to introduce you guys to how Three.js works
    // // // The process is basically only four steps.
    // let sphere = new THREE.SphereGeometry();
    // let material = new THREE.MeshBasicMaterial({
    //   color: "gray",
    //   side: THREE.DoubleSide,
    //   depthWrite: false,
    // });
    // let mesh = new THREE.Mesh(sphere, material);
    // scene.add(mesh);

    // Creates the grid
    const helper = new THREE.GridHelper(200, 20);
    helper.rotation.x = Math.PI / 2;
    helper.material.depthWrite = false;
    scene.add(helper);

    // const path = new THREE.Path();
    // path.moveTo(-50, 50);
    // path.lineTo(50, 50);
    // path.lineTo(50, -50);
    // path.lineTo(-50, -50);
    // path.lineTo(-50, 50);
    // const pathPoints = path.getPoints();
    // const pathGeometry = new THREE.BufferGeometry().setFromPoints(pathPoints);
    // const pathMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
    // const mesh = new THREE.Line(pathGeometry, pathMaterial);
    // scene.add(mesh);

    // An example to introduce you guys to how Three.js works by drawing hte outline of the room
    // The process is basically four simple steps.
    // 1. Define the shape. This can be THREE.Shape(), THREE.Spere(), THREE.Path(), etc.
    const square = new THREE.Shape();
    square.moveTo(0, 0);
    this.state.jsonObject.roomBoundary.forEach((vertex) => {
      console.log("Moving vertex to x: ", vertex.x, " y: ", vertex.y);
      square.lineTo(vertex.x, vertex.y);
    });
    square.lineTo(
      this.state.jsonObject.roomBoundary[0].x,
      this.state.jsonObject.roomBoundary[0].y
    );
    // 2. The geometry objects are the body of the 3D model you will be drawing - in this case the 2D square we defined above
    const geometry = new THREE.ShapeGeometry(square);
    // 3. Materials are the skin - the material that will be applied to a geometry
    const material = new THREE.MeshBasicMaterial({
      color: "white",
      side: THREE.DoubleSide,
      depthWrite: false,
    });
    // 4. The Mesh ties objects and materials in together.
    const mesh = new THREE.Mesh(geometry, material);
    // 5. We add the mesh to the scene to display the object!
    scene.add(mesh);

    // Circle
    // const circle = new THREE.Shape();
    // const x = 0;
    // const y = 0;
    // const radius = 0;
    // circle.absarc(x, y, radius);
    // const segments = 100;
    // let geometry = new THREE.ShapeGeometry(circle, segments / 2);
    // let material = new THREE.MeshBasicMaterial({
    //   color: "blue",
    //   side: THREE.DoubleSide,
    //   depthWrite: false,
    // });
    // let mesh = new THREE.Mesh(geometry, material);
    // scene.add(mesh);

    // // World sphere
    // let sphere = new THREE.SphereGeometry(50, 300, 300);
    // let material = new THREE.MeshPhongMaterial({
    //   map: new THREE.TextureLoader().load("/Assets/2_no_clouds_4k.jpg"),
    //   bumpMap: new THREE.TextureLoader().load("/Assets/elev_bump_4k.jpg"),
    //   bumpScale: 0.005,
    //   specularMap: THREE.ImageUtils.loadTexture("/Assets/water_4k.png"),
    //   specular: new THREE.Color("grey"),
    // });
    // let mesh = new THREE.Mesh(sphere, material);
    // scene.add(mesh);
    // sphere = new THREE.SphereGeometry(50.1, 300, 300);
    // material = new THREE.MeshPhongMaterial({
    //   map: new THREE.TextureLoader().load("/Assets/fair_clouds_4k.png"),
    //   transparent: true,
    // });
    // mesh = new THREE.Mesh(sphere, material);
    // scene.add(mesh);

    // const path = new THREE.Path();
    // path.lineTo(0, 0.8);
    // path.quadraticCurveTo(0, 1, 0.2, 1);
    // path.lineTo(1, 1);
    // const points = path.getPoints();
    // geometry = new THREE.BufferGeometry().setFromPoints(points);
    // material = new THREE.LineBasicMaterial({ color: 0xffffff });
    // const line = new THREE.Line(geometry, material);
    // scene.add(line);

    const sphere = new THREE.SphereGeometry();
    const object = new THREE.Mesh(
      sphere,
      new THREE.MeshBasicMaterial(0xff0000)
    );
    const box = new THREE.BoxHelper(object, 0xffff00);
    scene.add(box);

    this.renderer = renderer;
    this.scene = scene;
    this.camera = camera;
    this.object = mesh;

    let spotLight = new THREE.SpotLight(0xffffff, 0.25);
    spotLight.position.set(45, 50, 15);
    camera.add(spotLight);
    this.spotLight = spotLight;

    let ambLight = new THREE.AmbientLight(0x333333);
    ambLight.position.set(5, 3, 5);
    this.camera.add(ambLight);

    this.computeBoundingBox();
  };

  computeBoundingBox = () => {
    let offset = 1.6;
    const boundingBox = new THREE.Box3();
    boundingBox.setFromObject(this.object);
    const center = boundingBox.getCenter();
    const size = boundingBox.getSize();
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = this.camera.fov * (Math.PI / 180);
    let cameraZ = maxDim / 2 / Math.tan(fov / 2);
    cameraZ *= offset;
    this.camera.position.z = center.z + cameraZ;
    const minZ = boundingBox.min.z;
    const cameraToFarEdge = minZ < 0 ? -minZ + cameraZ : cameraZ - minZ;

    this.camera.far = cameraToFarEdge * 3;
    this.camera.lookAt(center);
    this.camera.updateProjectionMatrix();

    let controls = new OrbitControls(this.camera, this.renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.enableZoom = true;
    controls.zoomSpeed = 0.1;
    controls.enableKeys = false;
    controls.screenSpacePanning = false;
    controls.enableRotate = true;
    controls.autoRotate = false;
    controls.dampingFactor = 1;
    controls.autoRotateSpeed = 1.2;
    controls.enablePan = false;
    controls.target.set(center.x, center.y, center.z);
    controls.update();
    this.controls = controls;
    this.renderer.setSize(this.width, this.height);
    this.container.appendChild(this.renderer.domElement);
    this.start();
  };

  start = () => {
    if (!this.frameId) {
      this.frameId = requestAnimationFrame(this.animate);
    }
  };

  renderScene = () => {
    this.renderer.render(this.scene, this.camera);
  };

  animate = () => {
    this.frameId = requestAnimationFrame(this.animate);
    this.controls.update();
    this.renderScene();
  };

  stop = () => {
    cancelAnimationFrame(this.frameId);
  };

  handleWindowResize = () => {
    let width = window.innerWidth;
    let height = window.innerHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
  };

  componentWillUnmount() {
    this.stop();
    this.destroyContext();
  }

  destroyContext = () => {
    this.container.removeChild(this.renderer.domElement);
    this.renderer.forceContextLoss();
    this.renderer.context = null;
    this.renderer.domElement = null;
    this.renderer = null;
  };

  render() {
    const width = "100%";
    const height = "100%";

    return (
      <>
        <div
          ref={(container) => {
            this.container = container;
          }}
          style={{
            width: width,
            height: height,
            position: "absolute",
            overflow: "hidden",
          }}
        ></div>
      </>
    );
  }
}

export default Scene;
