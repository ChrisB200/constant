import { createContext, useEffect, useState } from "react"
import { fetchSetsByDate } from "../api/exercise";


export const SetContext = createContext(null);

export const SetProvider = ({ children, currentDate }) => {
  const [sets, setSets] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadSets = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchSetsByDate(currentDate);
      setSets(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => { 
    loadSets();
  }, [currentDate])

  return (
    <SetContext.Provider
      value={{ sets, setSets, isLoading, setIsLoading, error}}
    >
      {children}
    </SetContext.Provider>
  )
}

