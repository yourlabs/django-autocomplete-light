#!/bin/bash -eu
# Release a new version of django-autocomplete-light
#
# Usage: ./release.sh 1.2.3-rc0

if [ -z "${1-}" ]; then
    grep '^# ' $0
    exit 1
fi

if git tag -l | grep "^${1}\$"; then
    echo Tag $1 already exists
    exit 1
fi

stashed=0
if [[ $(git diff --stat) != '' ]]; then
    git stash
    stashed=1
fi

npm install
npm run build
if [[ $(git diff --stat) != '' ]]; then
    git add src/dal/static/autocomplete_light/i18n/
    git commit -am "Rebuild static"
fi

sed -i "s/version=[^,]*,/version='$1',/" setup.py
sed -i "s/release = [^,]*,/release = '$1'/" docs/conf.py
short=$(echo $1 | grep -Eo '[^.]+\.[^.]+')
sed -i "s/version = [^,]*,/version = '$short'/" docs/conf.py

git add setup.py docs/conf.py
git commit -m "Release $1"
git tag $1
python setup.py sdist
twine upload dist/django-autocomplete-light-${1/-/}.tar.gz
git push origin master $1

if [[ $stashed -eq 1 ]]; then
    git stash apply
fi
