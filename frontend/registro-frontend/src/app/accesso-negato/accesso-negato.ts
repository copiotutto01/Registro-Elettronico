import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth';

@Component({
  selector: 'app-accesso-negato',
  imports: [],
  templateUrl: './accesso-negato.html',
  styleUrl: './accesso-negato.css',
})
export class AccessoNegatoComponent {
  private router = inject(Router);
  private authService = inject(AuthService);

  goHome() {
    this.router.navigate(['/']);
  }

  logout() {
    this.authService.logout();
  }
}
