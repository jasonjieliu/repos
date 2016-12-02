# repos
all source

python:

py2exe生成exe：

1、下载安装py2exe：http://nchc.dl.sourceforge.net/project/py2exe/py2exe/0.6.9/py2exe-0.6.9.win64-py2.7.amd64.exe

2、在python源码目录创建文件setup.py（login.py是程序main入口，dll_excludes是打包时忽略是库文件）
	# !/usr/bin/python
	# coding:utf-8

	from distutils.core import setup
	import py2exe

	setup(
		windows = ['login.py'],
		options = {
			"py2exe":
				{"dll_excludes": ["MSVCP90.dll"],
				 "compressed"  : 1,
				 "optimize"    : 2,
				 "ascii"       : 0
				 }
		}
	)

2、cmd在python源码目录下执行python setup.py py2exe

3、在python源码目录下会生成一个dist文件夹，将该文件夹打包发布即可

pyinstaller生成exe：

1、下载安装setuptools：https://pypi.python.org/packages/1a/31/3c29a0d6eaf8851d2031003f300b4accb724e3f5c4d519e8e7d88bc373a3/setuptools-29.0.1.zip#md5=ab145ab25ebb85ffed5dc1db9d03a099
	解压setuptools-29.0.1.zip
	cd setuptools-29.0.1
	python setup.py install
	
2、下载安装pypiwin32：https://pypi.python.org/packages/79/da/1c6a0e2c258fa80a2754dc449fbe121800de8d9801e48e1e7dbeaed54c96/pypiwin32-219.win-amd64-py2.7.exe#md5=96152aa546fe016e8229749e8ed92920
	或者直接安装pyinstaller，pyinstaller在安装过程中会自动下载pypiwin32
	
3、下载安装pyinstaller：https://github-cloud.s3.amazonaws.com/releases/2835111/bfba749c-1171-11e6-8d18-a180a4df6377.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAISTNZFOVBIJMK3TQ%2F20161201%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20161201T083404Z&X-Amz-Expires=300&X-Amz-Signature=fb89524072d82c2df6c351a1d3cdab8af50e845cb1954b92a02f24b8df96b33f&X-Amz-SignedHeaders=host&actor_id=16793561&response-content-disposition=attachment%3B%20filename%3DPyInstaller-3.2.zip&response-content-type=application%2Foctet-stream
	解压PyInstaller-3.2.zip
	cd PyInstaller-3.2
	python setup.py install
	
3、cmd在python源码目录下执行pyinstaller.py login.py（login.py是程序main入口）
	pyinstaller.py参数说明：pyinstaller.py -Fw login.py
	-F, --onefile Py代码只有一个文件
	-D, --onedir Py代码放在一个目录中（默认选项）
	-K, --tk 包含TCL/TK
	-a, --ascii 不包含编码，在支持unicode的python上默认包含所有编码
	-d, --debug 生成debug模式的exe文件
	-w, --windowed, --noconsole 启动时无控制台(Windows Only)
	-c, --nowindowed, --console 启动时有控制台(Windows Only)
	-X, --upx 使用upx压缩exe文件
	-o DIR, --out=DIR 设置spec文件输出的目录，默认在PyInstaller同目录
	-i, --icon=<FILE.ICO> 加入图标（Windows Only）
	-v FILE, --version=FILE 加入版本信息文件
	
4、下载安装upx：https://github-cloud.s3.amazonaws.com/releases/67031040/494c5ea2-765b-11e6-8146-2a475a3f349e.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAISTNZFOVBIJMK3TQ%2F20161202%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20161202T105620Z&X-Amz-Expires=300&X-Amz-Signature=10e5bb2366fa26ad33871a85f4f713701da4a438e08d12de4f9451726eb9a6e1&X-Amz-SignedHeaders=host&actor_id=16793561&response-content-disposition=attachment%3B%20filename%3Dupx391w.zip&response-content-type=application%2Foctet-stream
	解压upx391w.zip
	将upx.exe拷贝到python安装目录即可（和python.exe同级目录）（Pyinstaller.py中也不需要加-x选项）