"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Bell, Gamepad2, LogOut, Menu, Settings, User, X } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useAuth } from "@/hooks/use-auth";

export function Navbar() {
    const { user, isAuthenticated, isLoading, logout } = useAuth();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const router = useRouter();

    const handleSignOut = async () => {
        await logout();
        router.push("/");
    };

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

    return (
        <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2">
                        <Gamepad2
                            className="h-8 w-8 text-purple-600"
                            suppressHydrationWarning
                        />
                        <span className="text-xl font-bold text-gray-900">
                            AI Gaming Friend
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        <Link
                            href="/games"
                            className="text-gray-700 hover:text-purple-600 transition-colors"
                        >
                            Games
                        </Link>
                        <Link
                            href="/ai-friends"
                            className="text-gray-700 hover:text-purple-600 transition-colors"
                        >
                            AI Friends
                        </Link>
                        <Link
                            href="/get-started"
                            className="text-gray-700 hover:text-purple-600 transition-colors"
                        >
                            Get Started
                        </Link>
                        <Link
                            href="/docs"
                            className="text-gray-700 hover:text-purple-600 transition-colors"
                        >
                            Documentation
                        </Link>
                    </div>

                    {/* User Actions */}
                    <div className="hidden md:flex items-center space-x-4">
                        {isLoading ? (
                            <div className="h-8 w-32 bg-gray-200 rounded-md animate-pulse" />
                        ) : isAuthenticated && user ? (
                            <div className="flex items-center space-x-3">
                                <Button variant="ghost" size="sm">
                                    <Bell
                                        className="h-4 w-4"
                                        suppressHydrationWarning
                                    />
                                </Button>
                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Avatar className="cursor-pointer">
                                            <AvatarFallback>
                                                {user.username
                                                    .charAt(0)
                                                    .toUpperCase()}
                                            </AvatarFallback>
                                        </Avatar>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent
                                        align="end"
                                        className="w-56"
                                    >
                                        <DropdownMenuItem asChild>
                                            <Link
                                                href="/profile"
                                                className="flex items-center"
                                            >
                                                <User className="mr-2 h-4 w-4" />
                                                Profile
                                            </Link>
                                        </DropdownMenuItem>
                                        <DropdownMenuItem asChild>
                                            <Link
                                                href="/settings"
                                                className="flex items-center"
                                            >
                                                <Settings className="mr-2 h-4 w-4" />
                                                Settings
                                            </Link>
                                        </DropdownMenuItem>
                                        <DropdownMenuSeparator />
                                        <DropdownMenuItem
                                            onClick={handleSignOut}
                                        >
                                            <LogOut className="mr-2 h-4 w-4" />
                                            Sign Out
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </div>
                        ) : (
                            <div className="flex items-center space-x-3">
                                <Link href="/accounts/signin">
                                    <Button variant="ghost">Sign In</Button>
                                </Link>
                                <Link href="/accounts/signup">
                                    <Button>Sign Up</Button>
                                </Link>
                            </div>
                        )}
                    </div>

                    {/* Mobile menu button */}
                    <div className="md:hidden">
                        <Button variant="ghost" size="sm" onClick={toggleMenu}>
                            {isMenuOpen ? (
                                <X className="h-6 w-6" />
                            ) : (
                                <Menu className="h-6 w-6" />
                            )}
                        </Button>
                    </div>
                </div>

                {/* Mobile Navigation */}
                {isMenuOpen && (
                    <div className="md:hidden py-4 border-t">
                        <div className="flex flex-col space-y-3">
                            {/* mobile links can stay as before */}
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
}
