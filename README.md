# OpenAlchemyPackage

OpenAlchemy package management as a service

## Web

Front end for the service. Defined here: [./web](./web).

## API

Serves requests for the front end. Defined here: [./api](./api).

## SDK

Wraps the API to make it easier to consume in the front end. Defined here:
[./sdk](./sdk).

## Database

Personalizes API responses vy exposing an interface to the database as well as
fixtures for testing. Defined here: [./database](./database).

## Security

Facade for security operations, such as generating public and private keys.
Exposes fixtures for testing. Defined here: [./security](./security).

## Build

When a new spec is uploaded, builds a package from th spec and uploads it to
the storage. Defined here: [./build](./build).

## Index

Implements the packaging index to enable pip installing the model packages.
Defined here: [./index](./index).

## Infrastructure

Shared CloudFormation stacks for application components. Defined here:
[./infrastructure](./infrastructure).

## Test

Execute tests against production for application components. Defined here:
[./test](./test).
