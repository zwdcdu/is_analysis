<!-- markdownlint-disable MD033-->
<!-- 禁止MD033类型的警告 https://www.npmjs.com/package/markdownlint -->

# 《信息系统分析与设计》（第4版）

![book](book.jpg)

清华大学出版社 王晓敏 邝孔武 编著 ， 主讲：成都大学信息科学与工程学院 赵卫东副教授

## 实验
- 实验平台地址：http://202.115.82.8/  学生用学号登录，初始密码等于学号

- ### [实验1：业务流程建模](./test1.md)

- ### [实验2：图书管理系统用例建模](./test2.md)

- ### [实验3：图书管理系统领域对象建模](./test3.md)
    
- ### [实验4：图书管理系统顺序图绘制](./test4.md)
 
- ### [实验5：图书管理系统数据库设计与界面设计](./test5.md)

## 实验6：期末考查说明
        
## 搭建文档编写环境：
- 编辑器: IntelliJ IDEA，VS Code等
- IDEA插件: markdown 和 plantuml
- 单独安装: git 和 graphviz

## 参考资料
- [教材下载](./信息系统分析与设计(第4版).pdf)
- 绘制方法参考：[PlantUML标准](http://plantuml.com)
- PlantUML服务: http://plantuml.com/zh/server
- plantuml在线编辑器： http://www.plantuml.com/plantuml
- Markdown格式参考：https://www.jianshu.com/p/b03a8d7b1719
- 老师的教学资源：https://github.com/zwdcdu/is_analysis
- Git简书 https://git-scm.com/book/zh/v2
- Git分支 https://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF
- Github 简明教程-操作标签 https://www.cnblogs.com/tracylxy/p/6439089.html
- Git菜鸟教程 http://www.runoob.com/git/git-tutorial.html
- [GitWindows客户端](./gitgfb_ttrar.rar)
- 版本控制样例参见：https://github.com/oracle/db-sample-schemas
- 文档编写工具 Sphinx 使用手册 https://of.gugud.com/t/topic/185 https://zh-sphinx-doc.readthedocs.io/en/latest/contents.html

## github在线显示plantuml图片
- 使用标准的"\!\[\](地址)"方式显示plantuml图片，地址格式是： http://www.plantuml.com/plantuml/proxy?cache=no&fmt=svg&src=https://zwdcdu.github.io/a.github.io/fig2.puml
    - cache=no表示不缓存，列容易适应文件的变化
    - fmt=svg表示以svg方式显示图形，这个很重要，否则汉字会显示为不同的字体。
    - https://zwdcdu.github.io/a.github.io/fig2.puml表示plantuml源码，可以是任何地址，只要返回plantuml源代码即可。

## git示例
### 克隆test资料库，如果test是私有项目，需要输入密码，clone完成后，会生成一个新的目录test
```
git clone https://github.com/你的github用户名/test.git
```
clone操作应该只做一次，会下载项目资料库中的所有文件、分支和标签，并新建一个.git隐藏目录，使本机和远程仓库建立关联。
clone之后可以使用git pull下载修改文件。

### 配置test目录
```
cd test
ls
git config --global user.name "你的github用户名"
git config --global user.email 你的github邮箱
ls -a
```

### 在本机修改a.c，然后push到网站，需要输入用户名和密码
```
vi a.c
git add *
git commit -m 'zhang 修改'
git push
```

### 在网上修改文件a.c,然后pull到本机
```
git pull
cat a.c
```

![book](./git_team.png)