import React from "react";
import styles from "../styles/ModalSheet.module.css";

function ModalSheet({ children, show, isHidden, hideModal }) {
  const handleClose = () => {
    hideModal()
  }

  return (
    <>
      <div className={isHidden ? "hide" : ""}>
        <div className={styles.background} onClick={handleClose} />
        <div className={styles.container}>
            {React.Children.map(children, (child) => 
                child.props.name === show ? child : null
            )}
        </div>
      </div>
    </>
  );
}

export default ModalSheet;
