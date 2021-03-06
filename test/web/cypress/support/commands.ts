/// <reference types="cypress" />

import { SpecService } from '@open-alchemy/package-sdk';

Cypress.Commands.add('login', async () => {
  const accessToken = Cypress.env('ACCESS_TOKEN');

  localStorage.setItem('access_token', accessToken);
  const now = new Date();
  localStorage.setItem('expires_at', (3600000 + now.getTime()).toString());

  return accessToken;
});

Cypress.Commands.add(
  'createSpec',
  async (accessToken: string, value: string, name: string) => {
    const specService = new SpecService();
    await specService.put({
      accessToken,
      value,
      language: 'JSON',
      name,
    });
  }
);

Cypress.Commands.add(
  'deleteSpec',
  async (accessToken: string, name: string) => {
    const specService = new SpecService();
    await specService.delete({
      accessToken,
      name,
    });
  }
);
