import { Link } from "react-router-dom";
import styles from "../styles/Navbar.module.css"

function Navbar() {
  return (
    <nav className={styles.container}>
      <div className={styles.links}>
        <Link to="/">Home</Link>
        <Link to="/exercises">Exercises</Link>
        <Link to="/analytics">Analytics</Link>
        <Link to="/settings">Settings</Link>
      </div>
    </nav>
  );
}

export default Navbar;
