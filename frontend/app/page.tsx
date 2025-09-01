import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Search, Users, Gamepad2, MessageCircle, Star } from "lucide-react"
import Link from "next/link"

export default function LandingPage() {
  const featuredGames = [
    {
      id: 1,
      name: "Ultimate Tic-Tac-Toe",
      players: "2",
      difficulty: "Easy",
      image: "/placeholder.svg?height=200&width=300",
    },
    { id: 2, name: "Chess", players: "2", difficulty: "Hard", image: "/placeholder.svg?height=200&width=300" },
    { id: 3, name: "Lands", players: "2-4", difficulty: "Medium", image: "/placeholder.svg?height=200&width=300" },
    {
      id: 4,
      name: "Ultimate One Night Werewolf",
      players: "4-8",
      difficulty: "Medium",
      image: "/placeholder.svg?height=200&width=300",
    },
  ]

  const activeRooms = [
    { id: 1, game: "Chess", host: "AlexMaster", players: "1/2", type: "Public", ai: "Friendly" },
    { id: 2, game: "Ultimate Tic-Tac-Toe", host: "GamePro", players: "2/2", type: "Private", ai: "Competitive" },
    { id: 3, game: "Werewolf", host: "NightOwl", players: "5/8", type: "Public", ai: "Trash Talk" },
    { id: 4, game: "Lands", host: "StrategyKing", players: "2/4", type: "Public", ai: "Friendly" },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      {/* Hero Section */}
      <section className="relative py-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">Create Your Perfect AI Gaming Companions</h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Design custom AI friends with unique personalities, chat with them, and invite them to play your favorite
            games. Build lasting relationships with AI companions tailored to your gaming style.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/auth/signup">
              <Button size="lg" className="bg-purple-600 hover:bg-purple-700">
                Create Your First AI Friend
              </Button>
            </Link>
            <Link href="/games">
              <Button size="lg" variant="outline">
                Browse Games
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Search and Filters */}
      <section className="py-12 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input placeholder="Search games, rooms, or players..." className="pl-10" />
            </div>
            <div className="flex gap-2">
              <Button variant="outline">All Games</Button>
              <Button variant="outline">2 Players</Button>
              <Button variant="outline">Multiplayer</Button>
              <Button variant="outline">Strategy</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Games */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Featured Games</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredGames.map((game) => (
              <Card key={game.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader className="p-0">
                  <img
                    src={game.image || "/placeholder.svg"}
                    alt={game.name}
                    className="w-full h-48 object-cover rounded-t-lg"
                  />
                </CardHeader>
                <CardContent className="p-4">
                  <CardTitle className="text-lg mb-2">{game.name}</CardTitle>
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-1 text-sm text-gray-600">
                      <Users className="h-4 w-4" />
                      {game.players}
                    </div>
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
                  <Link href={`/games/${game.id}`}>
                    <Button className="w-full mt-3 bg-transparent" variant="outline">
                      Play Now
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Active Game Rooms */}
      <section className="py-12 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Active Game Rooms</h2>
          <div className="grid gap-4">
            {activeRooms.map((room) => (
              <Card key={room.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <Gamepad2 className="h-5 w-5 text-purple-600" />
                        <span className="font-semibold">{room.game}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Users className="h-4 w-4" />
                        <span>Host: {room.host}</span>
                      </div>
                      <Badge variant={room.type === "Public" ? "default" : "secondary"}>{room.type}</Badge>
                      <Badge variant="outline">AI: {room.ai}</Badge>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-gray-600">{room.players} players</span>
                      <Button size="sm">
                        {room.players.split("/")[0] === room.players.split("/")[1] ? "Spectate" : "Join"}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Why Choose AI Gaming Friend?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageCircle className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Smart AI Creation</h3>
              <p className="text-gray-600">
                Design AI friends with custom personalities using natural language prompts
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Personal Relationships</h3>
              <p className="text-gray-600">
                Build unique bonds with each AI friend through conversations and shared gaming experiences
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Flexible Gaming</h3>
              <p className="text-gray-600">
                Invite your AI friends to play with you as teammates or challenge them as opponents
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
