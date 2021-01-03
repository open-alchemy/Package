/// <reference path="../support/index.d.ts" />

const VERSION = 'version 1';
const TITLE = 'title 1';
const DESCRIPTION = 'description 1';
const ID = 'spec1';
const SPEC_VALUE = {
  info: {
    title: TITLE,
    description: DESCRIPTION,
    version: VERSION,
  },
  components: {
    schemas: {
      Schema: {
        type: 'object',
        'x-tablename': 'schema',
        properties: { id: { type: 'integer' } },
      },
    },
  },
};
const SPEC_VALUE_STRING = JSON.stringify(SPEC_VALUE);

describe('specs', () => {
  let accessToken: string;

  beforeEach(() => {
    accessToken = Cypress.env('ACCESS_TOKEN');

    cy.deleteSpec(accessToken, ID);
  });

  it('should load the page, load the created spec on refresh click, delete the spec on delete click', () => {
    // Load empty page
    cy.login();
    cy.visit('/specs');
    // should not have any rows
    cy.get('table')
      .find('tr')
      .should('have.length', 1);

    // Add spec to the database
    cy.createSpec(accessToken, SPEC_VALUE_STRING, ID);

    // Click refresh
    cy.get('[data-cy=refresh]').should('exist');
    cy.get('[data-cy=refresh]').click();
    cy.get(`[data-cy=create]`).should('exist');
    // Check that content exists
    cy.get('table')
      .find('tr')
      .should('have.length', 2);
    cy.get(`[data-cy=id-${ID}]`).should('contain', ID);
    cy.get(`[data-cy=title-${ID}]`).should('contain', TITLE);
    cy.get(`[data-cy=description-${ID}]`).should('contain', DESCRIPTION);
    cy.get(`[data-cy=version-${ID}]`).should('contain', VERSION);
    cy.get(`[data-cy=updated-at-${ID}]`).should('exist');
    cy.get(`[data-cy=pip-install-${ID}]`).should('exist');
    cy.get(`[data-cy=pip-install-command-${ID}]`)
      .should('contain', ID)
      .and('contain', VERSION)
      .and('contain', 'pip install')
      .and('contain', '/pk_')
      .and('contain', ':sk_');
    cy.get(`[data-cy=copy-pip-install-command-${ID}]`).should(
      'contain',
      'Copy'
    );
    cy.get(`[data-cy=model-count-${ID}]`).should('contain', '1');
    cy.get(`[data-cy=management-${ID}]`).should('exist');
    cy.get(`[data-cy=edit-${ID}]`).should('exist');
    // Click delete
    cy.get(`[data-cy=delete-${ID}]`).should('exist');
    cy.get(`[data-cy=delete-${ID}]`).click();
    // Check that content no longer exists
    cy.get('table')
      .find('tr')
      .should('have.length', 1);
  });
});
