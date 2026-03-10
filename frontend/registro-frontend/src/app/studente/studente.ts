import { Component, inject, signal } from '@angular/core';
import { HttpClient, HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { environment } from '../../environments/environment';
import { AuthService } from '../auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-studente',
  imports: [HttpClientModule, CommonModule],
  templateUrl: './studente.html',
  styleUrl: './studente.css',
})
export class StudenteComponent {
  private http = inject(HttpClient);
  private authService = inject(AuthService);
  private router = inject(Router);

  private apiUrl = environment.apiUrl;

  votes: any[] = [];
  loading = signal(false);
  error = signal('');
  retryCount = signal(0);
  maxRetries = 3;

  ngOnInit() {
    this.loadMyVotes();
  }

  loadMyVotes(retry = false) {
    if (retry) {
      this.retryCount.update(count => count + 1);
    } else {
      this.retryCount.set(0);
    }

    this.loading.set(true);
    this.error.set('');

    this.http.get<any[]>(`${this.apiUrl}/my-votes`).subscribe({
      next: (data) => {
        this.votes = data;
        this.loading.set(false);
        this.retryCount.set(0);
        console.log('Voti caricati con successo:', data);
      },
      error: (err: HttpErrorResponse) => {
        console.error('Errore nel caricamento dei voti:', err);
        this.loading.set(false);

        if (err.status === 401) {
          // Token scaduto o non valido
          this.error.set('Sessione scaduta. Rieffettua il login.');
          setTimeout(() => {
            this.authService.logout();
          }, 2000);
        } else if (err.status === 403) {
          // Non autorizzato
          this.error.set('Non hai i permessi per visualizzare questi dati.');
          this.router.navigate(['/accesso-negato']);
        } else if (err.status === 0 || err.status >= 500) {
          // Errore di rete o server
          if (this.retryCount() < this.maxRetries) {
            this.error.set(`Errore di connessione. Tentativo ${this.retryCount() + 1}/${this.maxRetries}...`);
            setTimeout(() => this.loadMyVotes(true), 2000);
          } else {
            this.error.set('Impossibile caricare i voti. Riprova più tardi o contatta l\'amministratore.');
          }
        } else {
          // Altri errori
          this.error.set('Errore nel caricamento dei tuoi voti. Riprova più tardi.');
        }
      },
    });
  }

  calculateAverage(): number {
    if (this.votes.length === 0) return 0;
    const sum = this.votes.reduce((acc, v) => acc + v.vote, 0);
    return Math.round((sum / this.votes.length) * 100) / 100;
  }

  retryLoad() {
    this.loadMyVotes();
  }

  logout() {
    this.authService.logout();
  }
}
