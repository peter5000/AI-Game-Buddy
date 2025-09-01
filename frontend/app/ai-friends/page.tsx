"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Plus, Search, MessageCircle, Gamepad2, Settings, Trash2, Heart } from "lucide-react"
import Link from "next/link"

export default function AIFriendsPage() {
  const [searchQuery, setSearchQuery] = useState("")

  // Mock AI friends data
  const aiFriends = [
    {
      id: 1,
      name: "Chess Master Alex",
      personality: "Strategic and analytical, loves discussing chess theory and tactics",
      avatar: "/placeholder.svg?height=80&width=80",
      gamesPlayed: 45,
      favoriteGames: ["Chess", "Ultimate Tic-Tac-Toe"],
      relationship: "Close Friend",
      lastActive: "2 hours ago",
      difficulty: "Expert",
      traits: ["Strategic", "Patient", "Encouraging"],
    },
    {
      id: 2,
      name: "Luna the Cheerful",
      personality: "Bubbly and supportive, always celebrates your victories and helps you learn from defeats",
      avatar: "/placeholder.svg?height=80&width=80",
      gamesPlayed: 28,
      favoriteGames: ["Werewolf", "Exploding Kittens"],
      relationship: "Best Friend",
      lastActive: "30 minutes ago",
      difficulty: "Intermediate",
      traits: ["Cheerful", "Supportive", "Funny"],
    },
    {
      id: 3,
      name: "Rival Rick",
      personality: "Competitive trash-talker who pushes you to your limits with witty banter",
      avatar: "/placeholder.svg?height=80&width=80",
      gamesPlayed: 67,
      favoriteGames: ["Chess", "Lands"],
      relationship: "Friendly Rival",
      lastActive: "1 day ago",
      difficulty: "Hard",
      traits: ["Competitive", "Witty", "Challenging"],
    },
    {
      id: 4,
      name: "Sage the Wise",
      personality: "Calm and philosophical, offers deep insights about strategy and life",
      avatar: "/placeholder.svg?height=80&width=80",
      gamesPlayed: 89,
      favoriteGames: ["Chess", "Mafia"],
      relationship: "Mentor",
      lastActive: "5 hours ago",
      difficulty: "Master",
      traits: ["Wise", "Calm", "Insightful"],
    },
  ]

  const filteredFriends = aiFriends.filter(
    (friend) =>
      friend.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      friend.personality.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getRelationshipColor = (relationship: string) => {
    switch (relationship) {
      case "Best Friend":
        return "bg-pink-100 text-pink-700"
      case "Close Friend":
        return "bg-blue-100 text-blue-700"
      case "Friendly Rival":
        return "bg-orange-100 text-orange-700"
      case "Mentor":
        return "bg-purple-100 text-purple-700"
      default:
        return "bg-gray-100 text-gray-700"
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Beginner":
        return "bg-green-100 text-green-700"
      case "Intermediate":
        return "bg-yellow-100 text-yellow-700"
      case "Hard":
        return "bg-orange-100 text-orange-700"
      case "Expert":
        return "bg-red-100 text-red-700"
      case "Master":
        return "bg-purple-100 text-purple-700"
      default:
        return "bg-gray-100 text-gray-700"
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Your AI Friends</h1>
            <p className="text-gray-600">Manage your custom AI companions and their personalities</p>
          </div>
          <Link href="/ai-friends/create">
            <Button className="mt-4 md:mt-0">
              <Plus className="mr-2 h-4 w-4" />
              Create New AI Friend
            </Button>
          </Link>
        </div>

        {/* Search */}
        <div className="mb-8">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search AI friends..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* AI Friends Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredFriends.map((friend) => (
            <Card key={friend.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <Avatar className="w-16 h-16">
                    <AvatarImage src={friend.avatar || "/placeholder.svg"} />
                    <AvatarFallback>
                      {friend.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <CardTitle className="text-lg">{friend.name}</CardTitle>
                    <div className="flex flex-wrap gap-1 mt-2">
                      <Badge className={getRelationshipColor(friend.relationship)} variant="secondary">
                        {friend.relationship}
                      </Badge>
                      <Badge className={getDifficultyColor(friend.difficulty)} variant="secondary">
                        {friend.difficulty}
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4 line-clamp-3">{friend.personality}</CardDescription>

                <div className="space-y-3">
                  <div className="flex flex-wrap gap-1">
                    {friend.traits.map((trait) => (
                      <Badge key={trait} variant="outline" className="text-xs">
                        {trait}
                      </Badge>
                    ))}
                  </div>

                  <div className="text-sm text-gray-600">
                    <p>Games played together: {friend.gamesPlayed}</p>
                    <p>Last active: {friend.lastActive}</p>
                  </div>

                  <div className="text-sm">
                    <p className="font-medium mb-1">Favorite Games:</p>
                    <div className="flex flex-wrap gap-1">
                      {friend.favoriteGames.map((game) => (
                        <Badge key={game} variant="secondary" className="text-xs">
                          {game}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex gap-2 mt-6">
                  <Link href={`/ai-friends/${friend.id}/chat`} className="flex-1">
                    <Button variant="outline" size="sm" className="w-full bg-transparent">
                      <MessageCircle className="mr-2 h-4 w-4" />
                      Chat
                    </Button>
                  </Link>
                  <Link href={`/ai-friends/${friend.id}/invite`} className="flex-1">
                    <Button size="sm" className="w-full">
                      <Gamepad2 className="mr-2 h-4 w-4" />
                      Invite to Game
                    </Button>
                  </Link>
                </div>

                <div className="flex gap-2 mt-2">
                  <Link href={`/ai-friends/${friend.id}/edit`} className="flex-1">
                    <Button variant="ghost" size="sm" className="w-full">
                      <Settings className="mr-2 h-4 w-4" />
                      Edit
                    </Button>
                  </Link>
                  <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700 hover:bg-red-50">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredFriends.length === 0 && (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Heart className="h-12 w-12 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No AI friends found</h3>
            <p className="text-gray-600 mb-4">
              {searchQuery ? "Try adjusting your search terms" : "Create your first AI friend to get started!"}
            </p>
            {!searchQuery && (
              <Link href="/ai-friends/create">
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Create Your First AI Friend
                </Button>
              </Link>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
