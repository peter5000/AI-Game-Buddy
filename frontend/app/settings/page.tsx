"use client";

import { Bell, Camera, Shield, Trash2, User } from "lucide-react";
import { useState } from "react";

import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function SettingsPage() {
    const [profile, setProfile] = useState({
        username: "GameMaster2024",
        email: "gamemaster@example.com",
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
    });

    const [notifications, setNotifications] = useState({
        gameInvites: true,
        gameResults: true,
        achievements: true,
        friendRequests: true,
        emailNotifications: false,
        pushNotifications: true,
    });

    const [privacy, setPrivacy] = useState({
        profileVisibility: "public",
        gameHistoryVisibility: "friends",
        onlineStatus: true,
        allowFriendRequests: true,
    });

    const handleProfileUpdate = (field: string, value: string) => {
        setProfile((prev) => ({ ...prev, [field]: value }));
    };

    const handleNotificationToggle = (field: string, value: boolean) => {
        setNotifications((prev) => ({ ...prev, [field]: value }));
    };

    const handlePrivacyUpdate = (field: string, value: string | boolean) => {
        setPrivacy((prev) => ({ ...prev, [field]: value }));
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Settings
                    </h1>
                    <p className="text-gray-600 mt-2">
                        Manage your account preferences and privacy settings
                    </p>
                </div>

                <Tabs defaultValue="profile" className="space-y-6">
                    <TabsList className="grid w-full grid-cols-4">
                        <TabsTrigger value="profile">Profile</TabsTrigger>
                        <TabsTrigger value="notifications">
                            Notifications
                        </TabsTrigger>
                        <TabsTrigger value="privacy">Privacy</TabsTrigger>
                        <TabsTrigger value="account">Account</TabsTrigger>
                    </TabsList>

                    <TabsContent value="profile" className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <User className="h-5 w-5" />
                                    Profile Information
                                </CardTitle>
                                <CardDescription>
                                    Update your profile details and avatar
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="flex items-center gap-6">
                                    <Avatar className="w-20 h-20">
                                        <AvatarImage src="/placeholder.svg?height=80&width=80" />
                                        <AvatarFallback className="text-xl">
                                            GM
                                        </AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <Button
                                            variant="outline"
                                            className="mb-2 bg-transparent"
                                        >
                                            <Camera className="mr-2 h-4 w-4" />
                                            Change Avatar
                                        </Button>
                                        <p className="text-sm text-gray-600">
                                            JPG, PNG or GIF. Max size 2MB.
                                        </p>
                                    </div>
                                </div>

                                <Separator />

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="username">
                                            Username
                                        </Label>
                                        <Input
                                            id="username"
                                            value={profile.username}
                                            onChange={(e) =>
                                                handleProfileUpdate(
                                                    "username",
                                                    e.target.value
                                                )
                                            }
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="email">Email</Label>
                                        <Input
                                            id="email"
                                            type="email"
                                            value={profile.email}
                                            onChange={(e) =>
                                                handleProfileUpdate(
                                                    "email",
                                                    e.target.value
                                                )
                                            }
                                        />
                                    </div>
                                </div>

                                <Button>Save Changes</Button>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Change Password</CardTitle>
                                <CardDescription>
                                    Update your password to keep your account
                                    secure
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="current-password">
                                        Current Password
                                    </Label>
                                    <Input
                                        id="current-password"
                                        type="password"
                                        value={profile.currentPassword}
                                        onChange={(e) =>
                                            handleProfileUpdate(
                                                "currentPassword",
                                                e.target.value
                                            )
                                        }
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="new-password">
                                        New Password
                                    </Label>
                                    <Input
                                        id="new-password"
                                        type="password"
                                        value={profile.newPassword}
                                        onChange={(e) =>
                                            handleProfileUpdate(
                                                "newPassword",
                                                e.target.value
                                            )
                                        }
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="confirm-password">
                                        Confirm New Password
                                    </Label>
                                    <Input
                                        id="confirm-password"
                                        type="password"
                                        value={profile.confirmPassword}
                                        onChange={(e) =>
                                            handleProfileUpdate(
                                                "confirmPassword",
                                                e.target.value
                                            )
                                        }
                                    />
                                </div>
                                <Button>Update Password</Button>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="notifications" className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Bell className="h-5 w-5" />
                                    Notification Preferences
                                </CardTitle>
                                <CardDescription>
                                    Choose what notifications you want to
                                    receive
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="game-invites">
                                                Game Invitations
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Get notified when someone
                                                invites you to a game
                                            </p>
                                        </div>
                                        <Switch
                                            id="game-invites"
                                            checked={notifications.gameInvites}
                                            onCheckedChange={(checked) =>
                                                handleNotificationToggle(
                                                    "gameInvites",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="game-results">
                                                Game Results
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Notifications about your game
                                                outcomes
                                            </p>
                                        </div>
                                        <Switch
                                            id="game-results"
                                            checked={notifications.gameResults}
                                            onCheckedChange={(checked) =>
                                                handleNotificationToggle(
                                                    "gameResults",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="achievements">
                                                Achievements
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Get notified when you unlock new
                                                achievements
                                            </p>
                                        </div>
                                        <Switch
                                            id="achievements"
                                            checked={notifications.achievements}
                                            onCheckedChange={(checked) =>
                                                handleNotificationToggle(
                                                    "achievements",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="friend-requests">
                                                Friend Requests
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Notifications for new friend
                                                requests
                                            </p>
                                        </div>
                                        <Switch
                                            id="friend-requests"
                                            checked={
                                                notifications.friendRequests
                                            }
                                            onCheckedChange={(checked) =>
                                                handleNotificationToggle(
                                                    "friendRequests",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>
                                </div>

                                <Separator />

                                <div className="space-y-4">
                                    <h4 className="font-medium">
                                        Delivery Methods
                                    </h4>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="email-notifications">
                                                Email Notifications
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Receive notifications via email
                                            </p>
                                        </div>
                                        <Switch
                                            id="email-notifications"
                                            checked={
                                                notifications.emailNotifications
                                            }
                                            onCheckedChange={(checked) =>
                                                handleNotificationToggle(
                                                    "emailNotifications",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="push-notifications">
                                                Push Notifications
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Receive browser push
                                                notifications
                                            </p>
                                        </div>
                                        <Switch
                                            id="push-notifications"
                                            checked={
                                                notifications.pushNotifications
                                            }
                                            onCheckedChange={(checked) =>
                                                handleNotificationToggle(
                                                    "pushNotifications",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="privacy" className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Shield className="h-5 w-5" />
                                    Privacy Settings
                                </CardTitle>
                                <CardDescription>
                                    Control who can see your information and
                                    activity
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="profile-visibility">
                                            Profile Visibility
                                        </Label>
                                        <Select
                                            value={privacy.profileVisibility}
                                            onValueChange={(value) =>
                                                handlePrivacyUpdate(
                                                    "profileVisibility",
                                                    value
                                                )
                                            }
                                        >
                                            <SelectTrigger>
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="public">
                                                    Public - Anyone can view
                                                </SelectItem>
                                                <SelectItem value="friends">
                                                    Friends Only
                                                </SelectItem>
                                                <SelectItem value="private">
                                                    Private - Only you
                                                </SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="game-history-visibility">
                                            Game History Visibility
                                        </Label>
                                        <Select
                                            value={
                                                privacy.gameHistoryVisibility
                                            }
                                            onValueChange={(value) =>
                                                handlePrivacyUpdate(
                                                    "gameHistoryVisibility",
                                                    value
                                                )
                                            }
                                        >
                                            <SelectTrigger>
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="public">
                                                    Public - Anyone can view
                                                </SelectItem>
                                                <SelectItem value="friends">
                                                    Friends Only
                                                </SelectItem>
                                                <SelectItem value="private">
                                                    Private - Only you
                                                </SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="online-status">
                                                Show Online Status
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Let others see when you&apos;re
                                                online
                                            </p>
                                        </div>
                                        <Switch
                                            id="online-status"
                                            checked={privacy.onlineStatus}
                                            onCheckedChange={(checked) =>
                                                handlePrivacyUpdate(
                                                    "onlineStatus",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div>
                                            <Label htmlFor="friend-requests">
                                                Allow Friend Requests
                                            </Label>
                                            <p className="text-sm text-gray-600">
                                                Allow other players to send you
                                                friend requests
                                            </p>
                                        </div>
                                        <Switch
                                            id="friend-requests"
                                            checked={
                                                privacy.allowFriendRequests
                                            }
                                            onCheckedChange={(checked) =>
                                                handlePrivacyUpdate(
                                                    "allowFriendRequests",
                                                    checked
                                                )
                                            }
                                        />
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="account" className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Account Management</CardTitle>
                                <CardDescription>
                                    Manage your account settings and data
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="space-y-4">
                                    <div>
                                        <h4 className="font-medium mb-2">
                                            Export Data
                                        </h4>
                                        <p className="text-sm text-gray-600 mb-3">
                                            Download a copy of your game
                                            history, stats, and profile data
                                        </p>
                                        <Button variant="outline">
                                            Download My Data
                                        </Button>
                                    </div>

                                    <Separator />

                                    <div>
                                        <h4 className="font-medium mb-2">
                                            Clear Game History
                                        </h4>
                                        <p className="text-sm text-gray-600 mb-3">
                                            Remove all your game history and
                                            statistics (this cannot be undone)
                                        </p>
                                        <AlertDialog>
                                            <AlertDialogTrigger asChild>
                                                <Button
                                                    variant="outline"
                                                    className="text-orange-600 border-orange-600 hover:bg-orange-50 bg-transparent"
                                                >
                                                    Clear History
                                                </Button>
                                            </AlertDialogTrigger>
                                            <AlertDialogContent>
                                                <AlertDialogHeader>
                                                    <AlertDialogTitle>
                                                        Clear Game History
                                                    </AlertDialogTitle>
                                                    <AlertDialogDescription>
                                                        This will permanently
                                                        delete all your game
                                                        history, statistics, and
                                                        achievements. This
                                                        action cannot be undone.
                                                    </AlertDialogDescription>
                                                </AlertDialogHeader>
                                                <AlertDialogFooter>
                                                    <AlertDialogCancel>
                                                        Cancel
                                                    </AlertDialogCancel>
                                                    <AlertDialogAction className="bg-orange-600 hover:bg-orange-700">
                                                        Clear History
                                                    </AlertDialogAction>
                                                </AlertDialogFooter>
                                            </AlertDialogContent>
                                        </AlertDialog>
                                    </div>

                                    <Separator />

                                    <div>
                                        <h4 className="font-medium mb-2 text-red-600">
                                            Danger Zone
                                        </h4>
                                        <p className="text-sm text-gray-600 mb-3">
                                            Permanently delete your account and
                                            all associated data
                                        </p>
                                        <AlertDialog>
                                            <AlertDialogTrigger asChild>
                                                <Button variant="destructive">
                                                    <Trash2 className="mr-2 h-4 w-4" />
                                                    Delete Account
                                                </Button>
                                            </AlertDialogTrigger>
                                            <AlertDialogContent>
                                                <AlertDialogHeader>
                                                    <AlertDialogTitle>
                                                        Delete Account
                                                    </AlertDialogTitle>
                                                    <AlertDialogDescription>
                                                        This will permanently
                                                        delete your account,
                                                        game history,
                                                        statistics, and all
                                                        associated data. This
                                                        action cannot be undone.
                                                    </AlertDialogDescription>
                                                </AlertDialogHeader>
                                                <AlertDialogFooter>
                                                    <AlertDialogCancel>
                                                        Cancel
                                                    </AlertDialogCancel>
                                                    <AlertDialogAction className="bg-red-600 hover:bg-red-700">
                                                        Delete Account
                                                    </AlertDialogAction>
                                                </AlertDialogFooter>
                                            </AlertDialogContent>
                                        </AlertDialog>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}
