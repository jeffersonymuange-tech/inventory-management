# Git steps

First commit on main:

```bash
git init -b main
git add .gitignore requirements.txt pytest.ini README.md
git commit -m "Initial project setup"
git remote add origin https://github.com/YOUR-USERNAME/inventory-management.git
git push -u origin main
```

Then do this for each branch in the table:

```bash
git checkout -b BRANCH-NAME
git add FILES
git commit -m "message"
git push -u origin BRANCH-NAME
# on GitHub: open a pull request, merge it, click "Delete branch"
git checkout main
git pull
git branch -d BRANCH-NAME
```

| Branch | Files |
|--------|-------|
| feature/crud-routes | app.py, database.py, validation.py, crud_routes.py |
| feature/openfoodfacts | off_api.py, external_routes.py (and add the blueprint to app.py) |
| feature/cli | cli.py, cli_api.py, cli_view.py, cli_change.py, cli_input.py |
| test/api-tests | tests/conftest.py, tests/helpers.py, tests/test_read_and_add.py, tests/test_update_and_delete.py |
| test/openfoodfacts-tests | tests/test_off_barcode.py, tests/test_off_search.py, tests/test_search_routes.py, tests/test_import_route.py |
| test/cli-tests | tests/test_cli_view.py, tests/test_cli_change.py, tests/test_cli_menu.py |

Note: app.py imports both route files, so on the first branch use a version
of app.py without the `external` lines, then add them on the second branch.
