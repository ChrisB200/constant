import { createContext, useEffect, useState } from "react"
import { fetchExercises } from "../api/exercise";


export const ExerciseContext = createContext(null);

export const ExerciseProvider = ({ children }) => {
  const [exercises, setExercises] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadExercises = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchExercises();
      setExercises(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => { 
    loadExercises();
  }, [])

  return (
    <ExerciseContext.Provider
      value={{ exercises, setExercises, isLoading, setIsLoading, error}}
    >
      {children}
    </ExerciseContext.Provider>
  )
}
