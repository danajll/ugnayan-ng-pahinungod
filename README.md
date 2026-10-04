# Ugnayan ng Pahinungod

A web-based project developed using **Vue 3** and **Vite**.

## Tech Stack

* Vue 3
* Vite
* JavaScript

## Getting Started

### Prerequisites

* Node.js
* npm

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/danajll/ugnayan-ng-pahinungod.git
cd ugnayan-ng-pahinungod
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

## Git Branching Strategy

This project follows a branch-based development workflow to keep production-ready code separate from ongoing development and testing.

### Main Branches

| Branch      | Purpose                                                                           |
| ----------- | --------------------------------------------------------------------------------- |
| `main`      | Stable, production-ready version of the project.                                  |
| `staging`   | Integration and testing branch for completed features before merging into `main`. |
| `feature/*` | Individual features or development tasks.                                         |

### Branch Naming Conventions

Use the following prefixes when creating branches:

| Prefix   | Purpose                                              | Example                    |
| -------- | ---------------------------------------------------- | -------------------------- |
| `feat/`  | Developing a new feature                             | `feat/user-authentication` |
| `fix/`   | Fixing bugs or issues                                | `fix/login-validation`     |
| `chore/` | Maintenance, configuration, or documentation updates | `chore/update-readme`      |

Use lowercase letters and hyphens to separate words in branch names.

### Development Workflow

The general workflow is:

```text
feature/*  →  staging  →  main
```

1. **Create a feature branch** from `staging` for a specific task.
2. **Develop and commit changes** within your feature branch.
3. **Open a Pull Request (PR)** targeting `staging` once the changes are ready.
4. **Review, integrate, and test** the changes in `staging`.
5. **Merge `staging` into `main`** when the integrated changes are stable and ready for release.

### Example Commands

Create a new feature branch from `staging`:

```bash
git switch staging
git pull origin staging
git switch -c feat/your-feature-name
```

After making changes:

```bash
git add .
git commit -m "feat: add your feature"
git push -u origin feat/your-feature-name
```

Open a Pull Request on GitHub targeting `staging`.

### Commit Message Conventions

Use descriptive commit messages with the following prefixes:

| Prefix      | Description                                       |
| ----------- | ------------------------------------------------- |
| `feat:`     | New feature                                       |
| `fix:`      | Bug fix                                           |
| `chore:`    | Maintenance or configuration                      |
| `docs:`     | Documentation changes                             |
| `refactor:` | Code restructuring without changing functionality |
| `style:`    | Formatting or styling changes                     |

Examples:

```text
feat: add user registration
fix: resolve login validation error
chore: update project dependencies
docs: update README with branching workflow
```

## Important Notes

* Do not commit `node_modules/` or environment files containing secrets.
* Ensure `.gitignore` is properly configured before committing.
* Avoid committing directly to `main` for ordinary feature development.
* Keep your local branches updated with their respective remote branches before starting new work.
* Use Pull Requests to review changes before merging them into shared branches.
