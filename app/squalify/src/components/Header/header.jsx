import React from 'react';
import { Link } from "gatsby"

import headerStyles from "./header.module.scss";


const Header = () => {


  return (
      <header>
        <div className={headerStyles.statusBar}></div>
        <div className={headerStyles.headerContent}>
          <h3 className={headerStyles.logo}><Link to="/">Squalify</Link></h3>
        </div>
      </header>
  );
};


export default Header;