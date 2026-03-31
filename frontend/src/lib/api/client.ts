import { env } from "@/lib/env";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(message: string, status: number, detail: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  query?: Record<string, string | number | boolean | null | undefined>;
  headers?: HeadersInit;
};

function buildUrl(path: string, query?: RequestOptions["query"]) {
  const url = new URL(`${env.apiBaseUrl}${path.startsWith("/") ? path : `/${path}`}`);
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, String(value));
      }
    }
  }
  return url.toString();
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(buildUrl(path, options.query), {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    let detail: unknown = null;
    try {
      detail = await response.json();
    } catch {
      detail = await response.text();
    }
    const message =
      typeof detail === "object" && detail !== null && "detail" in detail
        ? String((detail as { detail: unknown }).detail)
        : `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status, detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const apiClient = {
  get: <T>(path: string, query?: RequestOptions["query"]) => request<T>(path, { query }),
  post: <T, B = unknown>(path: string, body?: B, query?: RequestOptions["query"]) => request<T>(path, { method: "POST", body, query }),
  put: <T, B = unknown>(path: string, body?: B, query?: RequestOptions["query"]) => request<T>(path, { method: "PUT", body, query }),
  patch: <T, B = unknown>(path: string, body?: B, query?: RequestOptions["query"]) => request<T>(path, { method: "PATCH", body, query }),
  delete: <T>(path: string, query?: RequestOptions["query"]) => request<T>(path, { method: "DELETE", query }),
  uploadForm: async <T>(path: string, formData: FormData, query?: RequestOptions["query"]) => {
    const response = await fetch(buildUrl(path, query), {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let detail: unknown = null;
      try {
        detail = await response.json();
      } catch {
        detail = await response.text();
      }
      const message =
        typeof detail === "object" && detail !== null && "detail" in detail
          ? String((detail as { detail: unknown }).detail)
          : `Request failed with status ${response.status}`;
      throw new ApiError(message, response.status, detail);
    }

    return (await response.json()) as T;
  },
};
