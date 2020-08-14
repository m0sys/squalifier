import React, {useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import uploadStyles from "./upload.module.scss";

import uploadIcon from "../../images/upload2.svg";


const Upload = (props) => {
  const [count, setCount] = useState(0);


  return (
    <div className={uploadStyles.uploadContainer}>
      <div className={uploadStyles.iconContainer}>
        <img className={uploadStyles.iconImg} src={uploadIcon} alt="upload"/>
      </div>
      <p>upload an image to classify</p>
    </div>
  );
};


export default Upload;