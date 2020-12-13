import axios from 'axios';
import { from, Observable } from 'rxjs';

import { SpecId, SpecValue, SpecInfo, SpecVersion } from './openapi/models';

import { SpecError } from './errors';
import { decodeResponse } from './helpers';

interface ICalculateUrlParams {
  id: SpecId;
  version?: SpecVersion;
}

function calculateUrl(params: ICalculateUrlParams): string {
  let url = `https://package.api.openalchemy.io/v1/specs/${params.id}`;
  if (params.version) {
    url = `${url}/versions/${params.version}`;
  }
  return url;
}

interface IGetParams {
  accessToken: string;
  id: SpecId;
  version?: SpecVersion;
}

interface IGetVersionsParams {
  accessToken: string;
  id: SpecId;
}

interface IPutParams {
  accessToken: string;
  id: SpecId;
  value: SpecValue;
  language: 'JSON' | 'YAML';
  version?: SpecVersion;
}

interface IDeleteParams {
  accessToken: string;
  id: SpecId;
}

export class SpecService {
  /**
   * Get the value of a spec
   *
   * Throws SpecError is something goes wrong whilst loading the spec
   *
   * @param params.accessToken The access token for the package service
   * @param params.id Unique identifier for the spec
   * @param params.version (optional) Version for the spec
   */
  async get(params: IGetParams): Promise<SpecValue> {
    let url = calculateUrl(params);

    const response = await axios
      .get<SpecValue>(url, {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      })
      .catch(error => {
        let message = decodeResponse(error.response.data);
        throw new SpecError(`error whilst loading the spec: ${message}`);
      });
    return response.data;
  }

  get$(params: IGetParams): Observable<SpecValue> {
    return from(this.get(params));
  }

  /**
   * Get the versions of a spec
   *
   * Throws SpecError is something goes wrong whilst loading the versions of the spec
   *
   * @param params.accessToken The access token for the package service
   * @param params.id Unique identifier for the spec
   */
  async getVersions(params: IGetVersionsParams): Promise<SpecInfo[]> {
    const response = await axios
      .get<SpecInfo[]>(
        `https://package.api.openalchemy.io/v1/specs/${params.id}/versions`,
        {
          headers: { Authorization: `Bearer ${params.accessToken}` },
        }
      )
      .catch(error => {
        let message = decodeResponse(error.response.data);
        throw new SpecError(
          `error whilst loading the versions for the spec: ${message}`
        );
      });
    return response.data;
  }

  getVersions$(params: IGetVersionsParams): Observable<SpecInfo[]> {
    return from(this.getVersions(params));
  }

  /**
   * Create or update a spec
   *
   * Throws SpecError is something goes wrong whilst creating or updating the spec
   *
   * @param params.accessToken The access token for the package service
   * @param params.id Unique identifier for the spec
   * @param params.value The value of the spec
   * @param params.language The language the spec is in
   * @param params.version (optional) Version for the spec
   */
  async put(params: IPutParams): Promise<void> {
    let url = calculateUrl(params);

    await axios
      .put<void>(url, params.value, {
        headers: {
          Authorization: `Bearer ${params.accessToken}`,
          'Content-Type': 'text/plain',
          'X-LANGUAGE': params.language,
        },
      })
      .catch(error => {
        let message = decodeResponse(error.response.data);
        throw new SpecError(
          `error whilst creating or updating the spec: ${message}`
        );
      });
    return;
  }

  put$(params: IPutParams): Observable<void> {
    return from(this.put(params));
  }

  /**
   * Delete a spec
   *
   * Throws SpecError is something goes wrong whilst deleting the spec
   *
   * @param params.accessToken The access token for the package service
   * @param params.id Unique identifier for the spec
   */
  async delete(params: IDeleteParams): Promise<void> {
    await axios
      .delete<void>(
        `https://package.api.openalchemy.io/v1/specs/${params.id}`,
        {
          headers: { Authorization: `Bearer ${params.accessToken}` },
        }
      )
      .catch(error => {
        let message = decodeResponse(error.response.data);
        throw new SpecError(`error whilst deleting the spec: ${message}`);
      });
    return;
  }

  delete$(params: IDeleteParams): Observable<void> {
    return from(this.delete(params));
  }
}
