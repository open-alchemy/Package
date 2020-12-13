import axios from 'axios';
import MockAdaptor from 'axios-mock-adapter';

import { SpecsService } from '../src/specs.service';
import { SpecsError } from '../src/errors';

describe('SpecsService', () => {
  let mockAdaptor: MockAdaptor;
  let service: SpecsService;

  beforeEach(() => {
    mockAdaptor = new MockAdaptor(axios);
    service = new SpecsService();
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
      const returnedSpecsPromise = service.list({ accessToken });

      // THEN the specs are returned
      await expect(returnedSpecsPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const message = 'message 1';
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/specs')
        .replyOnce(400, btoa(message));

      // WHEN list is called
      const returnedSpecsPromise = service.list({ accessToken });

      // THEN the specs are returned
      const expectedError = new SpecsError(
        `error whilst loading the specs: ${message}`
      );
      await expect(returnedSpecsPromise).rejects.toEqual(expectedError);
    });
  });
});
