import { Component, inject, signal } from '@angular/core';
import { HttpClient, HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { environment } from '../../environments/environment';
import { AuthService } from '../auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-docente',
  imports: [HttpClientModule, FormsModule, CommonModule],
  templateUrl: './docente.html',
  styleUrl: './docente.css',
})
export class DocenteComponent {
  private http = inject(HttpClient);
  private authService = inject(AuthService);
  private router = inject(Router);

  private apiUrl = environment.apiUrl;

  studentName = '';
  subject = '';
  vote = 0;

  votes: any[] = [];
  subjects: string[] = [];
  students: string[] = [];
  note: string = '';
  loading = signal(false);
  error = signal('');
  successMessage = signal('');
  retryCount = signal(0);
  maxRetries = 3;

  ngOnInit() {
    this.loadVotes();
    this.loadSubjects();
    this.loadStudents();
  }

  loadSubjects() {
    this.http.get<string[]>(`${this.apiUrl}/subjects`).subscribe({
      next: (data) => {
        this.subjects = data;
        console.log('Materie caricate:', data);
      },
      error: (err: HttpErrorResponse) => {
        console.error('Errore nel caricamento delle materie:', err);
        // Non mostrare errore per le materie, usa input libero
      },
    });
  }

  loadStudents() {
    this.http.get<string[]>(`${this.apiUrl}/students`).subscribe({
      next: (data) => {
        this.students = data;
        console.log('Studenti caricati:', data);
      },
      error: (err: HttpErrorResponse) => {
        console.error('Errore nel caricamento degli studenti:', err);
        // Non mostrare errore per gli studenti, usa input libero
      },
    });
  }


  insertVote() {
    if (!this.studentName.trim() || !this.subject.trim() || !this.vote) {
      this.error.set('Per favore, compila tutti i campi obbligatori');
      return;
    }

    if (this.vote < 0 || this.vote > 10) {
      this.error.set('Il voto deve essere compreso tra 0 e 10');
      return;
    }

    if (this.studentName.trim().length < 2) {
      this.error.set('Il nome dello studente deve contenere almeno 2 caratteri');
      return;
    }

    if (this.subject.trim().length < 2) {
      this.error.set('La materia deve contenere almeno 2 caratteri');
      return;
    }

    this.loading.set(true);
    this.error.set('');
    this.successMessage.set('');

    const data = {
      student_name: this.studentName.trim(),
      subject: this.subject.trim(),
      vote: this.vote,
      note: this.note && this.note.trim() ? this.note.trim() : undefined,
    };

    this.http.post(`${this.apiUrl}/votes`, data).subscribe({
      next: (response) => {
        console.log('Voto inserito con successo:', response);
        this.successMessage.set('✅ Voto inserito con successo!');
        this.loadVotes();
        this.resetForm();
        this.loading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err: HttpErrorResponse) => {
        console.error('Errore nell\'inserimento del voto:', err);
        this.loading.set(false);

        if (err.status === 401) {
          this.error.set('Sessione scaduta. Rieffettua il login.');
          setTimeout(() => {
            this.authService.logout();
          }, 2000);
        } else if (err.status === 403) {
          this.error.set('Non hai i permessi per inserire voti.');
          this.router.navigate(['/accesso-negato']);
        } else if (err.status === 400) {
          this.error.set('Dati inseriti non validi. Verifica i campi.');
        } else if (err.status === 0 || err.status >= 500) {
          this.error.set('Errore del server. Riprova più tardi.');
        } else {
          this.error.set('Errore nell\'inserimento del voto. Riprova.');
        }
      },
    });
  }

  loadVotes(retry = false) {
    if (retry) {
      this.retryCount.update(count => count + 1);
    } else {
      this.retryCount.set(0);
    }

    this.loading.set(true);
    this.error.set('');

    this.http.get<any[]>(`${this.apiUrl}/votes`).subscribe({
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
          this.error.set('Sessione scaduta. Rieffettua il login.');
          setTimeout(() => {
            this.authService.logout();
          }, 2000);
        } else if (err.status === 403) {
          this.error.set('Non hai i permessi per visualizzare i voti.');
          this.router.navigate(['/accesso-negato']);
        } else if (err.status === 0 || err.status >= 500) {
          if (this.retryCount() < this.maxRetries) {
            this.error.set(`Errore di connessione. Tentativo ${this.retryCount() + 1}/${this.maxRetries}...`);
            setTimeout(() => this.loadVotes(true), 2000);
          } else {
            this.error.set('Impossibile caricare i voti. Riprova più tardi.');
          }
        } else {
          this.error.set('Errore nel caricamento dei voti. Riprova più tardi.');
        }
      },
    });
  }

  private resetForm() {
    this.studentName = '';
    this.subject = '';
    this.vote = 0;
    this.note = '';
  }

  retryLoad() {
    this.loadVotes();
  }

  logout() {
    this.authService.logout();
  }

  getVoteClass(vote: number): string {
    if (vote >= 9) return 'excellent';
    if (vote >= 7.5) return 'good';
    if (vote >= 6) return 'average';
    if (vote >= 4) return 'poor';
    return 'fail';
  }
}

