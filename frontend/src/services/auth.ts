import api from './api';

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  profile_image?: string;
}

export const authService = {
  async login(data: LoginData) {
    const response = await api.post('/auth/login/', data);
    const { access, refresh } = response.data;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    return response.data;
  },

  async register(data: RegisterData) {
    const response = await api.post('/register/', data);
    return response.data;
  },

  async verifyOTP(email: string, otp: string) {
    const response = await api.post('/auth/verify-otp/', { email, otp_code: otp });
    const { access, refresh } = response.data;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    return response.data;
  },

  async resendOTP(email: string) {
    const response = await api.post('/auth/resend-otp/', { email });
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },

  getToken(): string | null {
    return localStorage.getItem('access_token');
  },
};