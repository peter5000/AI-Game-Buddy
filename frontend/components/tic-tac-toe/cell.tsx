"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { CellValue } from "@/types/games/ulttt.types";

type Props = {
    value: CellValue;
    onClick: () => void;
    isClickable: boolean;
};

export function Cell({ value, onClick, isClickable }: Props) {
    return (
        <Button
            variant="outline"
            className={cn(
                "h-24 w-24 rounded-none border border-slate-300 text-6xl",
                value === "X" ? "text-blue-500" : "text-red-500"
            )}
            onClick={onClick}
            disabled={!isClickable}
        >
            {value}
        </Button>
    );
}
