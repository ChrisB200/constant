import React from "react";
import { BASE_API_URL } from "../utils/constants";
import styles from "../styles/ExerciseSet.module.css"

function ExerciseSet({ exercise }) {
  return (
    <>
      <div className= {styles.illustration}>
        <img src={`${BASE_API_URL}/images/illustrations/${exercise.img}`}/>
      </div>
      <div>

      </div>
    </>
  )
}

export default ExerciseSet;
