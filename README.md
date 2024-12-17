# ico_converter
icon file converter


## Library
```
pip install -r requirements.txt
``` 

## 배포할때 불필요한 library 제거
```
pip freeze > mypiplist.txt
pip uninstall -r mypiplist.txt -y
```

## exe build
https://pypi.org/project/tkinterdnd2-universal/
```
 pyinstaller --onefile --noconsole --icon='icon_cnver.ico' --add-data='icon_cnver.ico:icon_cnver.ico' --name='ICON_CNVER' main.py --additional-hooks-dir=.
 ```