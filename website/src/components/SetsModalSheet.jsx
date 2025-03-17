import React, { useEffect, useState } from "react";
import styles from "../styles/SetsModalSheet.module.css";
import Set from "./Set";
import { BASE_API_URL } from "../utils/constants";
import { postSets } from "../api/exercise";

function SetsModalSheet({ currentDate, selectedExercise, hideModal, reset }) {
  const [sets, setSets] = useState({
  });

  const addSet = () => {
    const newOrder = Object.keys(sets).length + 1;
    const newSet = { reps: 0, weight: 0, date: currentDate, unit: "kg", order: newOrder };
    console.log(newOrder)

    setSets((prevSets) => ({
      ...prevSets,
      [newOrder]: newSet,
    }));
  };

  const createSets = async () => {
    try {
      const response = await postSets(sets, selectedExercise.id)
      console.log(response)
    } catch (e) {
      console.log(e)
    } finally {
      hideModal()
    }
  }

  useEffect(() => {
    if (reset) {
      setSets({})
    }
  }, [reset])

  return (
    <>
      <div className={styles.container}>
        <div className={styles.illustration}>
          <img
            src={`${BASE_API_URL}/images/illustrations/${selectedExercise.img}`}
          />
          <p className={styles.exercise}>{selectedExercise.name}</p>
        </div>
        <div>
          <div className={styles.bar}>
            <h2 className={styles.header}>Sets & Reps</h2>
            <button onClick={createSets}>&gt;</button>
          </div>
          <div className={styles.sets}>
            {Object.entries(sets).map(([order, set]) => (
              <Set key={order} order={order} sets={sets} setSets={setSets} />
            ))}
            <div onClick={addSet} className={styles.setContainer}>
              <p className={styles.add}>+</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SetsModalSheet;
