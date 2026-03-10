import { Routes } from '@angular/router';
import { roleGuard } from './role-guard';
import { DocenteComponent } from './docente/docente';
import { StudenteComponent } from './studente/studente';
import { AccessoNegatoComponent } from './accesso-negato/accesso-negato';
import { Home } from './home/home';

export const routes: Routes = [
  { path: 'home', component: Home },
  { path: 'docente', component: DocenteComponent, canActivate: [roleGuard], data: { role: 'docente' } },
  { path: 'studente', component: StudenteComponent, canActivate: [roleGuard], data: { role: 'studente' } },
  { path: 'accesso-negato', component: AccessoNegatoComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Default redirect to home
  { path: '**', redirectTo: '/home' }, // wildcard route
];
