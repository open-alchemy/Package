import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MatIconModule } from '@angular/material/icon';

import { SpecsCreateButtonComponent } from './specs-create-button.component';

describe('SpecsCreateButtonComponent', () => {
  let component: SpecsCreateButtonComponent;
  let fixture: ComponentFixture<SpecsCreateButtonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SpecsCreateButtonComponent],
      imports: [MatIconModule],
    });

    fixture = TestBed.createComponent(SpecsCreateButtonComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
