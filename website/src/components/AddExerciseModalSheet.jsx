import React, { useEffect, useState } from "react";
import styles from "../styles/AddExerciseModalSheet.module.css";
import { useExercises } from "../hooks/context";
import ExerciseCard from "./ExerciseCard";

function AddExerciseModalSheet({ setShow, setSelectedExercise, reset}) {
  const { exercises } = useExercises();
  const [filteredExercises, setFilteredExercises] = useState([]);

  const handleChange = async (e) => {
    const search = e.target.value;

    if (search !== "") {
      const filteredExercises = exercises.filter((ex) =>
        ex.name.toLowerCase().includes(search.toLowerCase()),
      );
      setFilteredExercises(filteredExercises);
    }
  };

  const handleClicked = (exercise) => {
    setShow("sets")
    setSelectedExercise(exercise)
  };

  useEffect(() => {
    setFilteredExercises(exercises);
  }, [exercises]);

  useEffect(() => {
    if (reset) {
      setSelectedExercise(null);
      setFilteredExercises([]);
    }
  }, [reset])

  return (
    <>
      <div className={styles.container}>
        <div className={styles.searchInfo}>
          <h2>Search Exercise</h2>
          <input
            name="search"
            onChange={handleChange}
            type="search"
            placeholder="Search"
          />
          <p>
            <span className={styles.amount}>{exercises.length}</span> exercises
          </p>
        </div>
        <div className={styles.exercises}>
          {filteredExercises.map((exercise) => (
            <ExerciseCard key={exercise.id} onClick={handleClicked} exercise={exercise} />
          ))}
        </div>
      </div>
    </>
  );
}

export default AddExerciseModalSheet;
