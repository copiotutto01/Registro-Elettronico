import { Component, inject } from '@angular/core';
import { AuthService } from '../auth';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  private auth = inject(AuthService);

  loginAsDocente() {
    // For demo, we can set a hint or just login normally
    this.auth.login();
  }

  loginAsStudente() {
    this.auth.login();
  }
}
