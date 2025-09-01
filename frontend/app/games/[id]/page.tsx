"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Users, Clock, Star, Settings, MessageCircle, Volume2 } from "lucide-react"
import Link from "next/link"

export default function GameRoomPage({ params }: { params: { id: string } }) {
  const [roomType, setRoomType] = useState("public")
  const [aiPersonality, setAiPersonality] = useState("friendly")
  const [maxPlayers, setMaxPlayers] = useState("2")
  const [selectedAIFriend, setSelectedAIFriend] = useState("")

  // Mock game data - in real app, fetch based on params.id
  const game = {
    id: params.id,
    name: "Ultimate Tic-Tac-Toe",
    description: "A strategic twist on the classic game with 9 interconnected boards",
    players: "2",
    difficulty: "Easy",
    duration: "5-10 min",
    rating: 4.2,
    image: "/placeholder.svg?height=300&width=400",
    rules: [
      "Play on a 3x3 grid of 3x3 tic-tac-toe boards",
      "Your move determines which board your opponent plays on next",
      "Win three boards in a row to win the game",
      "If sent to a completed board, you can play anywhere",
    ],
  }

  const handleCreateRoom = () => {
    // Handle room creation logic
    console.log("Creating room with:", { roomType, aiPersonality, maxPlayers })
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Game Info */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <img
                  src={game.image || "/placeholder.svg"}
                  alt={game.name}
                  className="w-full h-64 object-cover rounded-lg mb-4"
                />
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-2xl mb-2">{game.name}</CardTitle>
                    <CardDescription className="text-base">{game.description}</CardDescription>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                    <span className="font-semibold">{game.rating}</span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-4 mb-6">
                  <div className="flex items-center gap-2">
                    <Users className="h-5 w-5 text-gray-500" />
                    <span>{game.players} players</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="h-5 w-5 text-gray-500" />
                    <span>{game.duration}</span>
                  </div>
                  <Badge variant={game.difficulty === "Easy" ? "secondary" : "default"}>{game.difficulty}</Badge>
                </div>

                <Separator className="my-6" />

                <div>
                  <h3 className="text-lg font-semibold mb-3">How to Play</h3>
                  <ul className="space-y-2">
                    {game.rules.map((rule, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="bg-purple-100 text-purple-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold mt-0.5">
                          {index + 1}
                        </span>
                        <span className="text-gray-700">{rule}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mt-6">
                  <Link href={`/games/${game.id}/info`}>
                    <Button variant="outline">View Full Rules & Documentation</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Room Creation */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Create Game Room
                </CardTitle>
                <CardDescription>Set up your game preferences and invite players</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="room-type">Room Type</Label>
                  <Select value={roomType} onValueChange={setRoomType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="public">Public - Anyone can join</SelectItem>
                      <SelectItem value="private">Private - Invite only</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Invite AI Friend (Optional)</Label>
                  <Select value={selectedAIFriend} onValueChange={setSelectedAIFriend}>
                    <SelectTrigger>
                      <SelectValue placeholder="Choose an AI friend to invite" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">Play without AI friend</SelectItem>
                      <SelectItem value="alex">Chess Master Alex</SelectItem>
                      <SelectItem value="luna">Luna the Cheerful</SelectItem>
                      <SelectItem value="rick">Rival Rick</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="max-players">Max Players</Label>
                  <Select value={maxPlayers} onValueChange={setMaxPlayers}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="2">2 Players</SelectItem>
                      <SelectItem value="3">3 Players</SelectItem>
                      <SelectItem value="4">4 Players</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {roomType === "private" && (
                  <div className="space-y-2">
                    <Label htmlFor="invite-code">Room Code (Optional)</Label>
                    <Input id="invite-code" placeholder="Enter custom room code" />
                  </div>
                )}

                <Separator />

                <div className="space-y-3">
                  <h4 className="font-medium">Game Features</h4>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <MessageCircle className="h-4 w-4" />
                      <span className="text-sm">Text Chat</span>
                    </div>
                    <Badge variant="secondary">Enabled</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Volume2 className="h-4 w-4" />
                      <span className="text-sm">Voice Chat</span>
                    </div>
                    <Badge variant="outline">Coming Soon</Badge>
                  </div>
                </div>

                <Button className="w-full" onClick={handleCreateRoom}>
                  Create Room
                </Button>

                <div className="text-center">
                  <Link href="/rooms" className="text-sm text-purple-600 hover:underline">
                    Or browse existing rooms
                  </Link>
                </div>
              </CardContent>
            </Card>

            {/* Quick Play */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Quick Play</CardTitle>
                <CardDescription>Jump into a game immediately with default settings</CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/ai-friends/create">
                  <Button className="w-full bg-transparent" variant="outline">
                    Create AI Friend
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
