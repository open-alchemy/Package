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
        .replyOnce(200, [{ key: 'value' }]);

      // WHEN list is called
      const returnedSpecsPromise = list({ accessToken });

      // THEN the specs are returned
      expect(returnedSpecsPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/specs')
        .replyOnce(400, 'some error');

      // WHEN list is called
      const returnedSpecsPromise = list({ accessToken });

      // THEN the specs are returned
      const expectedError = new SpecsError(
        'something went wrong whilst loading the specs'
      );
      expect(returnedSpecsPromise).rejects.toEqual(expectedError);
    });
  });
});
