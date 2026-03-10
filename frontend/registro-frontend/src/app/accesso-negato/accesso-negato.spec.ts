import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccessoNegato } from './accesso-negato';

describe('AccessoNegato', () => {
  let component: AccessoNegato;
  let fixture: ComponentFixture<AccessoNegato>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccessoNegato],
    }).compileComponents();

    fixture = TestBed.createComponent(AccessoNegato);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
