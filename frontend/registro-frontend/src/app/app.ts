import { Component, signal, inject, OnInit } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from './auth';


@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('Registro Elettronico');
  isLoading = signal(true);
  auth = inject(AuthService);
  private router = inject(Router);

  ngOnInit() {
    setTimeout(() => {
      this.isLoading.set(false);
      if (this.auth.isLoggedIn()) {
        if (this.auth.hasRole('docente')) {
          this.router.navigate(['/docente']);
        } else if (this.auth.hasRole('studente')) {
          this.router.navigate(['/studente']);
        }
      }
    }, 1000);
  }

  login() {
    console.log('🔐 Login clicked');
    this.auth.login();
  }

  logout() {
    console.log('🚪 Logout clicked');
    this.auth.logout();
  }
}
