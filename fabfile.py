from fabric.api import local

# fab push
def push():
    'Local push to the repository.'
    local('git add .')
    local('git status')
    local('git commit -m "fab autocommit"')
    local('git push origin master')