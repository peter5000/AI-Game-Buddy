// Common API response structure
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: Record<string, string[]>;
}

// Auth types
export interface User {
  id: string;
  email: string;
  username: string;
  avatar?: string;
  createdAt: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  username: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// Game types
export interface Game {
  id: string;
  name: string;
  description: string;
  image: string;
  category: string;
  playerCount: {
    min: number;
    max: number;
  };
}

// AI Friend types
export interface AIFriend {
  id: string;
  name: string;
  personality: string;
  description: string;
  avatar: string;
  specialties: string[];
}