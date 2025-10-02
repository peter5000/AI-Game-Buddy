"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";

import { getAuthStatus } from "@/api/account.api";

interface UseAuthOptions {
    // If true, redirects unauthenticated users to the login page.
    requireAuth?: boolean;
    // If true, redirects authenticated users away from the current page (e.g., login/signup).
    redirectIfAuthed?: boolean;
    // The URL to redirect to.
    redirectUrl?: string;
}

export function useAuth({
    requireAuth = false,
    redirectIfAuthed = false,
    redirectUrl,
}: UseAuthOptions = {}) {
    const router = useRouter();

    const { data, isLoading, isError } = useQuery({
        queryKey: ["authStatus"],
        queryFn: getAuthStatus,
        staleTime: 5 * 60 * 1000, // 5 minutes
        retry: false, // Important: prevent retrying on auth errors (401)
    });

    // The query is successful if the user has a valid token.
    const isAuthenticated = !!data && !isError;

    useEffect(() => {
        // Don't redirect while the auth status is still being determined
        if (isLoading) return;

        // If the route requires authentication and the user is not logged in, redirect.
        if (requireAuth && !isAuthenticated) {
            router.push(redirectUrl || "/accounts/signin");
        }

        // If the user is already authenticated, redirect away from auth pages (login/signup).
        if (redirectIfAuthed && isAuthenticated) {
            router.push(redirectUrl || "/");
        }
    }, [
        isLoading,
        isAuthenticated,
        requireAuth,
        redirectIfAuthed,
        redirectUrl,
        router,
    ]);

    return { isAuthenticated, user: data, isLoading };
}
