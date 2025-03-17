import React, { useEffect, useState } from "react";
import DateSwitcher from "../components/DateSwitcher";
import Navbar from "../components/Navbar";
import styles from "../styles/HomePage.module.css";
import AddExerciseModalSheet from "../components/AddExerciseModalSheet";
import ModalSheet from "../components/ModalSheet";
import SetsModalSheet from "../components/SetsModalSheet";
import { SetProvider } from "../contexts/SetContext";
import HomeSets from "../components/HomeSets";

function Home() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [reset, setReset] = useState(false);
  const [isHidden, setIsHidden] = useState(true);
  const [show, setShow] = useState("add");
  const [selectedExercise, setSelectedExercise] = useState(null);

  const showModal = () => {
    setIsHidden(false);
  };

  const hideModal = () => {
    setReset(true);
  }

  useEffect(() => {
    if (reset) {
      setShow("add")
      setIsHidden(true);
      setSelectedExercise(null);
      setReset(false)
    }
  }, [reset])

  useEffect(() => {
    
  })

  return (
    <>
      <DateSwitcher date={currentDate} setDate={setCurrentDate}></DateSwitcher>
      <SetProvider currentDate={currentDate}>
        <HomeSets/>
      </SetProvider>
      <ModalSheet show={show} isHidden={isHidden} setIsHidden={setIsHidden} hideModal={hideModal}>
        <AddExerciseModalSheet
          setSelectedExercise={setSelectedExercise}
          setShow={setShow}
          name="add"
          reset={reset}
        />
        <SetsModalSheet
          selectedExercise={selectedExercise}
          setIsHidden={setIsHidden}
          name="sets"
          currentDate={currentDate}
          reset={reset}
          hideModal={hideModal}
        />
      </ModalSheet>
      <div className={styles.fixed}>
        <button className={styles.btnadd} onClick={showModal}>
          +
        </button>
        <Navbar />
      </div>
    </>
  );
}

export default Home;
