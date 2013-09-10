pykindle
========

Share and Publish kindle highlights and notes

Note: tested using Python 2.7.3. Will not work with python 3+

```
git clone git@github.com:dnene/pykindle.git
cd pykindle
# set appropriate virtualenv
python setup.py develop
python pykindle.py <amazon_user_id> <amazon_password>
```
Will generate a file called kindle_highlights.html
(No styles yet, only raw html)

