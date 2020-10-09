import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

import classBoxStyles from "./class_box.module.scss";

const ClassBox = props => {
  const { classType, on } = props;

  const classes = buildClasses();

  function buildClasses() {
    return classNames({
      [classBoxStyles.classBox]: true,
      [classBoxStyles.blueBox]: on,
    });
  }

  return (
    <div className={classes}>
      <h3>{classType}</h3>
    </div>
  );
};

ClassBox.propTypes = {
  classType: PropTypes.string.isRequired,
};

export default ClassBox;
