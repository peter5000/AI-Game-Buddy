"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ArrowLeft, Send, Gamepad2, Settings, MoreVertical } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import Link from "next/link"

interface Message {
  id: number
  sender: "user" | "ai"
  content: string
  timestamp: Date
}

export default function AIFriendChatPage({ params }: { params: { id: string } }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: "ai",
      content: "Hey there! I'm excited to chat with you. How are you feeling about our next game?",
      timestamp: new Date(Date.now() - 1000 * 60 * 5),
    },
    {
      id: 2,
      sender: "user",
      content: "I'm ready for a challenge! Want to play some chess?",
      timestamp: new Date(Date.now() - 1000 * 60 * 3),
    },
    {
      id: 3,
      sender: "ai",
      content: "I've been analyzing some new opening strategies. This should be interesting! 🎯 Ready when you are.",
      timestamp: new Date(Date.now() - 1000 * 60 * 2),
    },
  ])

  const [newMessage, setNewMessage] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Mock AI friend data
  const aiFriend = {
    id: params.id,
    name: "Chess Master Alex",
    personality: "Strategic and analytical, loves discussing chess theory and tactics",
    avatar: "/placeholder.svg?height=80&width=80",
    status: "online",
    relationship: "Close Friend",
    difficulty: "Expert",
    traits: ["Strategic", "Patient", "Encouraging"],
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!newMessage.trim()) return

    const userMessage: Message = {
      id: messages.length + 1,
      sender: "user",
      content: newMessage,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setNewMessage("")
    setIsTyping(true)

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: messages.length + 2,
        sender: "ai",
        content: generateAIResponse(newMessage),
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiResponse])
      setIsTyping(false)
    }, 1500)
  }

  const generateAIResponse = (userMessage: string): string => {
    // Simple response generation based on keywords
    const lowerMessage = userMessage.toLowerCase()

    if (lowerMessage.includes("game") || lowerMessage.includes("play")) {
      return "I'd love to play! What game are you in the mood for? I've been practicing my chess strategies lately. 🎮"
    }
    if (lowerMessage.includes("chess")) {
      return "Chess is my favorite! I've been studying the Sicilian Defense recently. Want to try it out in our next match? ♟️"
    }
    if (lowerMessage.includes("strategy")) {
      return "Strategy is everything! I always think three moves ahead. What's your favorite strategic approach?"
    }
    if (lowerMessage.includes("hello") || lowerMessage.includes("hi")) {
      return "Hello! Great to see you again. Ready for another exciting gaming session? 😊"
    }

    return "That's interesting! I enjoy our conversations. They help me understand your playing style better. What do you think about trying a new game together?"
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white border-b px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/ai-friends">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="h-4 w-4" />
                </Button>
              </Link>
              <Avatar className="w-10 h-10">
                <AvatarImage src={aiFriend.avatar || "/placeholder.svg"} />
                <AvatarFallback>AM</AvatarFallback>
              </Avatar>
              <div>
                <h1 className="font-semibold">{aiFriend.name}</h1>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-600">Online</span>
                  <Badge variant="secondary" className="text-xs">
                    {aiFriend.relationship}
                  </Badge>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Link href={`/ai-friends/${aiFriend.id}/invite`}>
                <Button size="sm">
                  <Gamepad2 className="mr-2 h-4 w-4" />
                  Invite to Game
                </Button>
              </Link>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem asChild>
                    <Link href={`/ai-friends/${aiFriend.id}/edit`}>
                      <Settings className="mr-2 h-4 w-4" />
                      Edit AI Friend
                    </Link>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 bg-white">
          <ScrollArea className="h-[calc(100vh-200px)] p-4">
            <div className="space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`flex gap-3 max-w-[70%] ${message.sender === "user" ? "flex-row-reverse" : ""}`}>
                    <Avatar className="w-8 h-8 flex-shrink-0">
                      {message.sender === "ai" ? (
                        <>
                          <AvatarImage src={aiFriend.avatar || "/placeholder.svg"} />
                          <AvatarFallback>AM</AvatarFallback>
                        </>
                      ) : (
                        <>
                          <AvatarImage src="/placeholder.svg?height=32&width=32" />
                          <AvatarFallback>You</AvatarFallback>
                        </>
                      )}
                    </Avatar>
                    <div className={`space-y-1 ${message.sender === "user" ? "text-right" : ""}`}>
                      <div
                        className={`rounded-lg px-4 py-2 ${
                          message.sender === "user" ? "bg-purple-600 text-white" : "bg-gray-100 text-gray-900"
                        }`}
                      >
                        {message.content}
                      </div>
                      <p className="text-xs text-gray-500">{formatTime(message.timestamp)}</p>
                    </div>
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex justify-start">
                  <div className="flex gap-3 max-w-[70%]">
                    <Avatar className="w-8 h-8">
                      <AvatarImage src={aiFriend.avatar || "/placeholder.svg"} />
                      <AvatarFallback>AM</AvatarFallback>
                    </Avatar>
                    <div className="bg-gray-100 rounded-lg px-4 py-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div
                          className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                          style={{ animationDelay: "0.1s" }}
                        ></div>
                        <div
                          className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                          style={{ animationDelay: "0.2s" }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div ref={messagesEndRef} />
          </ScrollArea>
        </div>

        {/* Message Input */}
        <div className="bg-white border-t p-4">
          <div className="flex gap-2">
            <Input
              placeholder={`Message ${aiFriend.name}...`}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button onClick={sendMessage} disabled={!newMessage.trim() || isTyping}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
