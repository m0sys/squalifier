import React from "react";

import Button from "../Button/button";
import ClassOptions from "../ClassOptions/class_options";
import Upload from "../Upload/upload";

import predictionPanelStyles from "./prediction_panel.module.scss";

const PredictionPanel = props => {
  const { onHandleClick, onUploadCompleted, category } = props;

  return (
    <React.Fragment>
      <h3 className={predictionPanelStyles.headline}>
        Front Squat or Back Squat?
      </h3>
      <div className={predictionPanelStyles.upload}>
        <Upload onUploadCompleted={onUploadCompleted} />
      </div>
      <div className={predictionPanelStyles.cta}>
        <Button onClick={onHandleClick} text="Classify" />
      </div>
      <div className={predictionPanelStyles.options}>
        <ClassOptions category={category} />
      </div>
    </React.Fragment>
  );
};

export default PredictionPanel;
