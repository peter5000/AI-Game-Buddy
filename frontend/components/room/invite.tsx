"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Copy, Share2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface InviteProps {
    roomId: string;
}

export function Invite({ roomId }: InviteProps) {
    const { toast } = useToast();
    const inviteLink = `${window.location.origin}/room/${roomId}`;

    const handleCopy = () => {
        navigator.clipboard.writeText(inviteLink).then(
            () => {
                toast({
                    title: "Copied to clipboard!",
                    description: "Invite link has been copied.",
                });
            },
            (err) => {
                console.error("Could not copy text: ", err);
                toast({
                    title: "Failed to copy",
                    description: "Could not copy the link to your clipboard.",
                    variant: "destructive",
                });
            },
        );
    };

    return (
        <Card className="mb-4">
            <CardHeader>
                <CardTitle>Invite</CardTitle>
            </CardHeader>
            <CardContent className="flex gap-2">
                <Input readOnly value={inviteLink} />
                <Button variant="outline" size="icon" onClick={handleCopy}>
                    <Copy className="h-5 w-5" />
                </Button>
                <Button variant="outline" size="icon">
                    <Share2 className="h-5 w-5" />
                </Button>
            </CardContent>
        </Card>
    );
}