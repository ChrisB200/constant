import React from "react";
import { capitaliseFirstLetter } from "../utils/helpers";
import HomeSetCard from "./HomeSetCard";
import styles from "../styles/MuscleCategory.module.css"

function MuscleCategory({ muscle, exercises, sets }) {
  return exercises.length !== 0 ? (
    <>
      <h2 className={styles.header}>{capitaliseFirstLetter(muscle)}</h2>
      <div className={styles.exercises}>
        {exercises.map((exercise) => (
          <HomeSetCard key={exercise.id} exercise={exercise} sets={sets}/>
        ))}
      </div>
    </>
  ) : (
    ""
  );
}

export default MuscleCategory;
