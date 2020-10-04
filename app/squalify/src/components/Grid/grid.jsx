import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

import gridStyles from "./grid.module.scss";

const Container = props => {
  const { children, hasMinHeight, center, id } = props;

  const classes = buildClasses();

  function buildClasses() {
    return classNames({
      [gridStyles.grid]: true,
      [gridStyles.hasMinHeight]: hasMinHeight,
      [gridStyles.center]: center,
    });
  }

  return (
    <div id={id} className={classes}>
      {children}
    </div>
  );
};

Container.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
};

export default Container;
