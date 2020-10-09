import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

import dropzoneStyles from "./dropzone.module.scss";

const Dropzone = props => {
  const { handler } = props;

  const onDrop = useCallback(acceptedFiles => {
    acceptedFiles.forEach(file => {
      const reader = new FileReader();

      // Set reader event handlers.
      reader.onabort = () => console.log("file reading was aborted");
      reader.onerror = () => console.log("file reading has failed");
      reader.onload = e => {
        console.log(e.target.result);
        handler(file);
      };

      reader.readAsArrayBuffer(file);
    }, []);
  });

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps({
        className: dropzoneStyles.dropzone,
      })}
    >
      <input {...getInputProps({})} />
    </div>
  );
};

export default Dropzone;
