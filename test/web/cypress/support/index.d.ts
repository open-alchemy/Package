/// <reference types="cypress" />

declare namespace Cypress {
  interface Chainable {
    /**
     * Custom command to login
     * @example cy.login()
     */
    login(): Chainable<string>;

    /**
     * Custom command to create a spec
     * @param accessToken The access token for authentication
     * @param value The body of the spec
     * @param id Unique identifier for the spec
     * @example cy.createSpec('token 1', 'value 1', 'id 1')
     */
    createSpec(accessToken: string, value: string, id: string): Chainable<void>;

    /**
     * Custom command to create a spec
     * @param accessToken The access token for authentication
     * @param id Unique identifier for the spec
     * @example cy.deleteSpec('token 1', 'value 1', 'id 1')
     */
    deleteSpec(accessToken: string, id: string): Chainable<void>;
  }
}
