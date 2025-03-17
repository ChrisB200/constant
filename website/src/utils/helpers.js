export function capitaliseFirstLetter(val) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}

export function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed, so add 1
  const day = String(date.getDate()).padStart(2, '0'); // Ensure day is always two digits

  return `${year}-${month}-${day}`;
}

export function exerciseById(exercises, id) {
  for (let e in exercises) {
    if (e.id == id) {
      return e;
    }
  }
  return null;
}
