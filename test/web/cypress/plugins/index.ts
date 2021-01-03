/// <reference types="cypress" />

import clipboardy from 'clipboardy';

/**
 * @type {Cypress.PluginConfig}
 */
module.exports = (on: any, config: any) => {
  on('task', {
    getClipboard() {
      return clipboardy.readSync();
    },
  });
};
