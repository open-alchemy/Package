import axios from 'axios';
import { from, Observable } from 'rxjs';

import { SpecInfo } from './openapi/models';

import { SpecsError } from './errors';
import { decodeResponse } from './helpers';

interface IListParams {
  accessToken: string;
}

export class SpecsService {
  /**
   * List all available specs
   *
   * Throws SpecsError if anything goes wrong whilst listing the specs
   *
   * @param params.accessToken The access token for the package service
   */
  async list(params: IListParams): Promise<SpecInfo[]> {
    const response = await axios
      .get<SpecInfo[]>('https://package.api.openalchemy.io/v1/specs', {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      })
      .catch(error => {
        let message = decodeResponse(error.response.data);
        throw new SpecsError(`error whilst loading the specs: ${message}`);
      });
    return response.data;
  }

  list$(params: IListParams): Observable<SpecInfo[]> {
    return from(this.list(params));
  }
}
