#!/bin/bash
if [ "$(uname)" == "Darwin" ]; then
    repo=`pwd`
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    repo="/opt/src/MagicHub/"
fi

cd $repo || exit

git pull
git add -A
git commit -m "update by script"
git push -u origin main
echo "更新完成！"
