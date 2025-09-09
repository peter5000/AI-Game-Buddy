import { apiRequest } from './index';
import { SignupRequest, SigninRequest, AuthResponse, ApiResponse } from '../types';

export async function signupUser(data: SignupRequest): Promise<ApiResponse<AuthResponse>> {
  return apiRequest<ApiResponse<AuthResponse>>('/accounts/register', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signinUser(data: SigninRequest): Promise<ApiResponse<AuthResponse>> {
  return apiRequest<ApiResponse<AuthResponse>>('/accounts/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signoutUser(): Promise<ApiResponse> {
  return apiRequest<ApiResponse>('/accounts/logout', {
    method: 'POST',
  });
}

export async function getCurrentUser(): Promise<ApiResponse<AuthResponse['user']>> {
  return apiRequest<ApiResponse<AuthResponse['user']>>('/accounts/user/me');
}

export async function refreshToken(): Promise<ApiResponse<{ success: boolean }>> {
  return apiRequest<ApiResponse<{ success: boolean }>>('/accounts/refresh', {
    method: 'POST',
  });
}

// Helper function to check if user is authenticated
export async function checkAuthStatus(): Promise<boolean> {
  try {
    await getCurrentUser();
    return true;
  } catch (error) {
    return false;
  }
}