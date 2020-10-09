import React from "react";

import ClassBox from "./ClassBox/class_box";

import classOptionsStyles from "./class_options.module.scss";

const ClassOptions = props => {
  const { category } = props;

  return (
    <div className={classOptionsStyles.classOptions}>
      <ClassBox
        on={category == 0}
        className={classOptionsStyles.classOne}
        classType="Front Squat"
      />
      <ClassBox
        on={category == 1}
        className={classOptionsStyles.classTwo}
        classType="Back Squat"
      />
    </div>
  );
};

export default ClassOptions;
