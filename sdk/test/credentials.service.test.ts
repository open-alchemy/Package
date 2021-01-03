import axios from 'axios';
import MockAdaptor from 'axios-mock-adapter';

import { CredentialsService } from '../src/credentials.service';
import { CredentialsError } from '../src/errors';

describe('CredentialsService', () => {
  let mockAdaptor: MockAdaptor;
  let service: CredentialsService;

  beforeEach(() => {
    mockAdaptor = new MockAdaptor(axios);
    service = new CredentialsService();
  });

  describe('get', () => {
    test('should return credentials value when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const responseData = {
        public_key: 'public key 1',
        secret_key: 'secret key 1',
      };
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/credentials/default')
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN get is called
      const returnedPromise = service.get({ accessToken });

      // THEN the credentials is returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should return credentials when 200 is returned using the observable method', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const responseData = {
        public_key: 'public key 1',
        secret_key: 'secret key 1',
      };
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/credentials/default')
        .replyOnce(200, responseData);

      // WHEN get is called
      const returnedPromise = service.get$({ accessToken }).toPromise();

      // THEN the credentials is returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const message = 'message 1';
      mockAdaptor
        .onGet('https://package.api.openalchemy.io/v1/credentials/default')
        .replyOnce(400, btoa(message));

      // WHEN get is called
      const returnedPromise = service.get({ accessToken });

      // THEN the expected error is thrown
      const expectedError = new CredentialsError(
        `error whilst loading the spec: ${message}`
      );
      await expect(returnedPromise).rejects.toEqual(expectedError);
    });
  });

  describe('delete', () => {
    test('should return 204 is returned', async () => {
      // GIVE mocked axios that returns 204
      const accessToken = 'token 1';
      mockAdaptor
        .onDelete('https://package.api.openalchemy.io/v1/credentials/default')
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [204];
        });

      // WHEN delete is called
      const returnedPromise = service.delete({ accessToken });

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should return when 204 is returned', async () => {
      // GIVE mocked axios that returns 204
      const accessToken = 'token 1';
      mockAdaptor
        .onDelete('https://package.api.openalchemy.io/v1/credentials/default')
        .replyOnce(204);

      // WHEN delete is called
      const returnedPromise = service.delete$({ accessToken }).toPromise();

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const message = 'message 1';
      mockAdaptor
        .onDelete('https://package.api.openalchemy.io/v1/credentials/default')
        .replyOnce(400, btoa(message));

      // WHEN delete is called
      const returnedPromise = service.delete({ accessToken });

      // THEN the expected error is thrown
      const expectedError = new CredentialsError(
        `error whilst deleting the spec: ${message}`
      );
      await expect(returnedPromise).rejects.toEqual(expectedError);
    });
  });
});
