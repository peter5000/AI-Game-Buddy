import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { checkAuth } from '@/lib/api';
import { useEffect } from 'react';

export function useAuth(redirectIfAuthenticated = false, redirectUrl = '/') {
  const router = useRouter();

  const { data, isLoading, isSuccess } = useQuery({
    queryKey: ['authStatus'],
    queryFn: checkAuth,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: false,
    refetchOnWindowFocus: false,
  });

  const isAuthenticated = isSuccess && data?.message === 'authenticated';

  useEffect(() => {
    if (isAuthenticated && redirectIfAuthenticated) {
      router.push(redirectUrl);
    }
  }, [isAuthenticated, redirectIfAuthenticated, redirectUrl, router]);

  return { isAuthenticated, isLoading };
}
