import axios from 'axios';

import { SpecId, SpecValue, SpecInfo, SpecVersion } from './openapi/models';

import { SpecError } from './errors';

interface IGetParams {
  accessToken: string;
  id: SpecId;
  version?: SpecVersion;
}

/**
 * Get the value of a spec
 *
 * Throws SpecError is something goes wrong whilst loading the spec
 *
 * @param params.accessToken The access token for the package service
 * @param params.id Unique identifier for the spec
 * @param params.version Version for the spec
 */
export async function get(params: IGetParams): Promise<SpecValue> {
  let url = `https://package.api.openalchemy.io/v1/specs/${params.id}`;
  if (params.version) {
    url = `${url}/versions/${params.version}`;
  }

  const response = await axios
    .get<SpecValue>(url, {
      headers: { Authorization: `Bearer ${params.accessToken}` },
    })
    .catch(error => {
      throw new SpecError(
        `error whilst loading the spec: ${error.response.data}`
      );
    });
  return response.data;
}

interface IGetVersionsParams {
  accessToken: string;
  id: SpecId;
}

/**
 * Get the versions of a spec
 *
 * Throws SpecError is something goes wrong whilst loading the versions of the spec
 *
 * @param params.accessToken The access token for the package service
 * @param params.id Unique identifier for the spec
 */
export async function getVersions(
  params: IGetVersionsParams
): Promise<SpecInfo[]> {
  const response = await axios
    .get<SpecInfo[]>(
      `https://package.api.openalchemy.io/v1/specs/${params.id}/versions`,
      {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      }
    )
    .catch(error => {
      throw new SpecError(
        `error whilst loading the versions for the spec: ${error.response.data}`
      );
    });
  return response.data;
}

interface IPutParams {
  accessToken: string;
  id: SpecId;
  value: SpecValue;
}

/**
 * Create or update a spec
 *
 * Throws SpecError is something goes wrong whilst creating or updating the spec
 *
 * @param params.accessToken The access token for the package service
 * @param params.id Unique identifier for the spec
 * @param params.value The value of the spec
 */
export async function put(params: IPutParams): Promise<void> {
  await axios
    .put<void>(
      `https://package.api.openalchemy.io/v1/specs/${params.id}`,
      params.value,
      {
        headers: { Authorization: `Bearer ${params.accessToken}` },
      }
    )
    .catch(error => {
      throw new SpecError(
        `error whilst creating or updating the spec: ${error.response.data}`
      );
    });
  return;
}

interface IDeleteParams {
  accessToken: string;
  id: SpecId;
}

/**
 * Delete a spec
 *
 * Throws SpecError is something goes wrong whilst deleting the spec
 *
 * @param params.accessToken The access token for the package service
 * @param params.id Unique identifier for the spec
 */
export async function delete_(params: IDeleteParams): Promise<void> {
  await axios
    .delete<void>(`https://package.api.openalchemy.io/v1/specs/${params.id}`, {
      headers: { Authorization: `Bearer ${params.accessToken}` },
    })
    .catch(error => {
      throw new SpecError(
        `error whilst deleting the spec: ${error.response.data}`
      );
    });
  return;
}
