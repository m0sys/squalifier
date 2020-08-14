import React from 'react';
import PropTypes from 'prop-types';

import buttonStyles from "./button.module.scss";


const Button = (props) => {
  const { text, onClick } = props;


  return (
      <button className={buttonStyles.ctaBtn} onClick={() => onClick()}>
        <h3 className={buttonStyles.btnTxt}>{text}</h3>
      </button>
  );
};


Button.propTypes = {
  text: PropTypes.string.isRequired
};


export default Button;