<!-- markdownlint-disable MD033-->
<!-- 禁止MD033类型的警告 https://www.npmjs.com/package/markdownlint -->

# 接口：getNextPrevStudent  [返回](../README.md)
用例： [评定成绩](../用例/评定成绩.md)

- 功能：
    返回一个学生的上一个或者下一个学生的学号。
    
- 权限：    
    老师：只有老师可以调用该API。
    
- API请求地址： 
    接口基本地址/v1/api/getNextPrevStudent/<is_next>/<student_id>

- 请求方式 ：
    GET

- 请求参数说明:        

  |参数名称|说明|
  |:---------:|:--------------------------------------------------------|
  |is_next|是下一个还是上一个，如果为1表示取下一个学生，如果为0表示上一个学生|
  |student_id|学生的学号|
    
- 返回实例：

        {         
            "status": true,
            "info": null,    
            "student_id": "201510315203"
        }
 
- 返回参数说明：    
 
  |参数名称|说明|
  |:---------:|:--------------------------------------------------------|      
  |status|bool类型，true表示正确的返回，false表示有错误|
  |info|返回结果说明信息|
  |student_id|学号|

