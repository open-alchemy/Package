import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestScheduler } from 'rxjs/testing';
import { map } from 'rxjs/operators';

import { ClipboardModule, ClipboardService } from 'ngx-clipboard';

import { CredentialsComponent } from './credentials.component';
import { PackageService } from '../../services/package/package.service';
import { Credentials } from '../../services/package/types';

const CREDENTIALS: Credentials = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  public_key: 'public key 1',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  secret_key: 'secret key 1',
};

describe('CredentialsComponent', () => {
  let component: CredentialsComponent;
  let fixture: ComponentFixture<CredentialsComponent>;
  let packageServiceSpy: jasmine.SpyObj<PackageService>;
  let clipboardServiceSpy: jasmine.SpyObj<ClipboardService>;
  let testScheduler: TestScheduler;

  beforeEach(() => {
    packageServiceSpy = jasmine.createSpyObj('PackageService', [
      'credentials$',
    ]);
    clipboardServiceSpy = jasmine.createSpyObj('ClipboardService', [
      'copyText',
      'destroy',
      'pushCopyResponse',
    ]);

    TestBed.configureTestingModule({
      imports: [ClipboardModule],
      declarations: [CredentialsComponent],
      providers: [
        { provide: PackageService, useValue: packageServiceSpy },
        { provide: ClipboardService, useValue: clipboardServiceSpy },
      ],
    });

    fixture = TestBed.createComponent(CredentialsComponent);
    component = fixture.componentInstance;

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  [
    {
      description: 'specId null',
      expectation: 'should not show button nor span',
      specId: null,
      specVersion: 'version 1',
      credentials: CREDENTIALS,
      expectedNotNull: false,
    },
    {
      description: 'specVersion null',
      expectation: 'should not show button nor span',
      specId: 'spec id 1',
      specVersion: null,
      credentials: CREDENTIALS,
      expectedNotNull: false,
    },
    {
      description: 'specVersion null',
      expectation: 'should not show button nor span',
      specId: 'spec id 1',
      specVersion: 'version 1',
      credentials: null,
      expectedNotNull: false,
    },
    {
      description: 'all defined',
      expectation: 'should not show button and span',
      specId: 'spec id 1',
      specVersion: 'version 1',
      credentials: CREDENTIALS,
      expectedNotNull: true,
    },
  ].forEach(
    ({
      description,
      expectation,
      specId,
      specVersion,
      credentials,
      expectedNotNull,
    }) => {
      describe(description, () => {
        it(expectation, () => {
          testScheduler.run((helpers) => {
            // GIVEN credentials$ that returns credentials, specId and version
            packageServiceSpy.credentials$ = helpers.cold('a', {
              a: { value: credentials, loading: false, success: null },
            });
            component.specId = specId;
            component.specVersion = specVersion;

            // WHEN changes are detected
            fixture.detectChanges();

            // THEN button and span are null or not as expected
            const componentSpecInfos$ = helpers.cold('a').pipe(
              map(() => {
                fixture.detectChanges();
                const button: HTMLButtonElement = fixture.nativeElement.querySelector(
                  'button'
                );
                const p: HTMLParagraphElement = fixture.nativeElement.querySelector(
                  'p'
                );
                if (p !== null) {
                  expect(p.innerText).toContain('pip install');
                  if (specId !== null) {
                    expect(p.innerText).toContain(specId);
                  }
                  if (specVersion !== null) {
                    expect(p.innerText).toContain(specVersion);
                  }
                  if (credentials !== null) {
                    expect(p.innerText).toContain(credentials.public_key);
                    expect(p.innerText).toContain(credentials.secret_key);
                  }
                }
                return { button: button !== null, p: p !== null };
              })
            );
            helpers.expectObservable(componentSpecInfos$).toBe('a', {
              a: { button: expectedNotNull, p: expectedNotNull },
            });
          });
        });
      });
    }
  );

  describe('copy button', () => {
    it('should copy to clipboard on copy click', () => {
      const specId = 'spec id 1';
      const specVersion = 'version 1';

      testScheduler.run((helpers) => {
        // GIVEN credentials$ that returns credentials, specId and version
        packageServiceSpy.credentials$ = helpers.cold('a', {
          a: { value: CREDENTIALS, loading: false, success: null },
        });
        component.specId = specId;
        component.specVersion = specVersion;

        // WHEN changes are detected and the button is clicked
        fixture.detectChanges();
        const componentSpecInfos$ = helpers.cold('a').pipe(
          map(() => {
            fixture.detectChanges();
            const button: HTMLButtonElement = fixture.nativeElement.querySelector(
              'button'
            );
            button.click();
            return true;
          })
        );
        helpers.expectObservable(componentSpecInfos$).toBe('a', {
          a: true,
        });
      });

      // THEN copyText has been called
      expect(clipboardServiceSpy.pushCopyResponse).toHaveBeenCalledTimes(1);
    });
  });
});
