# discovery.md

## GitHub CLI (`gh`)

- **Ce qu'il fait** : Permet de gérer les repos, issues et PRs directement depuis le terminal.
- **Découverte** : `gh repo list` affiche mes repos, `gh issue list` montre les issues ouvertes.
- **Cas d'usage** : Créer une PR ou lister les issues sans quitter le terminal.

---

## GitHub Copilot CLI (`gh copilot`)

- **Ce qu'il fait** : Génère et explique des commandes shell en langage naturel.
- **Découverte** : `gh copilot suggest 'trouver les fichiers Python modifiés cette semaine'` propose une commande `find` précise.
- **Cas d'usage** : Trouver des commandes complexes sans les mémoriser.

---

## bat

- **Ce qu'il fait** : Affiche les fichiers avec coloration syntaxique (meilleur que `cat`).
- **Découverte** : `bat --theme=GitHub README.md` rend le fichier plus lisible.
- **Cas d'usage** : Lire du code ou des fichiers de config dans le terminal.

---

## delta

- **Ce qu'il fait** : Affiche les diffs Git en mode side-by-side et coloré.
- **Découverte** : `git diff HEAD-1   delta` montre les changements de manière claire.
- **Cas d'usage** : Revoir les modifications avant un commit.

---

## fzf

- **Ce qu'il fait** : Fuzzy finder pour filtrer et sélectionner des éléments dans une liste.
- **Découverte** : `ls | fzf` permet de naviguer et sélectionner un fichier rapidement.
- **Cas d'usage** : Trouver un commit ou un fichier dans l'historique Git.

---

## Claude Code (`claude`)

- **Ce qu'il fait** : Assistant IA pour analyser du code, répondre à des questions ou générer des fichiers.
- **Découverte** : `claude 'Explique le but de ce dépôt'` donne un résumé clair.
- **Cas d'usage** : Générer des docstrings ou diagnostiquer des erreurs dans le code.