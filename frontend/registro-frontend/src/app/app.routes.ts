import { Routes } from '@angular/router';
import { roleGuard } from './role-guard';
import { DocenteComponent } from './docente/docente';
import { StudenteComponent } from './studente/studente';
import { AccessoNegatoComponent } from './accesso-negato/accesso-negato';


export const routes: Routes = [
  { path: 'docente', component: DocenteComponent, canActivate: [roleGuard], data: { role: 'docente' } },
  { path: 'studente', component: StudenteComponent, canActivate: [roleGuard], data: { role: 'studente' } },
  { path: 'accesso-negato', component: AccessoNegatoComponent },
  { path: '', redirectTo: '/docente', pathMatch: 'full' }, // Default redirect to docente (verrà gestito dal redirect automatico)
  { path: '**', redirectTo: '/docente' }, // wildcard route
];
