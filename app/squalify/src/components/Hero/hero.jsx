import React from "react";
import { useStaticQuery, graphql, navigate } from "gatsby";
import Img from "gatsby-image";

import Grid from "../Grid/grid";
import Button from "../Button/button";

import heroStyles from "./hero.module.scss";

const Hero = () => {
  const data = useHeroImage();

  function useHeroImage() {
    return useStaticQuery(graphql`
      query {
        file(relativePath: { eq: "hero.jpg" }) {
          childImageSharp {
            fluid(maxWidth: 1500, quality: 100) {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    `);
  }

  function handlOnClick() {
    navigate("/classification");
  }

  return (
    <main className={heroStyles.hero}>
      <Grid hasMinHeight center>
        <div className={heroStyles.top}>
          <h3 className={heroStyles.subhead}>
            Welcome to <span>Squalify</span>
          </h3>
          <h2 className={heroStyles.headline}>
            The First AI Powered <span>Front VS Back Squat Classifier!</span>
          </h2>
          <div className={heroStyles.cta}>
            <Button text="Initiate Classification" onClick={handlOnClick} />
          </div>
        </div>
        <div className={heroStyles.heroImgContainer}>
          <Img
            className={heroStyles.heroImg}
            fluid={data.file.childImageSharp.fluid}
          />
        </div>
      </Grid>
    </main>
  );
};

export default Hero;
