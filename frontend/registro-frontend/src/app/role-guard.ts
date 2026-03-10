import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './auth';

export const roleGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const requiredRole = route.data?.['role'];

  if (!auth.isLoggedIn()) {
    auth.login();
    return false;
  }

  if (requiredRole && !auth.hasRole(requiredRole)) {
    router.navigate(['/accesso-negato']);
    return false;
  }

  return true;
};
