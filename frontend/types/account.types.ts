import { z } from "zod";

export const UserSchema = z.object({
    userId: z.string().uuid("Invalid user ID"),
    username: z.string(),
    email: z.string().email("Invalid email address"),
});

export const SignupRequestSchema = z.object({
    username: z.string().min(3, "Username must be at least 3 characters"),
    email: z.string().email("Invalid email address"),
    password: z.string().min(8, "Password must be at least 8 characters"),
});

export const SigninRequestSchema = z.object({
    identifier: z.string().min(1, "Identifier is required"),
    password: z.string().min(1, "Password is required"),
});

export type User = z.infer<typeof UserSchema>;
export type SignupRequest = z.infer<typeof SignupRequestSchema>;
export type SigninRequest = z.infer<typeof SigninRequestSchema>;
