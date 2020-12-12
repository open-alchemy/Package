import axios from 'axios';

import { SpecInfo } from './openapi/models';

import { SpecsError } from './errors';

interface IListParams {
  accessToken: string;
}

export async function list(params: IListParams): Promise<SpecInfo[]> {
  const response = await axios
    .get<SpecInfo[]>('https://package.api.openalchemy.io/v1/specs', {
      headers: { Authorization: `Bearer ${params.accessToken}` },
    })
    .catch(() => {
      throw new SpecsError('something went wrong whilst loading the specs');
    });
  return response.data;
}
