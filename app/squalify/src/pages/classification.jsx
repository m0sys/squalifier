import React, { useState } from "react";
import { useMutation } from "@apollo/client";
import gql from "graphql-tag";

import Grid from "../components/Grid/grid";
import Layout from "../components/Layout/layout";
import PredictionPanel from "../components/PredictionPanel/prediction_panel";

import "../styles/main.scss";

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

  const [mutate, { loading: loading_pred, error: error_pred }] = useMutation(
    MAKE_PREDICTION,
    {
      onCompleted: data => onPredCompleted(data),
    }
  );

  const children = loadChildren(loading_pred, error_pred);

  function loadChildren(loading, error) {
    if (error) return <div>{error.message}</div>;
    if (loading) return <div>Loading...</div>;

    return (
      <PredictionPanel
        onHandleClick={onHandleClick}
        onUploadCompleted={onUploadCompleted}
        category={pred}
      />
    );
  }

  function onPredCompleted(data) {
    const category = data.makePrediction.prediction;
    setPred(category === "front-squat" ? 0 : 1);
  }

  function onUploadCompleted(file) {
    setImage(file);
  }

  function onHandleClick() {
    if (!image) {
      console.log("No images set");
      return;
    }
    mutate({ variables: { image } });
  }
  return (
    <Layout>
      <Grid hasMinHeight center>
        {children}
      </Grid>
    </Layout>
  );
}
