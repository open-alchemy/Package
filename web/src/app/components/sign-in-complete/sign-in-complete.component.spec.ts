import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { TestScheduler } from 'rxjs/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';

import { OAuthEvent, OAuthService } from 'angular-oauth2-oidc';

import { SignInCompleteComponent } from './sign-in-complete.component';
import { environment } from '../../../environments/environment';

const testScheduler = new TestScheduler((actual, expected) => {
  expect(actual).toEqual(expected);
});

describe('SignInCompleteComponent', () => {
  let component: SignInCompleteComponent;
  let fixture: ComponentFixture<SignInCompleteComponent>;
  let routerSpy: jasmine.SpyObj<Router>;
  let oAuthServiceSpy: jasmine.SpyObj<OAuthService>;

  beforeEach(() => {
    routerSpy = jasmine.createSpyObj('Router', ['navigate']);
    oAuthServiceSpy = jasmine.createSpyObj('OAuthService', ['events']);

    TestBed.configureTestingModule({
      declarations: [SignInCompleteComponent],
      providers: [
        { provide: OAuthService, useValue: oAuthServiceSpy },
        { provide: Router, useValue: routerSpy },
      ],
      schemas: [NO_ERRORS_SCHEMA],
    });

    fixture = TestBed.createComponent(SignInCompleteComponent);
    component = fixture.componentInstance;
  });

  afterEach(() => {
    sessionStorage.clear();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should navigate back to the stored path when token_received is triggered', () => {
      const url = 'url 1';
      sessionStorage.setItem(environment.signInCompleteReturnPathKey, url);

      testScheduler.run((helpers) => {
        // GIVEN events
        const events = helpers.cold<OAuthEvent>('a', {
          a: {
            type: 'token_received',
          },
        });
        oAuthServiceSpy.events = events;

        // WHEN ngOnInit is called
        component.ngOnInit();
      });

      // THEN navigate was called
      expect(routerSpy.navigate).toHaveBeenCalledOnceWith([url]);
      // AND the session storage is cleared
      expect(
        sessionStorage.getItem(environment.signInCompleteReturnPathKey)
      ).toBeNull();
    });

    ([
      {
        description: 'no events',
        expectation: 'it should not call navigate',
        marbles: '',
        values: {},
        expectedCalls: [],
      },
      {
        description: 'single different event',
        expectation: 'it should not call navigate',
        marbles: 'a',
        values: { a: { type: 'different' } },
        expectedCalls: [],
      },
      {
        description: 'single token_received event',
        expectation: 'it should call navigate once',
        marbles: 'a',
        values: { a: { type: 'token_received' } },
        expectedCalls: [['']],
      },
      {
        description: 'multiple token_received events',
        expectation: 'it should call navigate once',
        marbles: 'ab',
        values: {
          a: { type: 'token_received' },
          b: { type: 'token_received' },
        },
        expectedCalls: [['']],
      },
    ] as {
      description: string;
      expectation: string;
      marbles: string;
      values: { [key: string]: OAuthEvent };
      expectedCalls: string[][];
    }[]).forEach(
      ({ description, expectation, marbles, values, expectedCalls }) => {
        describe(description, () => {
          it(expectation, () => {
            testScheduler.run((helpers) => {
              // GIVEN events
              const events = helpers.cold<OAuthEvent>(marbles, values);
              oAuthServiceSpy.events = events;

              // WHEN ngOnInit is called
              component.ngOnInit();
            });

            // THEN navigate was called the expected number of times
            expect(routerSpy.navigate).toHaveBeenCalledTimes(
              expectedCalls.length
            );
            expectedCalls.forEach((expectedCall) =>
              expect(routerSpy.navigate).toHaveBeenCalledWith(expectedCall)
            );
          });
        });
      }
    );
  });
});
