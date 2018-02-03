# Programming Examples for DH Students

[David J. Thomas](mailto:dave.a.base@gmail.com), [thePortus.com](http://thePortus.com)<br>
Instructor of Ancient History and Digital Humanities, [University of South Florida](https://github.com/usf-portal)

**Only Works on Mac/Linux**

```python
# clone repo
git clone https://github.com/thePortus/dh-programming.git
# move inside repo
cd dh-programming
# install dependencies
pip install -r requirements.txt
# launch notebook
jupyter notebook
```

If you want to make a copy on your account, first make an empty repository on GitHub, then...

```python
# remove the original repo url
git remote remove origin
# add your repo url in, substituting username and repo name
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
# push to remote and set upstream
git push -u origin master
```
