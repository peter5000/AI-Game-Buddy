import { apiRequest } from './index';
import { SignupRequest, SigninRequest, User, ApiResponse } from '../types';

export async function signupUser(data: SignupRequest): Promise<User> {
  return apiRequest<User>('/accounts/register', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signinUser(data: SigninRequest): Promise<ApiResponse<User>> {
  return apiRequest<User>('/accounts/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signoutUser(): Promise<ApiResponse> {
  return apiRequest<ApiResponse>('/accounts/logout', {
    method: 'POST',
  });
}

export async function getCurrentUser(): Promise<ApiResponse<User>> {
  return apiRequest<ApiResponse<User>>('/accounts/user');
}

export async function refreshToken(): Promise<ApiResponse<{ success: boolean }>> {
  return apiRequest<ApiResponse<{ success: boolean }>>('/accounts/refresh', {
    method: 'POST',
  });
}

export async function checkAuth(): Promise<ApiResponse<{ status: string }>> {
  return apiRequest<ApiResponse<{ status: string }>>('/accounts/status');
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