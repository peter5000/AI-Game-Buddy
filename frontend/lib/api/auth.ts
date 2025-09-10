import { apiRequest } from './index';
import { SignupRequest, SigninRequest, User, ApiResponse } from '../types';

export async function signupUser(data: SignupRequest): Promise<ApiResponse<User>> {
  return apiRequest<ApiResponse<User>>('/accounts/register', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signinUser(data: SigninRequest): Promise<ApiResponse<User>> {
  return apiRequest<ApiResponse<User>>('/accounts/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function signoutUser(): Promise<ApiResponse<void>> {
  return apiRequest<ApiResponse<void>>('/accounts/logout', {
    method: 'POST',
  });
}

export async function deleteUser(): Promise<ApiResponse<void>> {
  return apiRequest<ApiResponse<void>>('/accounts/delete', {
    method: 'DELETE',
  });
}

export async function getCurrentUser(): Promise<ApiResponse<User>> {
  return apiRequest<ApiResponse<User>>('/accounts/user', {
    method: 'GET',
  });
}

export async function refreshToken(): Promise<ApiResponse<void>> {
  return apiRequest<ApiResponse<void>>('/accounts/refresh', {
    method: 'POST',
  });
}

export async function checkAuth(): Promise<ApiResponse<void>> {
  return apiRequest<ApiResponse<void>>('/accounts/status', {
    method: 'GET',
  });
}
