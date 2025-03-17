import React, { useEffect, useState } from "react";
import styles from "../styles/HomeSets.module.css";
import { useExercises, useSets } from "../hooks/context";
import MuscleCategory from "./MuscleCategory";
import { exerciseById } from "../utils/helpers";

function HomeSets() {
  const {sets} = useSets()
  const {exercises} = useExercises()
  const [categories, setCategories] = useState({
    chest: [],
    abdominals: [],
    back: [],
    biceps: [],
    calves: [],
    legs: [],
    shoulders: [],
  });

  useEffect(() => {
    if (exercises.length === 0 || sets.length === 0) return;
    const reset_categories = {
      chest: [],
      abdominals: [],
      back: [],
      biceps: [],
      calves: [],
      legs: [],
      shoulders: [],
    }

    setCategories(reset_categories)

    sets.forEach((set) => {
      const exercise = exercises.find((e) => e.id === set.exercise_id);
      if (exercise) {
        setCategories((prevCategories) => ({
          ...prevCategories,
          [exercise.main_muscle.toLowerCase()]: [
            ...(prevCategories[exercise.main_muscle.toLowerCase()] || []),
            exercise,
          ],
        }));
      }
    });
  }, [sets, exercises]);
  return (
    <>
      <div className={styles.container}>
        {Object.entries(categories).map(([muscle, exercises]) => (
          <div key={muscle}>
            <MuscleCategory muscle={muscle} exercises={exercises} sets={sets} />
          </div>
        ))}
      </div>
    </>
  );
}

export default HomeSets;
