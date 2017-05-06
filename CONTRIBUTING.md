# Before you begin

1. Verify that an issues has been assigned to you
2. Change the state of the _issue_ to `In progress`.
3. _Fork_ the repo
4. Follow the installation guide in the `INSTALL.md` file of this repository.

# Contribute to the project
1. Create a new branch
2. Work on it
3. Test your code!.
  - Only documentation and refactoring modifications does not need to have new tests.
4. Make sure tests are sucessful
5. If your work need specific tasks for deployment, make sure to notify it in [update.md](update.md) at the root of this project.
6. Push and create a _pull request_

# Good practices
* Code and comments are in english
* Follow [Git _workflow_ ](http://nvie.com/posts/a-successful-git-branching-model/).
    * Functionnality and big bugs are made via Pull Requests.
    * One bug/functionnality per pull requests.
    * Those pull requests are merged into the `develop` branch
    * Name the branch based on the modification : `hotfix-XXX`, `feature-XXX`, etc.
    * The branch `master` contains the production code. Do not try to _commit_ on this branch !

* Your test must fail before your modification and pass with it
* Make thorough _commit_ comment
* No test, no _pull request_

# Good practices : Pull Request/commit
## Pull-Requests
* PR template :

    ```markdown
    | Q                             | R
    | ----------------------------- | -------------------------------------------
    | Bug fix ?                     | [yes|no]
    | New functionnality ?          | [yes|no]
    | Tickets (_issues_) reference  | [List of ticket seprated by ;]
    ```
* Add QA comments. Those comments help to comprehend what have been modified, what must be tested and the more risky part of the code. Make sure to comment if a setup is needed beforehand.

## Commits
* For commits, we follow the Git philosophy :
    * The first line must not be more than 50 caracters
    * If needed, complete your commit by adding comments (maximum of 70 characters per following lines)
    * One fix , and one good fix only, per commit (atomic)

* Make sure your pull request does not have any useless commits E.G (`fix previous commit`, ...). If you have any, squash it.

Dont hesitate to ask for help, good luck!
