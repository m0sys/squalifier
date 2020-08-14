import React from "react";

import Header from "../components/Header/header";
import Container from "../components/Container/container";
import Button from "../components/Button/button";
import ClassOptions from "../components/ClassOptions/class_options";
import Upload from "../components/Upload/upload";

import "../styles/main.scss";

export default function ClassificationPage() {
  
  return (
    <div>
      <Header />
      <Container>
        <h3>Front Squat or Back Squat?</h3>
        <Upload />
        <Button text="Classify" />
        <ClassOptions />
      </Container>
    </div>

  )
}