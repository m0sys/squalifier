import React, {useState, useEffect } from 'react';
import PropTypes from 'prop-types';


const NotFoundPage = (props) => {
  const [count, setCount] = useState(0);


  return (
    <div>
      <h3>Welcome to 404!</h3>
      <p>You clicked {count} times</p>
    </div>
  );
};


export default NotFoundPage;