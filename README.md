# astd_python
傲视天地python实现

1.需要一个账号配置，可以直接拷贝傲视天地小助手的account.ini<br/>
account=平台:区服:账号:密码Md5:1:http*//:http*//:角色名<br/>

2.在bin目录下新建一个run.bat，gbk编码<br/>
SET MAINPATH=%cd%<br/>
SET SCRIPTPATH=%MAINPATH%/..<br/>
SET PYTHONPATH=%SCRIPTPATH%;%PYTHONPATH%<br/>
python %MAINPATH%/main.py --user-name=账号名,账号名 --role-name=角色名,角色名<br/>
多个账号角色，用逗号隔开<br/>

3.在git bash命令行下运行run.bat<br/>
