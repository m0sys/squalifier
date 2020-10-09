import React from "react";

import Hero from "../components/Hero/hero";
import Layout from "../components/Layout/layout";

import "../styles/main.scss";

export default function Home() {
  return (
    <Layout>
      <Hero />
    </Layout>
  );
}
