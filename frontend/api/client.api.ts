import camelcaseKeys from "camelcase-keys";
import snakecaseKeys from "snakecase-keys";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export class ApiError extends Error {
    constructor(
        message: string,
        public status: number,
        public errors?: Record<string, string[]>
    ) {
        super(message);
        this.name = "ApiError";
    }
}

export async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const config: RequestInit = {
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
        credentials: "include",
        ...options,
    };

    // Convert outgoing request body to snake_case
    if (config.body && typeof config.body === "string") {
        const bodyObject = JSON.parse(config.body);
        config.body = JSON.stringify(snakecaseKeys(bodyObject, { deep: true }));
    }

    let response = await fetch(url, config);

    // If we get a 401 (unauthorized) and it's not a refresh request,
    // try to refresh the token automatically
    if (response.status === 401 && !endpoint.includes("/accounts/refresh")) {
        try {
            const refreshResponse = await fetch(
                `${API_BASE_URL}/accounts/refresh`,
                {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (refreshResponse.ok) {
                // Retry the original request with the new token
                response = await fetch(url, config);
            }
        } catch {
            // Refresh failed, redirect to login
            if (typeof window !== "undefined") {
                window.location.href = "/accounts/signin";
            }
            throw new ApiError("Session expired. Please sign in again.", 401);
        }
    }

    // Handle responses with no content
    if (response.status === 204) {
        return null as T;
    }

    const data = await response.json();

    if (!response.ok) {
        const errors = data.errors
            ? camelcaseKeys(data.errors, { deep: true })
            : undefined;
        throw new ApiError(
            data.detail || data.message || "An error occurred",
            response.status,
            errors
        );
    }

    // Convert incoming response data to camelCase before returning
    return camelcaseKeys(data, { deep: true });
}
