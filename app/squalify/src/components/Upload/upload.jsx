import React, { useRef, useState } from "react";

import Dropzone from "./Dropzone/dropzone";
import uploadStyles from "./upload.module.scss";
import uploadIcon from "../../images/upload2.svg";

const Upload = props => {
  const { onUploadCompleted } = props;

  const [imgLoaded, setImgLoaded] = useState(false);
  const imgRef = useRef();

  function handleDropzone(file) {
    const urlReader = new FileReader();

    urlReader.onload = e => {
      onLoadUrl(e, file);
    };

    urlReader.readAsDataURL(file);
  }

  function onLoadUrl(e, file) {
    setImgLoaded(true);
    setContainerBgImage(e);
    onUploadCompleted(file);
  }

  function setContainerBgImage(e) {
    imgRef.current.style.backgroundImage = `url(${e.target.result})`;
  }

  return (
    <div className={uploadStyles.uploadContainer}>
      <div
        className={uploadStyles.imgOverlay}
        style={{ display: imgLoaded ? "block" : "none" }}
      >
        <div ref={imgRef} className={uploadStyles.img} />
      </div>

      <Dropzone handler={handleDropzone} />
      <div className={uploadStyles.iconContainer}>
        <img className={uploadStyles.iconImg} src={uploadIcon} alt="upload" />
      </div>
      <p>click or drag to upload a file for classification</p>
    </div>
  );
};

export default Upload;
