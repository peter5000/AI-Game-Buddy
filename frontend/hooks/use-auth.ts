import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

function getCookie(name: string): string | null {
  if (typeof document === 'undefined') {
    return null;
  }
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null;
  }
  return null;
}

export function useAuth(redirectIfAuthenticated = false, redirectUrl = '/') {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const accessToken = getCookie('access_token');
    const refreshToken = getCookie('refresh_token');
    const authStatus = !!(accessToken || refreshToken);

    setIsAuthenticated(authStatus);

    if (authStatus && redirectIfAuthenticated) {
      router.push(redirectUrl);
    }

    setIsLoading(false);
  }, [redirectIfAuthenticated, redirectUrl, router]);

  return { isAuthenticated, isLoading };
}
