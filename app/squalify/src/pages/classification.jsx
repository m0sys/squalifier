import React, { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import gql from "graphql-tag";

import Grid from "../components/Grid/grid";
import Button from "../components/Button/button";
import ClassOptions from "../components/ClassOptions/class_options";
import Upload from "../components/Upload/upload";
import Layout from "../components/Layout/layout";

import classificationStyles from "../styles/classification.module.scss";
import "../styles/main.scss";

const QUERY_INFO = gql`
  query {
    info
  }
`;

const MAKE_PREDICTION = gql`
  mutation($image: Upload!) {
    makePrediction(image: $image) {
      prediction
      confidence
    }
  }
`;

export default function ClassificationPage() {
  const [image, setImage] = useState(null);
  const [pred, setPred] = useState(null);

  const { loading, error, data: infoData } = useQuery(QUERY_INFO);

  const [
    mutate,
    { loading: loading_pred, error: error_pred, data: predData },
  ] = useMutation(MAKE_PREDICTION, {
    onCompleted: data => {
      const category = data.makePrediction.prediction;
      console.log(category);
      setPred(category === "front-squat" ? 0 : 1);
      console.log(pred);
    },
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  if (loading_pred) return <div>Loading...</div>;
  if (error_pred) return <div>{error_pred.message}</div>;

  function onUploadCompleted(file) {
    console.log("Upload Completed");
    console.log(file);
    setImage(file);
  }

  function onHandleClick() {
    console.log("Classify!");
    if (!image) {
      console.log("No images set");
      return;
    }

    console.log(image);

    mutate({ variables: { image } });
  }
  return (
    <Layout>
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
          <ClassOptions category={pred} />
        </div>
      </Grid>
    </Layout>
  );
}
