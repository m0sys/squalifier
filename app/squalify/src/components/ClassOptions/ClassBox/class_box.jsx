import React from 'react';
import PropTypes from 'prop-types';

import classBoxStyles from "./class_box.module.scss";


const ClassBox = (props) => {

  const { classType } = props;


  return (
    <div className={classBoxStyles.classBox}>
      <h3>{classType}</h3>
    </div>
  );
};


ClassBox.propTypes = {
  classType: PropTypes.string.isRequired,
}


export default ClassBox;