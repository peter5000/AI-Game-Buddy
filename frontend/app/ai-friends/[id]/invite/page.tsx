"use client";

import { ArrowLeft, Gamepad2, MessageCircle, Users } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";

interface PageProps {
    params: Promise<{ id: string }>;
}

export default function InviteAIFriendPage({ params }: PageProps) {
    const [friendId, setFriendId] = useState<string>("");
    const [selectedGame, setSelectedGame] = useState("");
    const [gameMode, setGameMode] = useState("");
    const [roomType, setRoomType] = useState("private");

    // Resolve params Promise
    useEffect(() => {
        params.then((resolvedParams) => {
            setFriendId(resolvedParams.id);
        });
    }, [params]);

    // Mock AI friend data - now using friendId from state
    const aiFriend = {
        id: friendId,
        name: "Chess Master Alex",
        personality:
            "Strategic and analytical, loves discussing chess theory and tactics",
        avatar: "/placeholder.svg?height=80&width=80",
        difficulty: "Expert",
        favoriteGames: ["Chess", "Ultimate Tic-Tac-Toe"],
        traits: ["Strategic", "Patient", "Encouraging"],
    };

    const games = [
        {
            id: "chess",
            name: "Chess",
            description: "Classic strategy game",
            players: "2",
            duration: "15-60 min",
            modes: [
                {
                    value: "vs",
                    label: "Play Against AI",
                    description: "Compete against your AI friend",
                },
                {
                    value: "with",
                    label: "Team Up",
                    description: "Play together against other players",
                },
                {
                    value: "learn",
                    label: "Learning Mode",
                    description: "Get tips and guidance while playing",
                },
            ],
        },
        {
            id: "tic-tac-toe",
            name: "Ultimate Tic-Tac-Toe",
            description: "Strategic twist on classic tic-tac-toe",
            players: "2",
            duration: "5-10 min",
            modes: [
                {
                    value: "vs",
                    label: "Play Against AI",
                    description: "Challenge your AI friend",
                },
                {
                    value: "with",
                    label: "Team Up",
                    description: "Play together in multiplayer",
                },
            ],
        },
        {
            id: "werewolf",
            name: "Ultimate One Night Werewolf",
            description: "Social deduction game",
            players: "4-8",
            duration: "10-15 min",
            modes: [
                {
                    value: "with",
                    label: "Play Together",
                    description: "AI joins as a player in the group",
                },
                {
                    value: "moderate",
                    label: "AI Moderator",
                    description: "AI guides the game as moderator",
                },
            ],
        },
    ];

    const selectedGameData = games.find((g) => g.id === selectedGame);
    const availableModes = selectedGameData?.modes || [];

    const handleInvite = () => {
        // Handle game invitation logic
        // Redirect to game room or lobby
    };

    // Show loading state while params are being resolved
    if (!friendId) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto"></div>
                    <p className="mt-2 text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <Link href={`/ai-friends/${aiFriend.id}/chat`}>
                        <Button variant="ghost" size="sm">
                            <ArrowLeft className="mr-2 h-4 w-4" />
                            Back to Chat
                        </Button>
                    </Link>
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">
                            Invite AI Friend to Game
                        </h1>
                        <p className="text-gray-600">
                            Choose a game and play mode with {aiFriend.name}
                        </p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Game Selection */}
                    <div className="lg:col-span-2 space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Select Game</CardTitle>
                                <CardDescription>
                                    Choose which game you&apos;d like to play
                                    together
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {games.map((game) => (
                                    <Card
                                        key={game.id}
                                        className={`cursor-pointer transition-all ${
                                            selectedGame === game.id
                                                ? "ring-2 ring-purple-600 bg-purple-50"
                                                : "hover:shadow-md"
                                        }`}
                                        onClick={() => setSelectedGame(game.id)}
                                    >
                                        <CardContent className="pt-4">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <h3 className="font-semibold mb-1">
                                                        {game.name}
                                                    </h3>
                                                    <p className="text-sm text-gray-600 mb-2">
                                                        {game.description}
                                                    </p>
                                                    <div className="flex gap-4 text-sm text-gray-500">
                                                        <span className="flex items-center gap-1">
                                                            <Users className="h-4 w-4" />
                                                            {game.players}{" "}
                                                            players
                                                        </span>
                                                        <span>
                                                            {game.duration}
                                                        </span>
                                                    </div>
                                                </div>
                                                {aiFriend.favoriteGames.includes(
                                                    game.name
                                                ) && (
                                                    <Badge variant="secondary">
                                                        Favorite
                                                    </Badge>
                                                )}
                                            </div>
                                        </CardContent>
                                    </Card>
                                ))}
                            </CardContent>
                        </Card>

                        {selectedGame && (
                            <Card>
                                <CardHeader>
                                    <CardTitle>Game Mode</CardTitle>
                                    <CardDescription>
                                        How would you like to play with your AI
                                        friend?
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    {availableModes.map((mode) => (
                                        <Card
                                            key={mode.value}
                                            className={`cursor-pointer transition-all ${
                                                gameMode === mode.value
                                                    ? "ring-2 ring-purple-600 bg-purple-50"
                                                    : "hover:shadow-md"
                                            }`}
                                            onClick={() =>
                                                setGameMode(mode.value)
                                            }
                                        >
                                            <CardContent className="pt-4">
                                                <h3 className="font-semibold mb-1">
                                                    {mode.label}
                                                </h3>
                                                <p className="text-sm text-gray-600">
                                                    {mode.description}
                                                </p>
                                            </CardContent>
                                        </Card>
                                    ))}
                                </CardContent>
                            </Card>
                        )}

                        {gameMode && (
                            <Card>
                                <CardHeader>
                                    <CardTitle>Room Settings</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="space-y-2">
                                        <Label>Room Type</Label>
                                        <Select
                                            value={roomType}
                                            onValueChange={setRoomType}
                                        >
                                            <SelectTrigger>
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="private">
                                                    Private - Just you and your
                                                    AI friend
                                                </SelectItem>
                                                <SelectItem value="public">
                                                    Public - Others can join and
                                                    spectate
                                                </SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </CardContent>
                            </Card>
                        )}
                    </div>

                    {/* AI Friend Info & Invite */}
                    <div className="lg:col-span-1">
                        <Card className="sticky top-8">
                            <CardHeader>
                                <CardTitle>AI Friend</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="text-center">
                                    <Avatar className="w-20 h-20 mx-auto mb-4">
                                        <AvatarImage
                                            src={
                                                aiFriend.avatar ||
                                                "/placeholder.svg"
                                            }
                                        />
                                        <AvatarFallback>AM</AvatarFallback>
                                    </Avatar>
                                    <h3 className="font-semibold text-lg">
                                        {aiFriend.name}
                                    </h3>
                                    <Badge variant="secondary" className="mt-2">
                                        {aiFriend.difficulty}
                                    </Badge>
                                </div>

                                <Separator />

                                <div>
                                    <h4 className="font-medium mb-2">
                                        Personality
                                    </h4>
                                    <p className="text-sm text-gray-600">
                                        {aiFriend.personality}
                                    </p>
                                </div>

                                <div>
                                    <h4 className="font-medium mb-2">Traits</h4>
                                    <div className="flex flex-wrap gap-1">
                                        {aiFriend.traits.map((trait) => (
                                            <Badge
                                                key={trait}
                                                variant="outline"
                                                className="text-xs"
                                            >
                                                {trait}
                                            </Badge>
                                        ))}
                                    </div>
                                </div>

                                <div>
                                    <h4 className="font-medium mb-2">
                                        Favorite Games
                                    </h4>
                                    <div className="flex flex-wrap gap-1">
                                        {aiFriend.favoriteGames.map((game) => (
                                            <Badge
                                                key={game}
                                                variant="secondary"
                                                className="text-xs"
                                            >
                                                {game}
                                            </Badge>
                                        ))}
                                    </div>
                                </div>

                                <Separator />

                                <div className="space-y-2">
                                    <Button
                                        className="w-full"
                                        onClick={handleInvite}
                                        disabled={!selectedGame || !gameMode}
                                    >
                                        <Gamepad2 className="mr-2 h-4 w-4" />
                                        Start Game
                                    </Button>

                                    <Link
                                        href={`/ai-friends/${aiFriend.id}/chat`}
                                    >
                                        <Button
                                            variant="outline"
                                            className="w-full bg-transparent"
                                        >
                                            <MessageCircle className="mr-2 h-4 w-4" />
                                            Chat First
                                        </Button>
                                    </Link>
                                </div>

                                {selectedGame && gameMode && (
                                    <div className="bg-blue-50 p-3 rounded-lg">
                                        <h4 className="font-medium text-blue-900 mb-1">
                                            Ready to Play!
                                        </h4>
                                        <p className="text-sm text-blue-700">
                                            {selectedGameData?.name} -{" "}
                                            {
                                                availableModes.find(
                                                    (m) => m.value === gameMode
                                                )?.label
                                            }
                                        </p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}
