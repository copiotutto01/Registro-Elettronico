import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Studente } from './studente';

describe('Studente', () => {
  let component: Studente;
  let fixture: ComponentFixture<Studente>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Studente],
    }).compileComponents();

    fixture = TestBed.createComponent(Studente);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
