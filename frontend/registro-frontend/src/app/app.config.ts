import { ApplicationConfig, provideAppInitializer } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import Keycloak from 'keycloak-js';
import { environment } from '../environments/environment';
import { routes } from './app.routes';
import { AuthInterceptor } from './http.interceptor';

// crea l'istanza di Keycloak
export const keycloak = new Keycloak({
  url: environment.keycloak.url,
  realm: environment.keycloak.realm,
  clientId: environment.keycloak.clientId,
});

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    // registra il services Keycloak
    // così da poterlo iniettare dove ci serve
    { provide: Keycloak, useValue: keycloak },
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    provideAppInitializer(async () => {
      try {
        console.log('🔐 Inizializzazione Keycloak...');
        console.log('Configurazione:', {
          url: environment.keycloak.url,
          realm: environment.keycloak.realm,
          clientId: environment.keycloak.clientId
        });

        const result = await keycloak.init({
          onLoad: 'check-sso',
          checkLoginIframe: false
        });

        console.log('✅ Keycloak inizializzato:', result);
        console.log('Token presente:', !!keycloak.token);
        console.log('Utente autenticato:', keycloak.authenticated);

        if (keycloak.authenticated) {
          console.log('Username:', keycloak.tokenParsed?.['preferred_username']);
          console.log('Ruoli:', keycloak.tokenParsed?.['realm_access']?.roles);
        }

        return result;
      } catch (error) {
        console.error('❌ Errore Keycloak:', error);
        throw error;
      }
    }),
  ],
};
