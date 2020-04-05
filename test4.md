<!-- markdownlint-disable MD033-->
<!-- 禁止MD033类型的警告 https://www.npmjs.com/package/markdownlint -->

## 实验4 图书管理系统顺序图绘制 | [返回](./README.md)

- 本实验的目的是掌握顺序图的作用，对象交互模式，消息在对象交互中的作用，以及顺序图与活动图（通常叫流程图）的区别。
- 仔细阅读并理解第10章系统总体设计的10.4.3节：设计类的方法。
- 根据[实验2：图书管理系统用例建模](./test2.md)以及[实验3：图书管理系统领域对象建模](./test3.md)，绘制出<b>图书管理系统</b>主要用例的顺序图。
- 用PlantUML标准工具画出图书管理系统的顺序图（如教材Page215的图10.41，图10.42，Page218的图10.46和图10.47）。
- 整个文档要汇总到README.md文本文件中进行说明，说明文件用Markdown格式编写。

<b>注意事项</b>

- 每个时序图就是一个用例（来自你的<b>实验2</b>）的时序，时序图中的对象就是类的对象（来自你的<b>实验3</b>）。
- 时序图中的消息可以是类（来自你的<b>实验3</b>）的操作方法（如教材Page219的图10.49）。
- 活动图（流程图）通常是一个具体功能或者算法的实现流程，需要非常精确地说明各种情况（含异常情况）的处理方式。
而时序图主要为了体现对象之间的消息流转，对象的生命同期。时序图通常只需要站在对象和参考者的角度描述主要的，正常的业务流程，
因此不需要绘制太多的分支及异常处理过程，这样可以保持时序图的简洁，直观。

<b>实验提交</b>

- 实验提交到自己的gitHub的is_analysis/test4目录中，主要文件名是：README.md，再附上一些图片文件。
- 你的gitHub中的is_analysis/test4目录中可能有以下文件：

``` filelist
README.md
sequence1.png
sequence2.png
...
```

- 你的实验内容提交成功后，可以直接访问https://github.com/<b>zhang</b>/is_analysis/tree/master/test4
查看你编写的实验文档。其中zhang是你的gitHub用户名。

- 请在2020-04-14之前提交，过时扣分。

<b>参考</b>

- 顺序图（也叫时序图）的绘制方法参考[PlantUML标准](http://plantuml.com/sequence-diagram)文件的sequence-diagram标准
- Markdown格式参考：https://www.jianshu.com/p/b03a8d7b1719
- 老师的教学资源：https://github.com/zwdcdu/is_analysis
- 老师以同学身份做的<b>伪实验4</b>参考：https://github.com/zwdcdu/is_analysis/tree/master/test4