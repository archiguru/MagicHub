#!/bin/bash
cd ..
echo "开始更新项目"
git checkout --orphan latest_branch
git add -A
git commit -am "remove history & reinitialize"
git branch -D main
git branch -m main
git push -f origin main
git branch --set-upstream-to=origin/main main
exit 0;
