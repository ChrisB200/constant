import { useState } from "react";
import styles from "../styles/LoginPage.module.css"
import { Link, useNavigate } from "react-router-dom";
import authService from "../api/authService"

function Login() {
  // allows for page redirection
  const navigate = useNavigate()

  // stores the error state
  const [error, setError] = useState(null)

  // stores the form values
  const [values, setValues] = useState({
    email: "",
    password: "",
  });

  // every time something is typed
  const handleChange = (e) => {
    setError(null);
    // sets the corresponding value in object based on input
    setValues({...values, [e.target.name]: e.target.value})
  }

  const handleSubmit = (e) => {
    // prevents form from refreshing the page
    e.preventDefault()
    
    // we then get form from event and check if its valid
    const form = e.target;
    const isValid = form.checkValidity();

    if (!isValid) {
      setError("invalid-form");
    } else {
        // try to login else set error state
        authService.login(values.email, values.password)
          .then(() => {
            navigate("/")
          })
          .catch((error) => {
            if (error.status === 401) {
              setError("invalid-credentials");
            } else if (error.status === 500) {
              setError("server-error");
            } else if (error.status === 404) {
              setError("connection-error");
            }
        })
      }
    }

  // here i change the class names using ternary statements
  // expression ? condition1 : condition2
  // same as if (expression) then condition1 else conditon2
  // this allows for classes to be toggled based on error state
  // i also use the python f statements but the equivalent in js
  // (python) f"my name is {name}"
  // (js) `my name is ${name}`
  return <>
    <div className={styles.container}>
      <form onSubmit={handleSubmit}>
        <h1>Log in</h1>
        <p className={`${styles.invalid} ${error != "invalid-credentials" ? "hide": ""}`}>The email or password is incorrect</p>
        <p className={`${styles.invalid} ${error != "server-error" ? "hide": ""}`}>There is an issue with our servers</p>
        <p className={`${styles.invalid} ${error != "connection-error" ? "hide": ""}`}>Unable to connect to servers</p>
        <div className={styles.row}>
          <label htmlFor="email">Email</label>
          <input required className={`${styles.input} ${error ? styles.error: ""}`} onChange={handleChange} name="email" type="email"/>
        </div>
        <div className={styles.row}>
          <label htmlFor="password">Password</label>
          <input required className={`${styles.input} ${error ? styles.error: ""}`} onChange={handleChange} name="password" type="password"/>
        </div>
        <hr/>
        <div className={styles.actions}>
          <button className={styles.create}>Log in</button>
          <p className={`${styles.invalid} ${error != "invalid-form" ? "hide": ""}`}>Please provide a valid email and password</p>
          <p>No account? <Link to="/signup" className={styles.clickable}>Create One</Link></p>
          <Link to="/forgot" className={styles.clickable}>Forgot Password</Link>
        </div>
      </form>
    </div>
  </>;
}

export default Login;

