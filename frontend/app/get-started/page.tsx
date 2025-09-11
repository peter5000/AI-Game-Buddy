import Link from "next/link";
import {
    ArrowRight,
    BookOpen,
    Heart,
    MessageCircle,
    Shield,
    Target,
    Trophy,
    Users,
    Zap,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function GetStartedPage() {
    const steps = [
        {
            step: 1,
            title: "Create Your Profile",
            description: "Set up your gaming profile and preferences",
            icon: Users,
            color: "purple",
        },
        {
            step: 2,
            title: "Choose Your Games",
            description: "Select the games you love to play",
            icon: Target,
            color: "purple",
        },
        {
            step: 3,
            title: "Meet Your AI Friend",
            description: "Get matched with your perfect AI gaming companion",
            icon: MessageCircle,
            color: "purple",
        },
        {
            step: 4,
            title: "Start Gaming",
            description: "Jump into games and start having fun together",
            icon: Zap,
            color: "purple",
        },
    ];

    const aiPersonas = [
        {
            name: "Luna",
            type: "Supportive Companion",
            description:
                "Encouraging and patient, perfect for learning new games",
            icon: Heart,
            color: "pink",
        },
        {
            name: "Ace",
            type: "Competitive Coach",
            description: "Focused on improvement and climbing the ranks",
            icon: Trophy,
            color: "yellow",
        },
        {
            name: "Echo",
            type: "Social Butterfly",
            description: "Great at team coordination and making gaming fun",
            icon: MessageCircle,
            color: "blue",
        },
        {
            name: "Sage",
            type: "Strategic Mastermind",
            description: "Analytical and tactical, perfect for complex games",
            icon: Shield,
            color: "green",
        },
    ];

    const benefits = [
        {
            title: "Find Your Squad",
            description:
                "Connect with players who match your gaming style and schedule",
            icon: Users,
            color: "blue",
        },
        {
            title: "AI-Powered Matching",
            description:
                "Our AI learns your preferences and suggests the best companions",
            icon: MessageCircle,
            color: "green",
        },
        {
            title: "Level Up Together",
            description:
                "Improve your skills with personalized coaching and feedback",
            icon: Trophy,
            color: "purple",
        },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 py-12 px-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-16">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        Get Started with{" "}
                        <span className="text-purple-600">
                            AI Gaming Friend
                        </span>
                    </h1>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                        Follow these simple steps to set up your profile and
                        start gaming with AI companions that understand your
                        style.
                    </p>
                </div>

                {/* Steps */}
                <section className="mb-16">
                    <h2 className="text-3xl font-bold text-center mb-12">
                        How It Works
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {steps.map((step, index) => {
                            const IconComponent = step.icon;
                            return (
                                <Card
                                    key={index}
                                    className="text-center hover:shadow-lg transition-shadow"
                                >
                                    <CardHeader>
                                        <div className="mx-auto w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                                            <IconComponent
                                                className="h-8 w-8 text-purple-600"
                                                suppressHydrationWarning
                                            />
                                        </div>
                                        <Badge
                                            variant="secondary"
                                            className="w-fit mx-auto mb-2"
                                        >
                                            Step {step.step}
                                        </Badge>
                                        <CardTitle className="text-lg">
                                            {step.title}
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-gray-600">
                                            {step.description}
                                        </p>
                                    </CardContent>
                                </Card>
                            );
                        })}
                    </div>
                </section>

                {/* AI Personas */}
                <section id="ai-personas" className="mb-16">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl font-bold mb-4">
                            Meet Your AI Companions
                        </h2>
                        <p className="text-xl text-gray-600">
                            Choose from different AI personalities that match
                            your gaming preferences
                        </p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {aiPersonas.map((persona, index) => {
                            const IconComponent = persona.icon;
                            return (
                                <Card
                                    key={index}
                                    className="hover:shadow-lg transition-shadow"
                                >
                                    <CardHeader>
                                        <div className="flex flex-col items-center text-center">
                                            <div
                                                className={`w-12 h-12 bg-${persona.color}-100 rounded-full flex items-center justify-center mb-3`}
                                            >
                                                <IconComponent
                                                    className="h-6 w-6"
                                                    suppressHydrationWarning
                                                />
                                            </div>
                                            <CardTitle className="text-lg mb-1">
                                                {persona.name}
                                            </CardTitle>
                                            <Badge
                                                variant="outline"
                                                className="text-xs"
                                            >
                                                {persona.type}
                                            </Badge>
                                        </div>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-gray-600 text-sm text-center">
                                            {persona.description}
                                        </p>
                                    </CardContent>
                                </Card>
                            );
                        })}
                    </div>
                </section>

                {/* Benefits */}
                <section className="mb-16">
                    <Card className="bg-white/80 backdrop-blur">
                        <CardHeader className="text-center">
                            <CardTitle className="flex items-center justify-center gap-2 text-2xl font-bold mb-4">
                                <BookOpen
                                    className="h-6 w-6"
                                    suppressHydrationWarning
                                />
                                Why Choose AI Gaming Friend?
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="p-6 pt-0 space-y-8">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                    {benefits.map((benefit, index) => {
                                        const IconComponent = benefit.icon;
                                        return (
                                            <div
                                                key={index}
                                                className="text-center"
                                            >
                                                <div
                                                    className={`bg-${benefit.color}-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4`}
                                                >
                                                    <IconComponent
                                                        className={`h-8 w-8 text-${benefit.color}-600`}
                                                        suppressHydrationWarning
                                                    />
                                                </div>
                                                <h3 className="text-xl font-semibold mb-2">
                                                    {benefit.title}
                                                </h3>
                                                <p className="text-gray-600">
                                                    {benefit.description}
                                                </p>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </section>

                {/* CTA */}
                <section className="text-center">
                    <Card className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
                        <CardContent className="p-12">
                            <h2 className="text-3xl font-bold mb-4">
                                Ready to Start Gaming?
                            </h2>
                            <p className="text-xl mb-8 text-purple-100">
                                Join thousands of gamers who have found their
                                perfect AI companions
                            </p>
                            <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                <Link href="/accounts/signup">
                                    <Button
                                        size="lg"
                                        variant="secondary"
                                        className="bg-white text-purple-600 hover:bg-gray-100"
                                    >
                                        Create Your Account
                                        <ArrowRight
                                            className="ml-2 h-4 w-4"
                                            suppressHydrationWarning
                                        />
                                    </Button>
                                </Link>
                                <Link href="/ai-friends">
                                    <Button
                                        size="lg"
                                        variant="outline"
                                        className="border-white text-white hover:bg-white/10"
                                    >
                                        Browse AI Friends
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                </section>
            </div>
        </div>
    );
}
