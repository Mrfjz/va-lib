### Setup
Install pyenv
```bash
brew install pyenv pyenv-virtualenv
```

Add the below lines to ~/.bash_profile to enable auto-activation of virtualenvs
```text
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Setup virtual env and install dependencies
```bash
make setup
```

After installation, the virtual env should be activated in terminal, i.e.
```bash
(python-template) xxx@xxx python-template % 
```
### Test
```bash
make test
```