# Update PTX remote 
* branch `main` is gitlab, branch `upmain` is github

```
git pull main 
# do sync 
git checkout upmain
git merge main 
git push 
# return on main
git checkout main 
```

# First time set-up :

* on github, rename the default upstream branch to upmain 

* add the prometheus-x as `upstream` remote
```
git remote add upstream git@github.com:Prometheus-X-association/smart-orientation-ontology.git
```

* on local : 
```
git fetch upstream
git switch -c upmain upstream/upmain
```

* for the first time push to remote: (add `--allow-unrelated-histories`): 
```
git checkout upmain
git merge main --allow-unrelated-histories
git push
```
