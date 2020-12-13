import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestScheduler } from 'rxjs/testing';

import { SpecsRefreshButtonComponent } from './specs-refresh-button.component';

describe('SpecsRefreshButtonComponent', () => {
  let component: SpecsRefreshButtonComponent;
  let fixture: ComponentFixture<SpecsRefreshButtonComponent>;
  let testScheduler: TestScheduler;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SpecsRefreshButtonComponent],
    });

    fixture = TestBed.createComponent(SpecsRefreshButtonComponent);
    component = fixture.componentInstance;

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should disable the button by default', () => {
    // GIVEN

    // WHEN changes are detected
    fixture.detectChanges();

    // THEN the button is disabled
    const button: HTMLButtonElement = fixture.nativeElement.querySelector(
      'button'
    );
    expect(button).toBeTruthy();
    expect(button.disabled).toBeTrue();
  });

  [
    {
      description: 'loading false',
      expectation: 'should enable the button',
      loading: false,
      expectedDisabled: false,
    },
    {
      description: 'loading true',
      expectation: 'should disable the button',
      loading: true,
      expectedDisabled: true,
    },
  ].forEach(({ description, expectation, loading, expectedDisabled }) => {
    describe(description, () => {
      it(expectation, () => {
        // GIVEN loading is set
        component.loading = loading;

        // WHEN changes are detected
        fixture.detectChanges();

        // THEN the button is disabled
        const button: HTMLButtonElement = fixture.nativeElement.querySelector(
          'button'
        );
        expect(button).toBeTruthy();
        expect(button.disabled).toEqual(expectedDisabled);
      });
    });
  });

  it('should emit events on the output when the button is clocked', () => {
    // GIVEN loading is false
    component.loading = false;
    fixture.detectChanges();

    testScheduler.run((helpers) => {
      // WHEN the button is clicked
      const button: HTMLButtonElement = fixture.nativeElement.querySelector(
        'button'
      );
      expect(button).toBeTruthy();
      helpers.cold('-b-d').subscribe(() => {
        button.click();
        fixture.detectChanges();
      });

      // THEN the click events are emitted
      helpers
        .expectObservable(component.refreshEvent)
        .toBe('-b-d', { b: undefined, d: undefined });
    });
  });
});
