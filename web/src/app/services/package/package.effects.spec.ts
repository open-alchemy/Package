import { Observable } from 'rxjs';
import { TestScheduler } from 'rxjs/testing';

import { Action } from '@ngrx/store';
import { OAuthService } from 'angular-oauth2-oidc';
import { specs } from '@open-alchemy/package-sdk';

import { PackageEffects } from './package.effects';

const testScheduler = new TestScheduler((actual, expected) => {
  expect(actual).toEqual(expected);
});

describe('PackageEffects', () => {
  let actions$ = new Observable<Action>();
  let effects: PackageEffects;
  let oAuthServiceSpy: jasmine.SpyObj<OAuthService>;
  let specsSpy = jasmine.SpyObj<specs>;

  const accessToken = 'token 1';

  beforeEach(() => {
    oAuthServiceSpy = jasmine.createSpyObj('OAuthService', ['getAccessToken']);
    oAuthServiceSpy.getAccessToken.and.returnValue(accessToken);
    effects = new PackageEffects(actions$, oAuthServiceSpy);
  });

  describe('listSpecs$', () => {
    [
      {
        description: 'empty actions',
        expectation: 'should return empty actions',
        actionsMarbles: '',
        actionsValues: {},
        expectedMarbles: '',
        expectedValues: {},
      },
    ].forEach(
      ({
        description,
        expectation,
        actionsMarbles,
        actionsValues,
        expectedMarbles,
        expectedValues,
      }) => {
        describe(description, () => {
          it(expectation, () => {
            testScheduler.run((helpers) => {
              // GIVEN actions
              actions$ = helpers.cold(actionsMarbles, actionsValues);

              // WHEN listSpecs$ is called
              const returnedActions = effects.listSpecs$;

              // THEN the expected actions are returned
              helpers
                .expectObservable(returnedActions)
                .toBe(expectedMarbles, expectedValues);
            });
          });
        });
      }
    );
  });
});
