"use client";

import type React from "react";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
import { Gamepad2 } from "lucide-react";

import { signinUser } from "@/api/account.api";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useAuth } from "@/hooks/use-auth";
import { tryCatch } from "@/lib/utils";

export default function SignInPage() {
    const { isAuthenticated, isLoading: isAuthLoading } = useAuth({
        redirectIfAuthed: true,
    });
    // Consolidated state for form fields
    const [formData, setFormData] = useState({
        identifier: "",
        password: "",
    });
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
    const queryClient = useQueryClient();

    if (isAuthLoading || isAuthenticated) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-600"></div>
            </div>
        );
    }

    // Single handler for all text input changes
    const handleInputChange = (field: string, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (isLoading) return;

        setIsLoading(true);
        setError(null);

        const [user, error] = await tryCatch(
            signinUser({
                identifier: formData.identifier,
                password: formData.password,
            })
        );

        setIsLoading(false);

        if (error) {
            setError(error.message);
            return;
        }

        if (user) {
            queryClient.setQueryData(["user"], user);
            router.push("/");
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
            <Card className="w-full max-w-md">
                <CardHeader className="text-center">
                    <div className="flex justify-center mb-4">
                        <Gamepad2 className="h-12 w-12 text-purple-600" />
                    </div>
                    <CardTitle className="text-2xl">Welcome Back</CardTitle>
                    <CardDescription>Sign in to your account</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="identifier">
                                Username or Email
                            </Label>
                            <Input
                                id="identifier"
                                type="text"
                                placeholder="Enter your username or email"
                                value={formData.identifier}
                                onChange={(e) =>
                                    handleInputChange(
                                        "identifier",
                                        e.target.value
                                    )
                                }
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                placeholder="Enter your password"
                                value={formData.password}
                                onChange={(e) =>
                                    handleInputChange(
                                        "password",
                                        e.target.value
                                    )
                                }
                                required
                            />
                        </div>
                        {error && (
                            <div className="text-red-500 text-sm text-center mb-4">
                                {error}
                            </div>
                        )}
                        <Button
                            type="submit"
                            className="w-full"
                            disabled={isLoading}
                        >
                            {isLoading ? "Signing In..." : "Sign In"}
                        </Button>
                    </form>

                    <div className="text-center">
                        <Link
                            href="/accounts/forgot-password"
                            className="text-sm text-purple-600 hover:underline"
                        >
                            Forgot your password?
                        </Link>
                    </div>

                    <Separator />

                    <div className="text-center text-sm">
                        {"Don't have an account? "}
                        <Link
                            href="/accounts/signup"
                            className="text-purple-600 hover:underline"
                        >
                            Sign up
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
