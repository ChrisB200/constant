import httpClient from "../utils/httpClient";
import { BASE_API_URL } from "../utils/constants";
import { formatDate } from "../utils/helpers";

export const fetchExercises = async () => {
  try {
    const response = await httpClient.get(`${BASE_API_URL}/exercises`);
    return response.data;
  } catch {
    console.error("Failed to fetch exercises", error);
    throw new Error("Failed to fetch exercises");
  }
};

export const postSets = async (sets, exercise_id) => {
  try {
    const response = await httpClient.post(`${BASE_API_URL}/sets`, {
      sets: sets,
      exercise_id: exercise_id
    })
    return response.data
  } catch {
    console.error("Failed to post sets")
    throw new Error("failed to post sets")
  }
}

export const fetchSetsByDate = async (date) => {
  try {
    const date_str = formatDate(date);
    const response = await httpClient.get(`${BASE_API_URL}/sets?date=${date_str}`)
    return response.data
  } catch (e) {
    console.error(e)
    throw new Error(e)
  }
}
