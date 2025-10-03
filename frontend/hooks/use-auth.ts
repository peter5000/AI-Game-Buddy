"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { getUser, signoutUser } from "@/api/account.api";

interface UseAuthOptions {
    requireAuth?: boolean;
    redirectIfAuthed?: boolean;
    redirectUrl?: string;
}

export function useAuth({
    requireAuth = false,
    redirectIfAuthed = false,
    redirectUrl,
}: UseAuthOptions = {}) {
    const router = useRouter();
    const queryClient = useQueryClient();

    const {
        data: user,
        isLoading,
        isError,
    } = useQuery({
        queryKey: ["user"],
        queryFn: getUser,
        staleTime: 5 * 60 * 1000,
        retry: false,
    });

    const isAuthenticated = !!user && !isError;

    const logout = async () => {
        await signoutUser();
        queryClient.resetQueries({ queryKey: ["user"] });
    };

    useEffect(() => {
        if (isLoading) return;

        if (requireAuth && !isAuthenticated) {
            router.push(redirectUrl || "/accounts/signin");
        }

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

    return { isAuthenticated, user, isLoading, logout };
}
