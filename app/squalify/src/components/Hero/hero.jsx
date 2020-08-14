import React from 'react';
import { useStaticQuery, graphql, navigate } from "gatsby";
import Img from "gatsby-image";

import Container from "../Container/container";
import Button from "../Button/button";

import heroStyles from "./hero.module.scss";


const Hero = () => {
  const data = useHeroImage()

  function useHeroImage() {
    return useStaticQuery(graphql`
    query {
      file(relativePath: {
        eq: "hero.jpg"
      })
      {
        childImageSharp {
          fluid(maxWidth: 1500, quality: 100) {
            ...GatsbyImageSharpFluid
            
          }
        }
      }
    }
    `)
  }

  function handlOnClick() {
    navigate('/classification')
  }


  return (
  <main className={heroStyles.hero}>
    <Container>
      <h3>
        Welcome to <span>Squalify</span>
      </h3>
      <h2>
        The First AI Powered <span>Front VS Back Squat Classifier!</span>
      </h2>
      <div className={heroStyles.heroImgContainer}>
        <Img className={heroStyles.heroImg}  fluid={data.file.childImageSharp.fluid}/>
        <p className="meta-text">
          Photo by{" "}
          <a href="https://unsplash.com/@amandhakal?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">
            Aman Dhakal
          </a>{" "}
          on{" "}
          <a href="https://unsplash.com/?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">
            Unsplash
          </a>
        </p>
      </div>
      <Button text="Initiate Classification" onClick={handlOnClick} />
    </Container>
  </main>
  );
};


export default Hero;