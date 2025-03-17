import { useContext } from "react"
import { ExerciseContext } from "../contexts/ExerciseContext"
import { SetContext } from "../contexts/SetContext";

export const useExercises = () => {
  const context = useContext(ExerciseContext);
  if (!context) {
    throw new Error("useExercises must be used within an ExerciseProvider");
  }
  return context;
}

export const useSets = () => {
  const context = useContext(SetContext);
  if (!context) {
    throw new Error("useSets must be used within a SetProvider")
  }
  return context;
}
