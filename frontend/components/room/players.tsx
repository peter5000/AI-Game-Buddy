import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Crown, Mic } from "lucide-react";

interface PlayersProps {
    users: string[];
    creatorId: string;
}

export function Players({ users, creatorId }: PlayersProps) {
    return (
        <Card className="mb-4">
            <CardHeader>
                <CardTitle>Players</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {users.map((user, index) => (
                    <div key={user} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Avatar>
                                <AvatarImage src="/placeholder-user.jpg" />
                                <AvatarFallback>P{index + 1}</AvatarFallback>
                            </Avatar>
                            {/* NOTE: Using index for player number, would be better to have usernames */}
                            <span>
                                Player {index + 1} ({user.substring(0, 6)}...)
                            </span>
                            {user === creatorId && (
                                <Crown className="h-5 w-5 text-yellow-500" />
                            )}
                        </div>
                        <div className="flex items-center gap-2">
                            <Mic className="h-5 w-5" />
                        </div>
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}