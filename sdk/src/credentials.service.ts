import axios from 'axios';
import { from, Observable } from 'rxjs';

import { Credentials } from './openapi/models';

import { CredentialsError } from './errors';
import { decodeResponse } from './helpers';

const URL = 'https://package.api.openalchemy.io/v1/credentials/default';

interface IGetParams {
  accessToken: string;
}

interface IDeleteParams {
  accessToken: string;
}

export class CredentialsService {
  /**
   * Get the value of credentials
   *
   * Throws CredentialsError is something goes wrong whilst loading the spec
   *
   * @param params.accessToken The access token for the package service
   */
  async get(params: IGetParams): Promise<Credentials> {
    const response = await axios
      .get<Credentials>(URL, {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      })
      .catch(error => {
        const message = decodeResponse(error.response.data);
        throw new CredentialsError(`error whilst loading the spec: ${message}`);
      });
    return response.data;
  }

  get$(params: IGetParams): Observable<Credentials> {
    return from(this.get(params));
  }

  /**
   * Delete a spec
   *
   * Throws CredentialsError is something goes wrong whilst deleting the spec
   *
   * @param params.accessToken The access token for the package service
   */
  async delete(params: IDeleteParams): Promise<void> {
    await axios
      .delete<void>(URL, {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      })
      .catch(error => {
        const message = decodeResponse(error.response.data);
        throw new CredentialsError(
          `error whilst deleting the spec: ${message}`
        );
      });
    return;
  }

  delete$(params: IDeleteParams): Observable<void> {
    return from(this.delete(params));
  }
}
