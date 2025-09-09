import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { QueryProvider } from "@/components/query-provider";
import { Navbar } from "@/components/navbar";
import { Toaster } from "@/components/ui/toaster";
import { WebSocketProvider } from "@/components/websocket-provider";

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
        <WebSocketProvider>
          <QueryProvider>
            <ThemeProvider>
              <Navbar />
              <main>{children}</main>
              <Toaster />
            </ThemeProvider>
          </QueryProvider>
        </WebSocketProvider>
      </body>
    </html>
  );
}