import { apiRequest } from './index';
import { SignupRequest, SigninRequest, AuthResponse, ApiResponse, User } from '../types';

export async function signupUser(data: SignupRequest): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/register', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signinUser(data: SigninRequest): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signoutUser(): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/logout', {
    method: 'POST',
  });
}

export async function getCurrentUser(): Promise<User> {
  return apiRequest<User>('/accounts/user/me');
}

export async function refreshToken(): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/refresh', {
    method: 'POST',
  });
}

export async function checkAuth(): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/status');
}

// Helper function to check if user is authenticated
export async function checkAuthStatus(): Promise<boolean> {
  try {
    await checkAuth();
    return true;
  } catch (error) {
    return false;
  }
}