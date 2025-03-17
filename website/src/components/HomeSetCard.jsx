import React, { useEffect, useState } from "react";
import styles from "../styles/HomeSetCard.module.css"
import dumbbell from "../assets/icons/dumbbell.svg"
import { BASE_API_URL } from "../utils/constants";

function HomeSetCard({exercise, sets}) {
  const [exerciseSets, setExerciseSets] = useState([])

  const getExerciseSets = () => {
    let foundSets = []

    console.log(sets)
    for (let set in sets) {
      if (sets[set].exercise_id === exercise.id) {
        foundSets.push(sets[set])
      }
    }
    setExerciseSets(foundSets)
  }

  useEffect(() => {
    getExerciseSets()
  }, [exercise, sets])

  return (<>
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{exercise.name}</h3>
        <button>X</button>
      </div>
      <div className={styles.illustration}>
        <img src={`${BASE_API_URL}/images/illustrations/${exercise.img}`}/>
      </div>
      <div className={styles.info}>
        <button>{exerciseSets.length} Sets</button>
        <div>
          <img src={dumbbell}/>
        </div>
      </div>
    </div>
  </>)
}

export default HomeSetCard;
