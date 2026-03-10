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
    console.log('🚀 App initialized');
    console.log('Auth service ready:', !!this.auth);

    // Mostra caricamento per 2 secondi per permettere a Keycloak di inizializzarsi
    setTimeout(() => {
      this.isLoading.set(false);
      console.log('✅ App loaded - isLoading=false');
      console.log('User authenticated:', this.auth.isLoggedIn());
      if (this.auth.isLoggedIn()) {
        console.log('Username:', this.auth.getUsername());
      }
    }, 2000);
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
