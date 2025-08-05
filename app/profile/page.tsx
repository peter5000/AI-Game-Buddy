import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Trophy, Calendar, Clock, Target, TrendingUp, Settings } from "lucide-react"
import Link from "next/link"

export default function ProfilePage() {
  const user = {
    username: "GameMaster2024",
    email: "gamemaster@example.com",
    joinDate: "March 2024",
    avatar: "/placeholder.svg?height=100&width=100",
    level: 15,
    xp: 2450,
    nextLevelXp: 3000,
  }

  const gameStats = [
    { game: "Chess", wins: 24, losses: 18, draws: 6, winRate: 50, hoursPlayed: 45 },
    { game: "Ultimate Tic-Tac-Toe", wins: 32, losses: 12, draws: 4, winRate: 67, hoursPlayed: 28 },
    { game: "Werewolf", wins: 15, losses: 20, draws: 0, winRate: 43, hoursPlayed: 22 },
    { game: "Lands", wins: 8, losses: 5, draws: 2, winRate: 53, hoursPlayed: 18 },
  ]

  const recentGames = [
    { id: 1, game: "Chess", opponent: "AI-Bobby", result: "Win", date: "2 hours ago", duration: "25 min" },
    { id: 2, game: "Ultimate Tic-Tac-Toe", opponent: "PlayerX", result: "Loss", date: "1 day ago", duration: "8 min" },
    { id: 3, game: "Werewolf", opponent: "AI-Moderator", result: "Win", date: "2 days ago", duration: "15 min" },
    { id: 4, game: "Chess", opponent: "AI-Kasparov", result: "Draw", date: "3 days ago", duration: "42 min" },
    { id: 5, game: "Lands", opponent: "StrategyPro", result: "Win", date: "4 days ago", duration: "35 min" },
  ]

  const achievements = [
    { name: "First Victory", description: "Win your first game", earned: true },
    { name: "Chess Master", description: "Win 25 chess games", earned: true },
    { name: "Social Player", description: "Play 10 multiplayer games", earned: true },
    { name: "Strategist", description: "Win 5 strategy games in a row", earned: false },
    { name: "Night Owl", description: "Play 50 games after midnight", earned: false },
    { name: "AI Whisperer", description: "Win against all AI personalities", earned: false },
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
              <Avatar className="w-24 h-24">
                <AvatarImage src={user.avatar || "/placeholder.svg"} />
                <AvatarFallback className="text-2xl">GM</AvatarFallback>
              </Avatar>

              <div className="flex-1 text-center md:text-left">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{user.username}</h1>
                <p className="text-gray-600 mb-4">Member since {user.joinDate}</p>

                <div className="flex flex-col sm:flex-row gap-4 items-center">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-lg px-3 py-1">
                      Level {user.level}
                    </Badge>
                    <span className="text-sm text-gray-600">
                      {user.xp} / {user.nextLevelXp} XP
                    </span>
                  </div>
                  <Progress value={(user.xp / user.nextLevelXp) * 100} className="w-32" />
                </div>
              </div>

              <Link href="/settings">
                <Button variant="outline">
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Profile Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="stats">Game Stats</TabsTrigger>
            <TabsTrigger value="history">Game History</TabsTrigger>
            <TabsTrigger value="achievements">Achievements</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Games</CardTitle>
                  <Target className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">127</div>
                  <p className="text-xs text-muted-foreground">+12 from last week</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">62%</div>
                  <p className="text-xs text-muted-foreground">+5% from last month</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Hours Played</CardTitle>
                  <Clock className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">113h</div>
                  <p className="text-xs text-muted-foreground">This month</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Favorite Game</CardTitle>
                  <Trophy className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">Chess</div>
                  <p className="text-xs text-muted-foreground">45 hours played</p>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Your latest games and achievements</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentGames.slice(0, 3).map((game) => (
                    <div key={game.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <Badge
                          variant={
                            game.result === "Win" ? "default" : game.result === "Loss" ? "destructive" : "secondary"
                          }
                        >
                          {game.result}
                        </Badge>
                        <div>
                          <p className="font-medium">{game.game}</p>
                          <p className="text-sm text-gray-600">vs {game.opponent}</p>
                        </div>
                      </div>
                      <div className="text-right text-sm text-gray-600">
                        <p>{game.date}</p>
                        <p>{game.duration}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="stats" className="space-y-6">
            <div className="grid gap-6">
              {gameStats.map((stat) => (
                <Card key={stat.game}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      {stat.game}
                      <Badge variant="outline">{stat.winRate}% Win Rate</Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                      <div className="text-center">
                        <p className="text-2xl font-bold text-green-600">{stat.wins}</p>
                        <p className="text-sm text-gray-600">Wins</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-bold text-red-600">{stat.losses}</p>
                        <p className="text-sm text-gray-600">Losses</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-bold text-yellow-600">{stat.draws}</p>
                        <p className="text-sm text-gray-600">Draws</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-bold text-blue-600">{stat.hoursPlayed}h</p>
                        <p className="text-sm text-gray-600">Played</p>
                      </div>
                      <div className="text-center">
                        <Progress value={stat.winRate} className="mt-2" />
                        <p className="text-sm text-gray-600 mt-1">Win Rate</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="history" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Game History</CardTitle>
                <CardDescription>Your complete gaming history</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentGames.map((game) => (
                    <div
                      key={game.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                    >
                      <div className="flex items-center gap-4">
                        <Badge
                          variant={
                            game.result === "Win" ? "default" : game.result === "Loss" ? "destructive" : "secondary"
                          }
                        >
                          {game.result}
                        </Badge>
                        <div>
                          <p className="font-medium">{game.game}</p>
                          <p className="text-sm text-gray-600">vs {game.opponent}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {game.duration}
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {game.date}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="achievements" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {achievements.map((achievement) => (
                <Card key={achievement.name} className={achievement.earned ? "border-yellow-200 bg-yellow-50" : ""}>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-4">
                      <div
                        className={`w-12 h-12 rounded-full flex items-center justify-center ${
                          achievement.earned ? "bg-yellow-200" : "bg-gray-200"
                        }`}
                      >
                        <Trophy className={`h-6 w-6 ${achievement.earned ? "text-yellow-600" : "text-gray-400"}`} />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold">{achievement.name}</h3>
                        <p className="text-sm text-gray-600">{achievement.description}</p>
                        {achievement.earned && (
                          <Badge variant="secondary" className="mt-2">
                            Earned
                          </Badge>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
