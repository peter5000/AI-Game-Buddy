import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { Navbar } from "@/components/navbar";
import { QueryProvider } from "@/components/query-provider";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/toaster";
import { WebSocketProvider } from "@/components/websocket-provider";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "AI Gaming Friend",
    description: "Your AI companion for gaming adventures",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className={inter.className}>
                <QueryProvider>
                    <WebSocketProvider>
                        <ThemeProvider>
                            <Navbar />
                            <main>{children}</main>
                            <Toaster />
                        </ThemeProvider>
                    </WebSocketProvider>
                </QueryProvider>
            </body>
        </html>
    );
}
