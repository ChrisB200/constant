import React from "react";
import styles from "../styles/DateSwitcher.module.css"

const ordinal = (n) => {
  const s = ['th', 'st', 'nd', 'rd'];
  const m = n % 100;
  return n + (s[(m - 20) % 10] || s[m] || s[0]);
};

function DateSwitcher({date, setDate}) {
  const dayName = date.toLocaleString(undefined, {
    weekday: "long"
  })

  const dayNum = date.toLocaleString(undefined, {
    day: "numeric"
  })

  const month = date.toLocaleString(undefined, {
    month: "long"
  })

  const prevDate = () => {
    const newDate = new Date(date)
    newDate.setDate(newDate.getDate() - 1)
    setDate(newDate)
  }

  const nextDate = () => {
    const newDate = new Date(date)
    newDate.setDate(newDate.getDate() + 1)
    setDate(newDate)
  }
  
  return (
    <div>
      <div className={styles.semicircle}></div>
      <div className={styles.container}>
        <button className={styles.switch} onClick={prevDate}>&lt;</button>
        <div className={styles.date}>
          <h3 className={styles.name}>{dayName}</h3>
          <h2 className={styles.month}>{`${ordinal(dayNum)} ${month}`}</h2>
        </div>
        <button className={styles.switch} onClick={nextDate}>&gt;</button>
      </div>
    </div>
  )
}

export default DateSwitcher
