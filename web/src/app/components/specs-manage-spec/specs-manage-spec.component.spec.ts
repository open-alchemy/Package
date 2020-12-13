import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MatIconModule } from '@angular/material/icon';

import { TestScheduler } from 'rxjs/testing';

import { SpecsManageSpecComponent } from './specs-manage-spec.component';
import { PackageService } from '../../services/package/package.service';

describe('SpecsManageSpecComponent', () => {
  let component: SpecsManageSpecComponent;
  let fixture: ComponentFixture<SpecsManageSpecComponent>;
  let testScheduler: TestScheduler;
  let packageServiceSpy: jasmine.SpyObj<PackageService>;

  beforeEach(() => {
    packageServiceSpy = jasmine.createSpyObj('PackageService', [
      'specsComponentDeleteSpec',
    ]);
    TestBed.configureTestingModule({
      declarations: [SpecsManageSpecComponent],
      imports: [MatIconModule],
      providers: [{ provide: PackageService, useValue: packageServiceSpy }],
    });

    fixture = TestBed.createComponent(SpecsManageSpecComponent);
    component = fixture.componentInstance;

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should not show the delete and edit buttons if specId is not defined', () => {
    // GIVEN

    // WHEN changes are detected
    fixture.detectChanges();

    // THEN the delete button is not shown
    const button: HTMLButtonElement = fixture.nativeElement.querySelector(
      'button'
    );
    expect(button).toBeFalsy();
    // AND the edit button is not shown
    const a: HTMLButtonElement = fixture.nativeElement.querySelector('a');
    expect(a).toBeFalsy();
  });

  describe('delete button', () => {
    it('should enable the delete button by default', () => {
      // GIVEN defined specId
      component.specId = 'spec id 1';

      // WHEN changes are detected
      fixture.detectChanges();

      // THEN the button is disabled
      const button: HTMLButtonElement = fixture.nativeElement.querySelector(
        'button'
      );
      expect(button).toBeTruthy();
      expect(button.disabled).toBeFalse();
    });

    [
      {
        description: 'deleteDisabled false',
        expectation: 'should enable the button',
        deleteDisabled: false,
        expectedDisabled: false,
      },
      {
        description: 'deleteDisabled true',
        expectation: 'should disable the button',
        deleteDisabled: true,
        expectedDisabled: true,
      },
    ].forEach(
      ({ description, expectation, deleteDisabled, expectedDisabled }) => {
        describe(description, () => {
          it(expectation, () => {
            // GIVEN deleteDisabled is set
            component.specId = 'spec id 1';
            component.deleteDisabled = deleteDisabled;

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
      }
    );

    it('should call specsComponentDeleteSpec on click and disable the delete button', () => {
      // GIVEN specId is set
      const specId = 'spec id 1';
      component.specId = specId;
      fixture.detectChanges();
      expect(packageServiceSpy.specsComponentDeleteSpec).toHaveBeenCalledTimes(
        0
      );

      // WHEN delete is clicked
      const button: HTMLButtonElement = fixture.nativeElement.querySelector(
        'button'
      );
      button.click();
      fixture.detectChanges();

      // THEN specsComponentDeleteSpec was called with the specId
      expect(
        packageServiceSpy.specsComponentDeleteSpec
      ).toHaveBeenCalledOnceWith(specId);
      // AND the button is disabled
      expect(button.disabled).toBeTrue();
    });
  });

  describe('deleteButtonClick', () => {
    it('should not call specsComponentDeleteSpec and disable the button if specId is not defined', () => {
      // GIVEN specId is null
      expect(component.specId).toBeNull();

      // WHEN deleteButtonClick is called
      component.deleteButtonClick();

      // THEN specsComponentDeleteSpec was not called
      expect(packageServiceSpy.specsComponentDeleteSpec).not.toHaveBeenCalled();
      // AND the button is not disabled
      expect(component.deleteDisabled).toBeFalse();
    });
  });

  describe('edit button', () => {
    it('should have the correct href', () => {
      // GIVEN specId is set
      const specId = 'spec id 1';
      component.specId = specId;

      // WHEN changes are detected
      fixture.detectChanges();

      // THEN the edit button has the correct link
      const a: HTMLButtonElement = fixture.nativeElement.querySelector('a');
      expect(a).toBeTruthy();
      expect(a.getAttribute('href')).toContain(specId);
    });
  });
});
