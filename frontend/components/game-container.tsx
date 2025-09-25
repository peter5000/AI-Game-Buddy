import * as React from "react";

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

interface GameContainerProps {
    title: string;
    description: string;
    children: React.ReactNode;
}

export function GameContainer({
    title,
    description,
    children,
}: GameContainerProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>{title}</CardTitle>
                <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent>{children}</CardContent>
        </Card>
    );
}