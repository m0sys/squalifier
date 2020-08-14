import React from 'react';
import PropTypes from 'prop-types';

import containerStyles from "./container.module.scss";


const Container = (props) => {

  const { children } = props;


  return (
    <div className={containerStyles.container}>
      {children}
    </div>
  );
};


Container.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]).isRequired
};


export default Container;