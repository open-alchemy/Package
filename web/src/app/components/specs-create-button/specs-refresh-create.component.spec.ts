import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MatIconModule } from '@angular/material/icon';

import { TestScheduler } from 'rxjs/testing';

import { SpecsCreateButtonComponent } from './specs-create-button.component';

describe('SpecsCreateButtonComponent', () => {
  let component: SpecsCreateButtonComponent;
  let fixture: ComponentFixture<SpecsCreateButtonComponent>;
  let testScheduler: TestScheduler;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SpecsCreateButtonComponent],
      imports: [MatIconModule],
    });

    fixture = TestBed.createComponent(SpecsCreateButtonComponent);
    component = fixture.componentInstance;

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
