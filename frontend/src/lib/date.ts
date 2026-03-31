function toLocalDateString(value: Date) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function getTodayDateString() {
  return toLocalDateString(new Date());
}

export function getWeekStartString(referenceDate = new Date()) {
  const value = new Date(referenceDate);
  const day = value.getDay();
  const diff = (day + 6) % 7;
  value.setDate(value.getDate() - diff);
  return toLocalDateString(value);
}

export function formatShortDate(value: string) {
  return new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric" }).format(new Date(value));
}

export function formatWeekday(value: string) {
  return new Intl.DateTimeFormat("en-US", { weekday: "short" }).format(new Date(value));
}
