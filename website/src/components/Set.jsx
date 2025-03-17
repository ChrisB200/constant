import React, { useEffect, useState } from "react";
import styles from "../styles/Set.module.css";

function Set({ order, sets, setSets }) {
  const [set, setSet] = useState(sets[order] || { reps: "", weight: "" });

const handleClick = (e) => {
  const [operation, name] = e.target.name.split("-");

  setSet((prev) => {
    const newValue = operation === "prev" ? prev[name] - 1 : prev[name] + 1;
    return { ...prev, [name]: newValue };
  });

  setSets((prevSets) => ({
    ...prevSets,
    [order]: {
      ...prevSets[order],
      [name]: operation === "prev" ? prevSets[order][name] - 1 : prevSets[order][name] + 1,
    },
  }));
};


  return (
    <div className={styles.container}>
      <p className={styles.x}>X</p>
      <p className={styles.order}>{order}</p>
      <div className={styles.row}>
        <button name="prev-reps" onClick={handleClick} className={styles.arrow}>&lt;</button>
        <p className={styles.reps}>{set.reps}</p>
        <button name="next-reps" onClick={handleClick} className={styles.arrow}>&gt;</button>
      </div>

      <div className={styles.row}>
        <button name="prev-weight" onClick={handleClick} className={styles.arrow}>&lt;</button>
        <p>{set.weight}kg</p>
        <button name="next-weight" onClick={handleClick} className={styles.arrow}>&gt;</button>
      </div>
    </div>
  );
}

export default Set;
