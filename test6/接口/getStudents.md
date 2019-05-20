<!-- markdownlint-disable MD033-->
<!-- 禁止MD033类型的警告 https://www.npmjs.com/package/markdownlint -->

# 接口：getStudents  [返回](../README.md)
用例： [学生列表](../用例/学生列表.md)

- 权限：
    学生/访客：不能看到RESULT_SUM，WEB_SUM
    老师：可以看到RESULT_SUM，WEB_SUM。

- 功能：
    返回所有学生的列表。

- API请求地址：
   接口基本地址/v1/api/getStudents

- 请求方式 ：
    GET

- 请求参数说明:
    无

- 返回实例：

        {
            "status": true,
            "info": null,
            "total": 121,
            "data": [
                {"WEB_SUM": "Y,Y,Y,Y,Y,N",
                "RESULT_SUM": "83.75,90,80,80,85,N",
                "GITHUB_USERNAME": "Chinajuedui",
                "STUDENT_ID": "201510315203",
                "CLASS": "软件(本)15-1",
                "NAME": "陈松华",
                "UPDATE_DATE": "2018-04-02 13:48:01"},
                {
                ...其他学生
                }
            ]
        }

- 返回参数说明：

  |参数名称|说明|
  |:---------:|:--------------------------------------------------------|
  |status|bool类型，true表示正确的返回，false表示有错误|
  |info|返回结果说明信息|
  |total|返回学生人数|
  |data|所有学生的数组|
  |WEB_SUM|网址是否正确的汇总|
  |RESULT_SUM|成绩的汇总|
  |GITHUB_USERNAME|GITHUB 用户名|
  |STUDENT_ID|学号|
  |CLASS|班级|
  |NAME|真实姓名|
  |UPDATE_DATE|GitHUB用户名修改日期|