"use client";

import { ArrowLeft, MessageCircle, Sparkles, User, Wand2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";

export default function CreateAIFriendPage() {
    const [aiData, setAiData] = useState({
        name: "",
        personality: "",
        difficulty: "",
        favoriteGames: [] as string[],
        traits: [] as string[],
        avatar: "",
        customPrompt: "",
    });

    const [isGenerating, setIsGenerating] = useState(false);
    const [previewMode, setPreviewMode] = useState(false);

    const difficultyOptions = [
        {
            value: "beginner",
            label: "Beginner",
            description: "Easy-going, makes simple moves",
        },
        {
            value: "intermediate",
            label: "Intermediate",
            description: "Balanced gameplay, good for learning",
        },
        {
            value: "hard",
            label: "Hard",
            description: "Challenging opponent, strategic thinking",
        },
        {
            value: "expert",
            label: "Expert",
            description: "Advanced strategies, minimal mistakes",
        },
        {
            value: "master",
            label: "Master",
            description: "Near-perfect play, ultimate challenge",
        },
    ];

    const gameOptions = [
        "Chess",
        "Ultimate Tic-Tac-Toe",
        "Lands",
        "Werewolf",
        "Mafia",
        "Exploding Kittens",
    ];

    const traitOptions = [
        "Friendly",
        "Competitive",
        "Witty",
        "Supportive",
        "Strategic",
        "Cheerful",
        "Sarcastic",
        "Patient",
        "Encouraging",
        "Analytical",
        "Creative",
        "Calm",
        "Energetic",
        "Wise",
        "Playful",
        "Serious",
        "Humorous",
        "Focused",
    ];

    const personalityTemplates = [
        {
            name: "The Mentor",
            description: "Wise and patient, helps you improve your skills",
            prompt: "You are a wise and patient gaming mentor who loves helping players improve. You offer strategic advice, celebrate progress, and provide encouraging feedback. You speak with wisdom and kindness, always focusing on learning and growth.",
        },
        {
            name: "The Rival",
            description:
                "Competitive and challenging, pushes you to your limits",
            prompt: "You are a competitive gaming rival who loves a good challenge. You're confident, sometimes cocky, but always respectful. You enjoy trash talk and banter, but you also recognize good plays and show respect when deserved.",
        },
        {
            name: "The Cheerleader",
            description: "Enthusiastic and supportive, celebrates every move",
            prompt: "You are an enthusiastic and supportive gaming companion who celebrates every good move and encourages during tough moments. You're bubbly, positive, and always find something good to say. You make gaming fun and lighthearted.",
        },
        {
            name: "The Strategist",
            description: "Analytical and tactical, discusses deep strategy",
            prompt: "You are a strategic gaming companion who loves analyzing moves and discussing tactics. You think several steps ahead, explain your reasoning, and enjoy deep strategic conversations. You're logical, methodical, and intellectually curious.",
        },
    ];

    const handleInputChange = (field: string, value: string | string[]) => {
        setAiData((prev) => ({ ...prev, [field]: value }));
    };

    const toggleGame = (game: string) => {
        setAiData((prev) => ({
            ...prev,
            favoriteGames: prev.favoriteGames.includes(game)
                ? prev.favoriteGames.filter((g) => g !== game)
                : [...prev.favoriteGames, game],
        }));
    };

    const toggleTrait = (trait: string) => {
        setAiData((prev) => ({
            ...prev,
            traits: prev.traits.includes(trait)
                ? prev.traits.filter((t) => t !== trait)
                : [...prev.traits, trait],
        }));
    };

    const applyTemplate = (template: (typeof personalityTemplates)[0]) => {
        setAiData((prev) => ({
            ...prev,
            personality: template.description,
            customPrompt: template.prompt,
        }));
    };

    const generateAI = async () => {
        setIsGenerating(true);
        // Simulate AI generation
        await new Promise((resolve) => setTimeout(resolve, 2000));
        setIsGenerating(false);
        setPreviewMode(true);
    };

    const saveAIFriend = () => {
        // Handle saving the AI friend
        // Redirect to AI friends list
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <Link href="/ai-friends">
                        <Button variant="ghost" size="sm">
                            <ArrowLeft className="mr-2 h-4 w-4" />
                            Back to AI Friends
                        </Button>
                    </Link>
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">
                            Create New AI Friend
                        </h1>
                        <p className="text-gray-600">
                            Design your perfect gaming companion
                        </p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Form */}
                    <div className="lg:col-span-2">
                        <Tabs defaultValue="basic" className="space-y-6">
                            <TabsList className="grid w-full grid-cols-3">
                                <TabsTrigger value="basic">
                                    Basic Info
                                </TabsTrigger>
                                <TabsTrigger value="personality">
                                    Personality
                                </TabsTrigger>
                                <TabsTrigger value="advanced">
                                    Advanced
                                </TabsTrigger>
                            </TabsList>

                            <TabsContent value="basic" className="space-y-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <User className="h-5 w-5" />
                                            Basic Information
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="space-y-2">
                                            <Label htmlFor="name">
                                                AI Friend Name
                                            </Label>
                                            <Input
                                                id="name"
                                                placeholder="e.g., Chess Master Alex, Luna the Cheerful"
                                                value={aiData.name}
                                                onChange={(e) =>
                                                    handleInputChange(
                                                        "name",
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </div>

                                        <div className="space-y-2">
                                            <Label htmlFor="difficulty">
                                                Skill Level
                                            </Label>
                                            <Select
                                                value={aiData.difficulty}
                                                onValueChange={(value) =>
                                                    handleInputChange(
                                                        "difficulty",
                                                        value
                                                    )
                                                }
                                            >
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select difficulty level" />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    {difficultyOptions.map(
                                                        (option) => (
                                                            <SelectItem
                                                                key={
                                                                    option.value
                                                                }
                                                                value={
                                                                    option.value
                                                                }
                                                            >
                                                                <div>
                                                                    <div className="font-medium">
                                                                        {
                                                                            option.label
                                                                        }
                                                                    </div>
                                                                    <div className="text-sm text-gray-600">
                                                                        {
                                                                            option.description
                                                                        }
                                                                    </div>
                                                                </div>
                                                            </SelectItem>
                                                        )
                                                    )}
                                                </SelectContent>
                                            </Select>
                                        </div>

                                        <div className="space-y-2">
                                            <Label>Favorite Games</Label>
                                            <div className="flex flex-wrap gap-2">
                                                {gameOptions.map((game) => (
                                                    <Badge
                                                        key={game}
                                                        variant={
                                                            aiData.favoriteGames.includes(
                                                                game
                                                            )
                                                                ? "default"
                                                                : "outline"
                                                        }
                                                        className="cursor-pointer"
                                                        onClick={() =>
                                                            toggleGame(game)
                                                        }
                                                    >
                                                        {game}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>

                                        <div className="space-y-2">
                                            <Label>Personality Traits</Label>
                                            <div className="flex flex-wrap gap-2">
                                                {traitOptions.map((trait) => (
                                                    <Badge
                                                        key={trait}
                                                        variant={
                                                            aiData.traits.includes(
                                                                trait
                                                            )
                                                                ? "default"
                                                                : "outline"
                                                        }
                                                        className="cursor-pointer"
                                                        onClick={() =>
                                                            toggleTrait(trait)
                                                        }
                                                    >
                                                        {trait}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent
                                value="personality"
                                className="space-y-6"
                            >
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <MessageCircle className="h-5 w-5" />
                                            Personality Templates
                                        </CardTitle>
                                        <CardDescription>
                                            Choose a template to get started,
                                            then customize further
                                        </CardDescription>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            {personalityTemplates.map(
                                                (template) => (
                                                    <Card
                                                        key={template.name}
                                                        className="cursor-pointer hover:shadow-md transition-shadow"
                                                        onClick={() =>
                                                            applyTemplate(
                                                                template
                                                            )
                                                        }
                                                    >
                                                        <CardContent className="pt-4">
                                                            <h3 className="font-semibold mb-2">
                                                                {template.name}
                                                            </h3>
                                                            <p className="text-sm text-gray-600">
                                                                {
                                                                    template.description
                                                                }
                                                            </p>
                                                        </CardContent>
                                                    </Card>
                                                )
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>

                                <Card>
                                    <CardHeader>
                                        <CardTitle>
                                            Personality Description
                                        </CardTitle>
                                        <CardDescription>
                                            Describe how you want your AI friend
                                            to behave and communicate
                                        </CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <Textarea
                                            placeholder="e.g., Friendly and encouraging, loves to celebrate good moves and help with strategy. Has a cheerful personality and uses emojis occasionally."
                                            value={aiData.personality}
                                            onChange={(e) =>
                                                handleInputChange(
                                                    "personality",
                                                    e.target.value
                                                )
                                            }
                                            rows={4}
                                        />
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value="advanced" className="space-y-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <Wand2 className="h-5 w-5" />
                                            Custom AI Prompt
                                        </CardTitle>
                                        <CardDescription>
                                            Advanced: Write a detailed prompt to
                                            define your AI&apos;s behavior,
                                            speaking style, and personality
                                        </CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <Textarea
                                            placeholder="You are a gaming companion who... [Describe in detail how the AI should behave, speak, and interact]"
                                            value={aiData.customPrompt}
                                            onChange={(e) =>
                                                handleInputChange(
                                                    "customPrompt",
                                                    e.target.value
                                                )
                                            }
                                            rows={8}
                                            className="font-mono text-sm"
                                        />
                                        <p className="text-sm text-gray-600 mt-2">
                                            This prompt will be used to train
                                            your AI friend&apos;s personality
                                            and responses.
                                        </p>
                                    </CardContent>
                                </Card>
                            </TabsContent>
                        </Tabs>
                    </div>

                    {/* Preview Panel */}
                    <div className="lg:col-span-1">
                        <Card className="sticky top-8">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Sparkles className="h-5 w-5" />
                                    AI Friend Preview
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="text-center">
                                    <Avatar className="w-20 h-20 mx-auto mb-4">
                                        <AvatarImage
                                            src={
                                                aiData.avatar ||
                                                "/placeholder.svg"
                                            }
                                        />
                                        <AvatarFallback className="text-lg">
                                            {aiData.name
                                                ? aiData.name
                                                      .split(" ")
                                                      .map((n) => n[0])
                                                      .join("")
                                                : "AI"}
                                        </AvatarFallback>
                                    </Avatar>
                                    <h3 className="font-semibold text-lg">
                                        {aiData.name || "Your AI Friend"}
                                    </h3>
                                    {aiData.difficulty && (
                                        <Badge
                                            variant="secondary"
                                            className="mt-2"
                                        >
                                            {
                                                difficultyOptions.find(
                                                    (d) =>
                                                        d.value ===
                                                        aiData.difficulty
                                                )?.label
                                            }
                                        </Badge>
                                    )}
                                </div>

                                <Separator />

                                {aiData.personality && (
                                    <div>
                                        <h4 className="font-medium mb-2">
                                            Personality
                                        </h4>
                                        <p className="text-sm text-gray-600">
                                            {aiData.personality}
                                        </p>
                                    </div>
                                )}

                                {aiData.traits.length > 0 && (
                                    <div>
                                        <h4 className="font-medium mb-2">
                                            Traits
                                        </h4>
                                        <div className="flex flex-wrap gap-1">
                                            {aiData.traits.map((trait) => (
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
                                )}

                                {aiData.favoriteGames.length > 0 && (
                                    <div>
                                        <h4 className="font-medium mb-2">
                                            Favorite Games
                                        </h4>
                                        <div className="flex flex-wrap gap-1">
                                            {aiData.favoriteGames.map(
                                                (game) => (
                                                    <Badge
                                                        key={game}
                                                        variant="secondary"
                                                        className="text-xs"
                                                    >
                                                        {game}
                                                    </Badge>
                                                )
                                            )}
                                        </div>
                                    </div>
                                )}

                                <Separator />

                                <div className="space-y-2">
                                    <Button
                                        className="w-full"
                                        onClick={generateAI}
                                        disabled={
                                            !aiData.name ||
                                            !aiData.personality ||
                                            isGenerating
                                        }
                                    >
                                        {isGenerating ? (
                                            <>
                                                <Sparkles className="mr-2 h-4 w-4 animate-spin" />
                                                Generating AI...
                                            </>
                                        ) : (
                                            <>
                                                <Sparkles className="mr-2 h-4 w-4" />
                                                Generate AI Friend
                                            </>
                                        )}
                                    </Button>

                                    {previewMode && (
                                        <Button
                                            variant="outline"
                                            className="w-full bg-transparent"
                                            onClick={saveAIFriend}
                                        >
                                            Save AI Friend
                                        </Button>
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}
