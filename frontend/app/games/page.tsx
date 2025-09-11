import Image from "next/image";
import Link from "next/link";
import { Clock, Filter, Search, Star, Users } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function GamesPage() {
    const games = [
        {
            id: 1,
            name: "Ultimate Tic-Tac-Toe",
            description:
                "A strategic twist on the classic game with 9 interconnected boards",
            players: "2",
            difficulty: "Easy",
            duration: "5-10 min",
            rating: 4.2,
            image: "/placeholder.svg?height=200&width=300",
            category: "Strategy",
        },
        {
            id: 2,
            name: "Chess",
            description:
                "The timeless strategy game with AI opponents of varying skill levels",
            players: "2",
            difficulty: "Hard",
            duration: "15-60 min",
            rating: 4.8,
            image: "/placeholder.svg?height=200&width=300",
            category: "Strategy",
        },
        {
            id: 3,
            name: "Lands",
            description:
                "Custom territory control game with resource management",
            players: "2-4",
            difficulty: "Medium",
            duration: "20-30 min",
            rating: 4.5,
            image: "/placeholder.svg?height=200&width=300",
            category: "Strategy",
        },
        {
            id: 4,
            name: "Ultimate One Night Werewolf",
            description: "Fast-paced social deduction game with AI moderator",
            players: "4-8",
            difficulty: "Medium",
            duration: "10-15 min",
            rating: 4.6,
            image: "/placeholder.svg?height=200&width=300",
            category: "Social",
        },
        {
            id: 5,
            name: "Classic Mafia",
            description: "The original social deduction game with AI players",
            players: "6-12",
            difficulty: "Medium",
            duration: "30-45 min",
            rating: 4.3,
            image: "/placeholder.svg?height=200&width=300",
            category: "Social",
        },
        {
            id: 6,
            name: "Exploding Kittens",
            description: "Hilarious card game of strategy and luck",
            players: "2-5",
            difficulty: "Easy",
            duration: "10-15 min",
            rating: 4.4,
            image: "/placeholder.svg?height=200&width=300",
            category: "Card",
        },
    ];

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Game Library
                    </h1>
                    <p className="text-gray-600">
                        Choose from our collection of games and play with AI
                        companions
                    </p>
                </div>

                {/* Search and Filters */}
                <div className="mb-8 space-y-4">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                            <Input
                                placeholder="Search games..."
                                className="pl-10"
                            />
                        </div>
                        <Button
                            variant="outline"
                            className="md:w-auto bg-transparent"
                        >
                            <Filter className="mr-2 h-4 w-4" />
                            Filters
                        </Button>
                    </div>

                    <div className="flex flex-wrap gap-2">
                        <Button variant="outline" size="sm">
                            All Categories
                        </Button>
                        <Button variant="outline" size="sm">
                            Strategy
                        </Button>
                        <Button variant="outline" size="sm">
                            Social
                        </Button>
                        <Button variant="outline" size="sm">
                            Card Games
                        </Button>
                        <Button variant="outline" size="sm">
                            2 Players
                        </Button>
                        <Button variant="outline" size="sm">
                            Multiplayer
                        </Button>
                    </div>
                </div>

                {/* Games Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {games.map((game) => (
                        <Card
                            key={game.id}
                            className="hover:shadow-lg transition-shadow"
                        >
                            <CardHeader className="p-0">
                                <Image
                                    src={game.image || "/placeholder.svg"}
                                    alt={game.name}
                                    width={300}
                                    height={200}
                                    className="w-full h-48 object-cover rounded-t-lg"
                                />
                            </CardHeader>
                            <CardContent className="p-6">
                                <div className="flex justify-between items-start mb-2">
                                    <CardTitle className="text-xl">
                                        {game.name}
                                    </CardTitle>
                                    <div className="flex items-center gap-1">
                                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                                        <span className="text-sm text-gray-600">
                                            {game.rating}
                                        </span>
                                    </div>
                                </div>

                                <CardDescription className="mb-4 line-clamp-2">
                                    {game.description}
                                </CardDescription>

                                <div className="flex flex-wrap gap-2 mb-4">
                                    <Badge variant="secondary">
                                        {game.category}
                                    </Badge>
                                    <Badge
                                        variant={
                                            game.difficulty === "Easy"
                                                ? "secondary"
                                                : game.difficulty === "Medium"
                                                  ? "default"
                                                  : "destructive"
                                        }
                                    >
                                        {game.difficulty}
                                    </Badge>
                                </div>

                                <div className="flex justify-between items-center text-sm text-gray-600 mb-4">
                                    <div className="flex items-center gap-1">
                                        <Users className="h-4 w-4" />
                                        {game.players} players
                                    </div>
                                    <div className="flex items-center gap-1">
                                        <Clock className="h-4 w-4" />
                                        {game.duration}
                                    </div>
                                </div>

                                <div className="flex gap-2">
                                    <Link
                                        href={`/games/${game.id}`}
                                        className="flex-1"
                                    >
                                        <Button className="w-full">
                                            Play Now
                                        </Button>
                                    </Link>
                                    <Link href={`/games/${game.id}/info`}>
                                        <Button variant="outline" size="icon">
                                            <span className="sr-only">
                                                Game Info
                                            </span>
                                            ℹ️
                                        </Button>
                                    </Link>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
}
