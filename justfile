# show this list
default:
    just --list

# commit
commit:
    git add .
    cz commit

# push
push:
    git push

# commit then push
commit-push: commit push

# bump version
bump:
    cz bump
    git push
    git push --tags

# update deps
update:
    nix flake update
    poetry update

# format
format:
    # TODO: treefmt?
    isort .
    black .
    alejandra .
