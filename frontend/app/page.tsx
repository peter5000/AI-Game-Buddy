import Link from "next/link";
import {
    ArrowRight,
    Gamepad2,
    MessageCircle,
    Search,
    Star,
    Users,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
            {/* Hero Section */}
            <section className="py-20 px-4 text-center">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-5xl font-bold text-gray-900 mb-6">
                        Your AI Gaming{" "}
                        <span className="text-purple-600">Companion</span>
                    </h1>
                    <p className="text-xl text-gray-600 mb-8">
                        Connect with AI friends, discover new games, and enhance
                        your gaming experience with intelligent companions.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/get-started">
                            <Button
                                size="lg"
                                className="bg-purple-600 hover:bg-purple-700"
                            >
                                Get Started
                                <ArrowRight
                                    className="ml-2 h-4 w-4"
                                    suppressHydrationWarning
                                />
                            </Button>
                        </Link>
                        <Link href="/games">
                            <Button variant="outline" size="lg">
                                Browse Games
                            </Button>
                        </Link>
                    </div>
                </div>
            </section>

            {/* Search Section */}
            <section className="py-12 px-4">
                <div className="max-w-6xl mx-auto">
                    <div className="flex flex-col md:flex-row gap-4 mb-8">
                        <div className="relative flex-1">
                            <Search
                                className="absolute left-3 top-3 h-4 w-4 text-gray-400"
                                suppressHydrationWarning
                            />
                            <Input
                                placeholder="Search games, rooms, or players..."
                                className="pl-10"
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button variant="outline">Filter</Button>
                            <Button variant="outline">Sort</Button>
                        </div>
                    </div>

                    {/* Featured Rooms */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                        <Card className="hover:shadow-lg transition-shadow">
                            <div className="rounded-lg overflow-hidden">
                                <div className="aspect-video bg-gradient-to-r from-purple-400 to-pink-400"></div>
                                <CardContent className="p-4">
                                    <h3 className="font-semibold mb-2">
                                        League of Legends Ranked
                                    </h3>
                                    <div className="flex justify-between items-center text-sm text-gray-600">
                                        <div className="flex items-center">
                                            <Users
                                                className="h-4 w-4 mr-1"
                                                suppressHydrationWarning
                                            />
                                            <span>4/5 players</span>
                                        </div>
                                        <Badge variant="secondary">
                                            Active
                                        </Badge>
                                    </div>
                                </CardContent>
                            </div>
                        </Card>

                        <Card className="hover:shadow-lg transition-shadow">
                            <div className="rounded-lg overflow-hidden">
                                <div className="aspect-video bg-gradient-to-r from-blue-400 to-cyan-400"></div>
                                <CardContent className="p-4">
                                    <h3 className="font-semibold mb-2">
                                        Valorant Casual
                                    </h3>
                                    <div className="flex justify-between items-center text-sm text-gray-600">
                                        <div className="flex items-center">
                                            <Users
                                                className="h-4 w-4 mr-1"
                                                suppressHydrationWarning
                                            />
                                            <span>3/5 players</span>
                                        </div>
                                        <Badge variant="secondary">
                                            Active
                                        </Badge>
                                    </div>
                                </CardContent>
                            </div>
                        </Card>

                        <Card className="hover:shadow-lg transition-shadow">
                            <div className="rounded-lg overflow-hidden">
                                <div className="aspect-video bg-gradient-to-r from-green-400 to-emerald-400"></div>
                                <CardContent className="p-4">
                                    <h3 className="font-semibold mb-2">
                                        Minecraft Creative
                                    </h3>
                                    <div className="flex justify-between items-center text-sm text-gray-600">
                                        <div className="flex items-center">
                                            <Users
                                                className="h-4 w-4 mr-1"
                                                suppressHydrationWarning
                                            />
                                            <span>2/8 players</span>
                                        </div>
                                        <Badge variant="secondary">
                                            Active
                                        </Badge>
                                    </div>
                                </CardContent>
                            </div>
                        </Card>

                        <Card className="hover:shadow-lg transition-shadow">
                            <div className="rounded-lg overflow-hidden">
                                <div className="aspect-video bg-gradient-to-r from-yellow-400 to-orange-400"></div>
                                <CardContent className="p-4">
                                    <h3 className="font-semibold mb-2">
                                        Apex Legends
                                    </h3>
                                    <div className="flex justify-between items-center text-sm text-gray-600">
                                        <div className="flex items-center">
                                            <Users
                                                className="h-4 w-4 mr-1"
                                                suppressHydrationWarning
                                            />
                                            <span>2/3 players</span>
                                        </div>
                                        <Badge variant="secondary">
                                            Active
                                        </Badge>
                                    </div>
                                </CardContent>
                            </div>
                        </Card>
                    </div>

                    {/* Recent Activity */}
                    <div className="bg-white rounded-lg p-6 shadow-sm">
                        <h2 className="text-2xl font-bold mb-6">
                            Recent Activity
                        </h2>
                        <div className="grid gap-4">
                            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div className="flex items-center space-x-4">
                                    <div className="flex items-center space-x-2">
                                        <Gamepad2
                                            className="h-5 w-5 text-purple-600"
                                            suppressHydrationWarning
                                        />
                                        <span className="font-medium">
                                            Sarah joined &quot;Overwatch
                                            Competitive&quot;
                                        </span>
                                    </div>
                                    <div className="flex items-center text-sm text-gray-500">
                                        <Users
                                            className="h-4 w-4 mr-1"
                                            suppressHydrationWarning
                                        />
                                        <span>5/6 players</span>
                                    </div>
                                </div>
                                <span className="text-sm text-gray-500">
                                    2 minutes ago
                                </span>
                            </div>

                            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div className="flex items-center space-x-4">
                                    <div className="flex items-center space-x-2">
                                        <Gamepad2
                                            className="h-5 w-5 text-purple-600"
                                            suppressHydrationWarning
                                        />
                                        <span className="font-medium">
                                            New room created: &quot;CS2
                                            Scrimmage&quot;
                                        </span>
                                    </div>
                                    <div className="flex items-center text-sm text-gray-500">
                                        <Users
                                            className="h-4 w-4 mr-1"
                                            suppressHydrationWarning
                                        />
                                        <span>1/5 players</span>
                                    </div>
                                </div>
                                <span className="text-sm text-gray-500">
                                    5 minutes ago
                                </span>
                            </div>

                            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div className="flex items-center space-x-4">
                                    <div className="flex items-center space-x-2">
                                        <Gamepad2
                                            className="h-5 w-5 text-purple-600"
                                            suppressHydrationWarning
                                        />
                                        <span className="font-medium">
                                            Mike completed &quot;Destiny 2
                                            Raid&quot;
                                        </span>
                                    </div>
                                    <div className="flex items-center text-sm text-gray-500">
                                        <Users
                                            className="h-4 w-4 mr-1"
                                            suppressHydrationWarning
                                        />
                                        <span>6/6 players</span>
                                    </div>
                                </div>
                                <span className="text-sm text-gray-500">
                                    15 minutes ago
                                </span>
                            </div>

                            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div className="flex items-center space-x-4">
                                    <div className="flex items-center space-x-2">
                                        <Gamepad2
                                            className="h-5 w-5 text-purple-600"
                                            suppressHydrationWarning
                                        />
                                        <span className="font-medium">
                                            Emma started &quot;Fortnite
                                            Duos&quot;
                                        </span>
                                    </div>
                                    <div className="flex items-center text-sm text-gray-500">
                                        <Users
                                            className="h-4 w-4 mr-1"
                                            suppressHydrationWarning
                                        />
                                        <span>2/2 players</span>
                                    </div>
                                </div>
                                <span className="text-sm text-gray-500">
                                    22 minutes ago
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-16 px-4">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-3xl font-bold text-center mb-12">
                        Why Choose AI Gaming Friend?
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <MessageCircle
                                    className="h-8 w-8 text-purple-600"
                                    suppressHydrationWarning
                                />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                Smart AI Companions
                            </h3>
                            <p className="text-gray-600">
                                Get paired with AI friends that understand your
                                gaming style and preferences.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Users
                                    className="h-8 w-8 text-blue-600"
                                    suppressHydrationWarning
                                />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                Find Your Squad
                            </h3>
                            <p className="text-gray-600">
                                Connect with like-minded players and build
                                lasting gaming friendships.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Star
                                    className="h-8 w-8 text-green-600"
                                    suppressHydrationWarning
                                />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                Level Up Together
                            </h3>
                            <p className="text-gray-600">
                                Improve your skills with AI coaching and
                                collaborative gameplay.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-16 px-4 bg-purple-600">
                <div className="max-w-4xl mx-auto text-center text-white">
                    <h2 className="text-3xl font-bold mb-4">
                        Ready to Game Smarter?
                    </h2>
                    <p className="text-xl mb-8 text-purple-100">
                        Join thousands of gamers who have enhanced their
                        experience with AI companions.
                    </p>
                    <Link href="/accounts/signup">
                        <Button
                            size="lg"
                            variant="secondary"
                            className="bg-white text-purple-600 hover:bg-gray-100"
                        >
                            Sign Up Free Today
                            <ArrowRight
                                className="ml-2 h-4 w-4"
                                suppressHydrationWarning
                            />
                        </Button>
                    </Link>
                </div>
            </section>
        </div>
    );
}
