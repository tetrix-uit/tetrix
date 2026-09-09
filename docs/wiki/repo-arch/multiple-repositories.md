# Multiple Repositories Architecture

This project has many components. A component is an application, a service, a library, or a
deployment configuration. Each component has its own directory. This root repository holds the
shared knowledge and the governance documents. It also has one shared end-to-end test repository.

## Component types

| Directory | Content |
| --- | --- |
| `apps/` | The frontend applications. |
| `services/` | The server-side services. |
| `libs/` | The shared libraries and the public libraries. |
| `deployment/` | The deployment configuration. |
| `e2e/` | The shared end-to-end tests. |

## Layouts

The project can use one of two layouts. The directory structure is the same in both layouts.

- **Monorepo.** One repository contains all the components. Each component directory is a
  folder in this repository. The `e2e/` directory is also in this repository.
- **Polyrepo.** Each component has its own repository. Each component directory in this root
  repository points to that repository, for example with a submodule or a link. The complete
  `e2e/` directory points to one shared test repository.

## Rules

- Each component must have its own directory.
- Keep the code, the local rules, and the documentation of a component in its directory.
- Keep the knowledge that more than one component needs in `docs/` of this root repository.
- If a component needs code from another component, put that code in a library in `libs/`.
- Keep tests in `e2e/` when they check workflows that use more than one application or service.
- Use one repository for the complete `e2e/` directory.

## Where to put a new component

1. Find the component type in the table above.
2. Make a new directory for the component in the directory of its component type.
3. If the project uses the polyrepo layout, make a new repository for the component. Then point
   the new directory to that repository.
4. Write a `README.md` in the new directory. Give the purpose of the component and how to start it.
