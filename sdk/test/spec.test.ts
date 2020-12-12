import axios from 'axios';
import MockAdaptor from 'axios-mock-adapter';

import { get, put } from '../src/spec';
import { SpecError } from '../src/errors';

describe('spec', () => {
  let mockAdaptor: MockAdaptor;

  beforeEach(() => {
    mockAdaptor = new MockAdaptor(axios);
  });

  describe('get', () => {
    test('should return specs when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const responseData = 'spec 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN get is called
      const returnedSpecPromise = get({ accessToken, specId });

      // THEN the specs are returned
      expect(returnedSpecPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const message = 'message 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(400, message);

      // WHEN get is called
      const returnedSpecPromise = get({ accessToken, specId });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst loading the spec: ${message}`
      );
      expect(returnedSpecPromise).rejects.toEqual(expectedError);
    });
  });

  describe('put', () => {
    test('should return specs when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const specValue = 'spec value 1';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [204];
        });

      // WHEN put is called
      const returnedSpecPromise = put({ accessToken, specId, specValue });

      // THEN the specs are returned
      expect(returnedSpecPromise).resolves.toEqual(undefined);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const specValue = 'spec value 1';
      const message = 'message 1';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(400, message);

      // WHEN put is called
      const returnedSpecPromise = put({ accessToken, specId, specValue });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst creating or updating the spec: ${message}`
      );
      expect(returnedSpecPromise).rejects.toEqual(expectedError);
    });
  });
});
