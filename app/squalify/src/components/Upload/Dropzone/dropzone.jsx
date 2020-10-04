import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

import dropzoneStyles from "./dropzone.module.scss";

const Dropzone = props => {
  const [isLoading, setIsLoading] = useState(false);

  const { onUploadCompleted } = props;

  const onDrop = useCallback(acceptedFiles => {
    acceptedFiles.forEach(file => {
      const reader = new FileReader();

      // Set reader event handlers.
      reader.onabort = () => console.log("file reading was aborted");
      reader.onerror = () => console.log("file reading has failed");
      reader.onloadstart = () => setIsLoading(true);
      reader.onload = e => {
        console.log(e.target.result);
      };

      reader.onloadend = () => setIsLoading(false);

      reader.readAsArrayBuffer(file);

      // reader.readAsArrayBuffer(file);
      onUploadCompleted(file);
    }, []);
  });

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps({
        className: dropzoneStyles.dropzone,
        style: {
          opacity: isLoading ? 1 : 0,
        },
      })}
    >
      <input
        {...getInputProps({
          style: {
            backgroundColor: isLoading ? "red" : "none",
          },
        })}
      />
    </div>
  );
};

export default Dropzone;
