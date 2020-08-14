import React from 'react';

import ClassBox from "./ClassBox/class_box";

import classOptionsStyles from "./class_options.module.scss";


const ClassOptions = (props) => {


  return (
    <div className={classOptionsStyles.classOptions}>
      <ClassBox className={classOptionsStyles.classOne} classType="Front Squat"/>
      <ClassBox className={classOptionsStyles.classTwo} classType="Back Squat"/>
    </div>
  );
};




export default ClassOptions;