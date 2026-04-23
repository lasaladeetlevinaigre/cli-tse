# DEVKIT - Guide de Démarrage Rapide

## Installation

```bash
cd devkit
pip install -e .
```

## Premiers Pas

### 1. Vérifier l'installation

```bash
devkit --version
devkit --help
```

### 2. Configurer devkit

Créer un fichier de configuration `~/.devkit/config.json`:

```json
{
  "ai_tool": "claude",
  "default_repo": "owner/repo",
  "theme": "dark",
  "show_spinner": true
}
```

La configuration est chargée automatiquement au démarrage.

## Commandes GitHub

### Lister les issues

```bash
# Lister les 10 premières issues ouvertes
devkit gh issues

# Lister avec un repo spécifique
devkit gh issues --repo owner/repo

# Lister avec un état spécifique
devkit gh issues --state all --limit 20

# Mode interactif avec fzf
devkit gh issues --interactive
```

### Afficher le résumé d'une PR

```bash
devkit gh pr-summary 42
devkit gh pr-summary 42 --repo owner/repo
```

### Créer une branche feature

```bash
devkit gh start-feature my-feature
```

### Créer une PR

```bash
devkit gh open-pr \
  --title "feat: new feature" \
  --body "Description of the feature" \
  --draft
```

### Afficher le statut CI/CD

```bash
devkit gh run-status
devkit gh run-status --repo owner/repo
```

## Commandes IA

### Expliquer une commande shell

```bash
devkit ai explain "git rebase -i HEAD~3"
```

### Obtenir des suggestions

```bash
devkit ai suggest "create a python function to parse CSV files"
```

### Examiner une PR

```bash
devkit ai review 42
devkit ai review 42 --repo owner/repo
```

### Générer un message de commit

```bash
# Sur les changements en staging
git add .
devkit ai commit

# Sur tous les changements
devkit ai commit --no-staged
```

## Workflow Automation

### Démarrer une feature complète

```bash
# Crée une branche, une PR draft et un plan d'implémentation
devkit workflow feature-start my-feature

# Liée à une issue
devkit workflow feature-start my-feature --issue 42

# Avec un repo spécifique
devkit workflow feature-start my-feature --issue 42 --repo owner/repo
```

Cette commande:
1. Crée une branche `feature/my-feature`
2. Pousse la branche sur le serveur
3. Crée une PR en draft
4. (Si --issue) Génère un plan d'implémentation basé sur l'issue

## Structure du Projet

```
devkit/
├── src/devkit/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Typer CLI app entry point
│   ├── config.py             # Configuration management
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── github.py         # GitHub commands (issues, PR, CI)
│   │   ├── ai.py             # AI commands (explain, suggest, review, commit)
│   │   └── workflow.py       # Workflow automation (feature-start)
│   └── utils/
│       ├── __init__.py
│       ├── gh.py             # GitHub CLI wrapper
│       ├── shell.py          # Generic subprocess wrapper
│       └── display.py        # Rich display utilities (tables, panels)
├── tests/
│   ├── __init__.py
│   └── test_utils.py         # Unit tests
├── pyproject.toml            # Project metadata and dependencies
├── README.md                 # Project documentation
└── test_integration.py       # Integration tests
```

## Architecture

### Couches

1. **CLI Layer** (main.py)
   - Typer app avec 3 subcommands: `gh`, `ai`, `workflow`
   - Dispatch vers les modules de commandes

2. **Commands Layer** (commands/)
   - `github.py`: Opérations GitHub via gh CLI
   - `ai.py`: Commandes IA via gh copilot
   - `workflow.py`: Automatisation de workflows

3. **Utils Layer** (utils/)
   - `gh.py`: Wrappers pour GitHub CLI (`gh()`, `gh_json()`, `gh_copilot()`)
   - `shell.py`: Exécution générique de commandes shell
   - `display.py`: Rendu via Rich (tables, panels, spinners)

4. **Config Layer** (config.py)
   - Chargement de `~/.devkit/config.json`
   - Modèle Pydantic typé

### Patterns

- **Type hints**: Toutes les fonctions utilisent des type hints Python 3.12+
- **Error Handling**: Détection de commandes manquantes avec `shutil.which()`
- **Subprocess Abstraction**: Toutes les exécutions passent par les wrappers
- **Rich Output**: Affichage unifié via Rich Console

## Dépendances

- **typer**: Framework CLI
- **rich**: Affichage formaté (tables, panels, spinners, couleurs)
- **pydantic**: Validation de configuration
- **subprocess**: Orchestration d'outils
- **json**: Parsing de JSON depuis gh --json

### Outils externes requis

- `git`: Pour les opérations de branche
- `gh`: GitHub CLI (pour toutes les opérations GitHub)
- `gh copilot`: GitHub Copilot CLI (pour l'IA)
- `fzf`: (Optionnel) Pour le mode interactif

## Développement

### Installation en mode dev

```bash
pip install -e ".[dev]"
```

### Lancer les tests

```bash
# Tests unitaires
pytest

# Avec couverture
pytest --cov=src/devkit

# Tests d'intégration
python test_integration.py
```

### Linting et formatage

```bash
# Vérifier le style
black --check src/
ruff check src/

# Formater automatiquement
black src/
ruff check --fix src/

# Type checking
mypy src/
```

## Exemples d'Utilisation

### Workflow complet de feature

```bash
# 1. Démarrer une feature
devkit workflow feature-start user-auth --issue 123

# 2. Développer...
# $ vim src/auth.py
# $ git add src/auth.py

# 3. Générer un message de commit automatique
devkit ai commit

# 4. Créer une PR (ou mettre à jour la draft)
devkit gh open-pr --title "feat: user auth" --body "Implements JWT authentication"

# 5. Examiner le diff
devkit ai review <PR_NUMBER>
```

### Exploration d'issues

```bash
# Lister les issues
devkit gh issues --limit 20

# Examiner une issue spécifique
devkit gh issues --interactive

# Comprendre une commande complexe
devkit ai explain "git log --oneline --graph --all"
```

## Limitations et Considérations

- Les commandes IA utilisent `gh copilot` (nécessite GitHub Copilot)
- Le mode interactif nécessite `fzf`
- Certaines commandes nécessitent des droits d'accès au repo
- Les diffs volumineux sont tronqués pour les appels IA

## Troubleshooting

### Erreur: "gh not found"

```bash
# Installer GitHub CLI
brew install gh  # macOS
# ou
apt install gh   # Linux
```

### Erreur: "gh copilot not found"

```bash
# Installer GitHub Copilot CLI
gh extension install github/gh-copilot
```

### Erreur: "fzf not found" (pour mode interactif)

```bash
# Installer fzf
brew install fzf   # macOS
# ou
apt install fzf    # Linux
```

## Prochaines Étapes

- [ ] Ajouter support de Gemini CLI
- [ ] Ajouter support de Claude Code CLI
- [ ] Implémenter la sélection interactive avec fzf
- [ ] Ajouter des hooks git pré-commit/push
- [ ] Cacher les secrets dans les diffs envoyés à l'IA
- [ ] Ajouter plus de tests d'intégration
- [ ] Documenter les patterns internes
