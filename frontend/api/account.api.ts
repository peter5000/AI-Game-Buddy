import { SigninRequest, SignupRequest, User } from "@/types/account.types";

import { apiRequest } from "./index.api";

export async function signupUser(data: SignupRequest): Promise<User> {
    return apiRequest<User>("/accounts/register", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export async function signinUser(data: SigninRequest): Promise<User> {
    return apiRequest<User>("/accounts/login", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export async function signoutUser(): Promise<void> {
    await apiRequest<void>("/accounts/logout", {
        method: "POST",
    });
}

export async function refreshToken(): Promise<void> {
    await apiRequest<void>("/accounts/refresh", {
        method: "POST",
    });
}

export async function deleteUser(): Promise<void> {
    await apiRequest<void>("/accounts/delete", {
        method: "DELETE",
    });
}

export async function getAuthStatus(): Promise<{ userId: string }> {
    return apiRequest<{ userId: string }>("/accounts/status", {
        method: "GET",
    });
}

export async function getCurrentUser(): Promise<User> {
    return apiRequest<User>("/accounts/user", {
        method: "GET",
    });
}
