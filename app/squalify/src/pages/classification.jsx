import React, { useState } from "react";
import { useQuery } from "@apollo/client";
// import { graphql } from "gatsby";
import gql from "graphql-tag";

import Grid from "../components/Grid/grid";
import Button from "../components/Button/button";
import ClassOptions from "../components/ClassOptions/class_options";
import Upload from "../components/Upload/upload";
import Layout from "../components/Layout/layout";

import classificationStyles from "../styles/classification.module.scss";
import "../styles/main.scss";

// export const QUERY_INFO = graphql`
//   query {
//     squalify {
//       info
//     }
//   }
// `;

const APOLLO_JOBS = gql`
  query {
    info
  }
`;

export default function ClassificationPage() {
  const [image, setImage] = useState(null);

  const { loading, error, data: apolloData } = useQuery(APOLLO_JOBS);
  console.log(error && error.networkError);
  console.log(apolloData);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  function onUploadCompleted(res) {
    console.log("Upload Completed");
    console.log(res);
    setImage(res);
  }

  function onHandleClick() {
    console.log("Classify!");
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
          <ClassOptions />
        </div>
        <p>{apolloData && apolloData.info}</p>
      </Grid>
    </Layout>
  );
}
