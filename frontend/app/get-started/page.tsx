import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Users, MessageCircle, Trophy, Shield, Heart, Zap, Target } from "lucide-react"
import Link from "next/link"

export default function GetStartedPage() {
  const steps = [
    {
      step: 1,
      title: "Create Your Account",
      description: "Sign up for free and customize your gaming profile",
      icon: Users,
      action: "Sign Up Now",
      link: "/auth/signup",
    },
    {
      step: 2,
      title: "Choose Your First Game",
      description: "Browse our game library and pick something that interests you",
      icon: Target,
      action: "Browse Games",
      link: "/games",
    },
    {
      step: 3,
      title: "Select AI Personality",
      description: "Choose an AI companion that matches your playing style",
      icon: MessageCircle,
      action: "Learn About AI",
      link: "#ai-personalities",
    },
    {
      step: 4,
      title: "Start Playing",
      description: "Jump into your first game and start having fun!",
      icon: Zap,
      action: "Play Now",
      link: "/games",
    },
  ]

  const aiPersonalities = [
    {
      name: "Friendly",
      description: "Encouraging and supportive, perfect for learning new games",
      traits: ["Positive reinforcement", "Helpful tips", "Patient teaching"],
      icon: Heart,
      color: "bg-green-100 text-green-600",
    },
    {
      name: "Competitive",
      description: "Challenging and strategic, pushes you to improve your skills",
      traits: ["Advanced strategies", "Tactical analysis", "Skill development"],
      icon: Trophy,
      color: "bg-blue-100 text-blue-600",
    },
    {
      name: "Trash Talk",
      description: "Playful banter and witty remarks for entertaining matches",
      traits: ["Humorous comments", "Playful rivalry", "Entertainment focused"],
      icon: MessageCircle,
      color: "bg-purple-100 text-purple-600",
    },
    {
      name: "Neutral",
      description: "Focused purely on gameplay without personality distractions",
      traits: ["Game-focused", "Minimal chatter", "Pure strategy"],
      icon: Shield,
      color: "bg-gray-100 text-gray-600",
    },
  ]

  const policies = [
    {
      title: "Good Sportsmanship",
      points: [
        "Treat all players with respect and courtesy",
        "Accept wins and losses gracefully",
        "No harassment, bullying, or toxic behavior",
        "Help new players learn and improve",
      ],
    },
    {
      title: "Fair Play",
      points: [
        "No cheating, exploiting, or using unfair advantages",
        "Play games as intended by the rules",
        "Report suspicious behavior to moderators",
        "Respect the AI companions and other players",
      ],
    },
    {
      title: "Community Guidelines",
      points: [
        "Keep conversations appropriate for all ages",
        "No spam, advertising, or self-promotion",
        "Respect privacy and personal information",
        "Follow game-specific rules and etiquette",
      ],
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Get Started with AI Gaming Friend</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Welcome to the future of gaming! Learn how to make the most of your AI gaming companions and start your
            journey to becoming a better player.
          </p>
        </div>

        {/* Getting Started Steps */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">How to Get Started</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((step) => {
              const IconComponent = step.icon
              return (
                <Card key={step.step} className="text-center hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="mx-auto w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                      <IconComponent className="h-8 w-8 text-purple-600" />
                    </div>
                    <Badge variant="secondary" className="w-fit mx-auto mb-2">
                      Step {step.step}
                    </Badge>
                    <CardTitle className="text-lg">{step.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="mb-4">{step.description}</CardDescription>
                    <Link href={step.link}>
                      <Button variant="outline" size="sm">
                        {step.action}
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </section>

        {/* AI Personalities */}
        <section id="ai-personalities" className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Meet Your AI Companions</h2>
            <p className="text-gray-600 max-w-3xl mx-auto">
              Choose from different AI personalities that match your gaming style and preferences. Each AI has unique
              traits and communication styles.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {aiPersonalities.map((ai) => {
              const IconComponent = ai.icon
              return (
                <Card key={ai.name} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center gap-4">
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center ${ai.color}`}>
                        <IconComponent className="h-6 w-6" />
                      </div>
                      <div>
                        <CardTitle>{ai.name}</CardTitle>
                        <CardDescription>{ai.description}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <h4 className="font-medium text-sm">Key Traits:</h4>
                      <ul className="space-y-1">
                        {ai.traits.map((trait, index) => (
                          <li key={index} className="text-sm text-gray-600 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 bg-purple-600 rounded-full" />
                            {trait}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </section>

        {/* How It Works */}
        <section className="mb-16">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-6 w-6" />
                How AI Gaming Friend Works
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Users className="h-8 w-8 text-blue-600" />
                  </div>
                  <h3 className="font-semibold mb-2">Smart Matchmaking</h3>
                  <p className="text-sm text-gray-600">
                    Our AI analyzes your skill level and preferences to match you with the perfect gaming companions.
                  </p>
                </div>
                <div className="text-center">
                  <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <MessageCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <h3 className="font-semibold mb-2">Dynamic Conversations</h3>
                  <p className="text-sm text-gray-600">
                    AI companions engage in natural conversations, provide tips, and adapt to your communication style.
                  </p>
                </div>
                <div className="text-center">
                  <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Trophy className="h-8 w-8 text-purple-600" />
                  </div>
                  <h3 className="font-semibold mb-2">Skill Development</h3>
                  <p className="text-sm text-gray-600">
                    Track your progress, earn achievements, and improve your gaming skills with personalized feedback.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Community Policies */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Community Policies</h2>
            <p className="text-gray-600 max-w-3xl mx-auto">
              To ensure everyone has a great experience, please follow our community guidelines and policies.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {policies.map((policy) => (
              <Card key={policy.title}>
                <CardHeader>
                  <CardTitle className="text-lg">{policy.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {policy.points.map((point, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-purple-600 rounded-full mt-2 flex-shrink-0" />
                        {point}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Call to Action */}
        <section className="text-center">
          <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
            <CardContent className="pt-8 pb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Ready to Start Gaming?</h2>
              <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
                Join thousands of players who are already enjoying games with their AI companions. Create your account
                today and discover your new favorite gaming partner!
              </p>
              <div className="flex gap-4 justify-center">
                <Link href="/auth/signup">
                  <Button size="lg">Create Free Account</Button>
                </Link>
                <Link href="/games">
                  <Button size="lg" variant="outline">
                    Browse Games
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  )
}
