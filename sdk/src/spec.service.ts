import axios from 'axios';
import { from, Observable } from 'rxjs';

import { SpecName, SpecValue, SpecInfo, SpecVersion, Spec } from './types';

import { SpecError } from './errors';
import { decodeResponse } from './helpers';

interface ICalculateUrlParams {
  name: SpecName;
  version?: SpecVersion;
}

function calculateUrl(params: ICalculateUrlParams): string {
  let url = `https://package.api.openalchemy.io/v1/specs/${params.name}`;
  if (params.version) {
    url = `${url}/versions/${params.version}`;
  }
  return url;
}

interface IGetParams {
  accessToken: string;
  name: SpecName;
  version?: SpecVersion;
}

interface IGetVersionsParams {
  accessToken: string;
  name: SpecName;
}

interface IPutParams {
  accessToken: string;
  name: SpecName;
  value: SpecValue;
  language: 'JSON' | 'YAML';
  version?: SpecVersion;
}

interface IDeleteParams {
  accessToken: string;
  name: SpecName;
}

export class SpecService {
  /**
   * Get the value of a spec
   *
   * Throws SpecError is something goes wrong whilst loading the spec
   *
   * @param params.accessToken The access token for the package service
   * @param params.name Display name of the spec
   * @param params.version (optional) Version for the spec
   */
  async get(params: IGetParams): Promise<Spec> {
    const url = calculateUrl(params);

    const response = await axios
      .get<Spec>(url, {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      })
      .catch((error) => {
        const message = decodeResponse(error.response.data);
        throw new SpecError(`error whilst loading the spec: ${message}`);
      });
    return response.data;
  }

  get$(params: IGetParams): Observable<Spec> {
    return from(this.get(params));
  }

  /**
   * Get the versions of a spec
   *
   * Throws SpecError is something goes wrong whilst loading the versions of the spec
   *
   * @param params.accessToken The access token for the package service
   * @param params.name Display name of the spec
   */
  async getVersions(params: IGetVersionsParams): Promise<SpecInfo[]> {
    const response = await axios
      .get<SpecInfo[]>(
        `https://package.api.openalchemy.io/v1/specs/${params.name}/versions`,
        {
          headers: { Authorization: `Bearer ${params.accessToken}` },
        }
      )
      .catch((error) => {
        const message = decodeResponse(error.response.data);
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
   * @param params.name Display name of the spec
   * @param params.value The value of the spec
   * @param params.language The language the spec is in
   * @param params.version (optional) Version for the spec
   */
  async put(params: IPutParams): Promise<void> {
    const url = calculateUrl(params);

    await axios
      .put<void>(url, params.value, {
        headers: {
          Authorization: `Bearer ${params.accessToken}`,
          'Content-Type': 'text/plain',
          'X-LANGUAGE': params.language,
        },
      })
      .catch((error) => {
        const message = decodeResponse(error.response.data);
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
   * @param params.name Display name of the spec
   */
  async delete(params: IDeleteParams): Promise<void> {
    await axios
      .delete<void>(calculateUrl(params), {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      })
      .catch((error) => {
        const message = decodeResponse(error.response.data);
        throw new SpecError(`error whilst deleting the spec: ${message}`);
      });
    return;
  }

  delete$(params: IDeleteParams): Observable<void> {
    return from(this.delete(params));
  }
}
