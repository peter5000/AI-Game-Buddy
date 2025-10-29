"use client";

import type React from "react";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
import { Gamepad2 } from "lucide-react";

import { signupUser } from "@/api/account.api";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useAuth } from "@/hooks/use-auth";
import { tryCatch } from "@/lib/utils";

export default function SignUpPage() {
    const { isAuthenticated, isLoading: isAuthLoading } = useAuth({
        redirectIfAuthed: true,
    });
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        agreeToTerms: false,
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

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (isLoading) return;

        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setIsLoading(true);
        setError(null); // Clear previous errors on a new submission

        const [user, error] = await tryCatch(
            signupUser({
                username: formData.username,
                email: formData.email,
                password: formData.password,
            })
        );

        setIsLoading(false);

        // Handle the error case
        if (error) {
            setError(error.message);
            return;
        }

        if (user) {
            queryClient.setQueryData(["user"], user);
            router.push("/");
        }
    };

    const handleInputChange = (field: string, value: string | boolean) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
            <Card className="w-full max-w-md">
                <CardHeader className="text-center">
                    <div className="flex justify-center mb-4">
                        <Gamepad2 className="h-12 w-12 text-purple-600" />
                    </div>
                    <CardTitle className="text-2xl">
                        Join AI Gaming Friend
                    </CardTitle>
                    <CardDescription>
                        Create your account and start playing with AI companions
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="username">Username</Label>
                            <Input
                                id="username"
                                placeholder="Choose a username"
                                value={formData.username}
                                onChange={(e) =>
                                    handleInputChange(
                                        "username",
                                        e.target.value
                                    )
                                }
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="Enter your email"
                                value={formData.email}
                                onChange={(e) =>
                                    handleInputChange("email", e.target.value)
                                }
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                placeholder="Create a password"
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
                        <div className="space-y-2">
                            <Label htmlFor="confirmPassword">
                                Confirm Password
                            </Label>
                            <Input
                                id="confirmPassword"
                                type="password"
                                placeholder="Confirm your password"
                                value={formData.confirmPassword}
                                onChange={(e) =>
                                    handleInputChange(
                                        "confirmPassword",
                                        e.target.value
                                    )
                                }
                                required
                            />
                        </div>
                        <div className="flex items-center space-x-2">
                            <Checkbox
                                id="terms"
                                checked={formData.agreeToTerms}
                                onCheckedChange={(checked) =>
                                    handleInputChange(
                                        "agreeToTerms",
                                        checked as boolean
                                    )
                                }
                            />
                            <Label htmlFor="terms" className="text-sm">
                                I agree to the{" "}
                                <Link
                                    href="/terms"
                                    className="text-purple-600 hover:underline"
                                >
                                    Terms of Service
                                </Link>{" "}
                                and{" "}
                                <Link
                                    href="/privacy"
                                    className="text-purple-600 hover:underline"
                                >
                                    Privacy Policy
                                </Link>
                            </Label>
                        </div>
                        {error && (
                            <div className="text-red-500 text-sm text-center mb-4">
                                {error}
                            </div>
                        )}
                        <Button
                            type="submit"
                            className="w-full"
                            disabled={isLoading || !formData.agreeToTerms}
                        >
                            {isLoading
                                ? "Creating Account..."
                                : "Create Account"}
                        </Button>
                    </form>
                    <Separator />
                    <div className="text-center text-sm">
                        Already have an account?{" "}
                        <Link
                            href="/accounts/signin"
                            className="text-purple-600 hover:underline"
                        >
                            Sign in
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
