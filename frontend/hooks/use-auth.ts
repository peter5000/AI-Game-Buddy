import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { checkAuthStatus } from '@/lib/api';

export function useAuth(redirectIfAuthenticated = false, redirectUrl = '/') {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function checkStatus() {
      try {
        const authStatus = await checkAuthStatus();
        setIsAuthenticated(authStatus);
        if (authStatus && redirectIfAuthenticated) {
          router.push(redirectUrl);
        }
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    }

    checkStatus();
  }, [redirectIfAuthenticated, redirectUrl, router]);

  return { isAuthenticated, isLoading };
}
