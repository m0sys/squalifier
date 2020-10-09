import React from "react";
import Header from "../Header/header";
import Footer from "../Footer/footer";

const Layout = props => {
  const { children } = props;

  return (
    <React.Fragment>
      <Header />
      {children}
      <Footer />
    </React.Fragment>
  );
};

export default Layout;
