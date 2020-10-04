import React, { useState, useRef } from "react";

import Header from "../components/Header/header";
import Grid from "../components/Grid/grid";
import Button from "../components/Button/button";
import ClassOptions from "../components/ClassOptions/class_options";
import Upload from "../components/Upload/upload";

import classificationStyles from "../styles/classification.module.scss";
import "../styles/main.scss";

export default function ClassificationPage() {
  const [image, setImage] = useState(null);

  function onUploadCompleted(res) {
    console.log("Upload Completed");
    console.log(res);
    setImage(res);
  }

  function onHandleClick() {
    console.log("Classify!");
  }
  return (
    <div>
      <Header />
      <Grid hasMinHeight center>
        <h3 className={classificationStyles.headline}>
          Front Squat or Back Squat?
        </h3>
        <div className={classificationStyles.upload}>
          <Upload onUploadCompleted={onUploadCompleted} />
        </div>
        <div className={classificationStyles.cta}>
          <Button onClick={onHandleClick} text="Classify" />
        </div>
        <div className={classificationStyles.options}>
          <ClassOptions />
        </div>
      </Grid>
    </div>
  );
}
