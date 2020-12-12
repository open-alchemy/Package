import axios from 'axios';
import MockAdaptor from 'axios-mock-adapter';

import { list } from '../src/specs';
import { SpecsError } from '../src/errors';

describe('specs', () => {
  let mockAdaptor: MockAdaptor;

  beforeEach(() => {
    mockAdaptor = new MockAdaptor(axios);
  });

  describe('list', () => {
    test('should return specs when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const responseData = [{ key: 'value' }];
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/specs')
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN list is called
      const returnedSpecsPromise = list({ accessToken });

      // THEN the specs are returned
      expect(returnedSpecsPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const message = 'message 1';
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/specs')
        .replyOnce(400, message);

      // WHEN list is called
      const returnedSpecsPromise = list({ accessToken });

      // THEN the specs are returned
      const expectedError = new SpecsError(
        `error whilst loading the specs: ${message}`
      );
      expect(returnedSpecsPromise).rejects.toEqual(expectedError);
    });
  });
});
