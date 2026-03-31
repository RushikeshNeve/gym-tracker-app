const fallbackApiBaseUrl = import.meta.env.DEV ? "http://localhost:8000/api/v1" : "/api/v1";

export const env = {
  apiBaseUrl: (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "") || fallbackApiBaseUrl,
};
