import React from "react";
import styles from "../styles/ExerciseCard.module.css"
import { BASE_API_URL } from "../utils/constants";

function ExerciseCard({ exercise, onClick }) {
  return (<>
    <div className={styles.container} onClick={() => onClick(exercise)}>
      <h3>{exercise.name}</h3>
      <div className={styles.illustration}>
        <img src={`${BASE_API_URL}/images/illustrations/${exercise.img}`}/>
      </div>
      <p>{exercise.main_muscle}</p>
    </div>
  </>)
}

export default ExerciseCard;
