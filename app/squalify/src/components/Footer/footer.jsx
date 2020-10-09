import React from "react";

import Grid from "../Grid/grid";
import footerStyles from "./footer.module.scss";

const Footer = props => {
  const today = new Date();

  return (
    <footer>
      <Grid>
        <p className={footerStyles.cc}>
          Copyright © {today.getFullYear()} Squalify.dev. All Rights Reserved
        </p>
      </Grid>
    </footer>
  );
};

export default Footer;
