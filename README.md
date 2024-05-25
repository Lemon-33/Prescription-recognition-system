# **表单智能识别服务系统详细设计v5**

## **1. 系统介绍**

该软件系统名称为“表单智能识别服务系统”，用于表单信息的智能识别。该系统可以实现用户的注册登录、表单类型的选取、表单图片上传、表单内容识别、任意区域框选与识别、模板存储与更新、识别结果的查看修改和保存等功能。

本系统采用C/S两端模式，由客户端和服务端构成。客户端通过操作界面与用户进行交互，并且通过发送HTTP请求以及接收HTTP响应来与服务端进行交互。而服务端则根据接收到的客户端请求，进行相应的图像处理以及文字识别等操作，并将处理结果返回给客户端。

客户端和服务端的开发语言都是Python3，客户端和服务端之间以HTTP协议实现信息的交互

## **2. 客户端**

客户端目前采用Python3进行开发，负责与用户进行交互。客户端包含两个部分，用户界面部分以及与服务端交互的部分。根据用户需求不同，用户操作界面可分为海关报关单识别和药库入库单识别两种。用户界面的开发主要通过调用pyQt5库完成，包括一个注册界面、一个登录界面、一个模板选择页面和一个实际操作界面，用于满足用户操作的需要。而与服务端交互的部分则负责将用户的请求发送给服务端，并且接收服务端所返回的结果，然后交由用户界面进行显示。

### **2.1 注册/登录和模板选择界面**

登录界面如图2所示。登录时，用户输入用户名、密码，按“登录”键后该信息会发送给服务端。根据服务端的返回信息用户端有不同的响应：若服务端返回“No\_user”或“Password mistake”，则停留在登录界面，并在状态栏显示服务端返回的信息；若服务端返回“successful+token”则保存接收到的token值并跳转到模板选择界面。

注册时，用户输入用户名和两遍密码后，按“确认”按钮，客户端会对比“密码”栏和“确认密码”栏输入的信息是否相同，若不相同，则在状态栏显示“密码错误”，若相同，则将用户名和密码发送给服务端。若服务端返回“Failed\_name”，则停留在该界面，并在状态栏显示“该用户名已存在”；若服务端返回“successful”，则跳转回登录界面。

模板选择界面若按“药库入库单”按钮，则跳转至药库入库单用户操作界面；若按“海关报关单”按钮，则跳转至海关报关单用户操作界面。

图4 模板选择界面

### **2.2 用户操作界面**

1. 上传请求

   用户按“打开”按钮后，将打开一张表单图片，客户端会对图片进行归一化处理后得到一张归一化后的二值化图片。客户端将图片内容与用户名、表单类型、图片格式一起发送给服务端。若服务端返回识别结果，则将识别界面显示在界面上；若返回“Module\_failed+PictureID”，则将返回结果显示在状态栏，提示用户框选表单。

1. 保存请求

   用户框选完毕后，按“保存”按钮，客户端会将用户名、第一个左上角点的绝对坐标、表格长、表格宽、图片id、图片格式、每次框选的信息（包括：序号、关键字、左上相对坐标、右下相对坐标）发送给服务端。客户端接收来自服务端的识别结果，并将其显示在界面上。

1. 清空请求

   若用户发现识别结果错误率很高，则按“清空”按钮，则用户操作界面的所有识别结果全部清空，用户重新对表单进行框选。

1. 确认请求

   当用户对识别结果确认无误后，按“确认”按钮，客户端将用户名、图片id、和确认后的OCR识别结果发送给服务端。

   ## **3. 客户端服务端交互**

   客户端发送request请求，通过HTTP协议POST方式，以不同的url形式，将不同的请求内容发送给服务端，服务端接收相应的POST请求并解析请求体，完成不同请求对应的操作。

   表1前后端API

| &emsp;请求模块名称 | &emsp;方式 |     &emsp;url      |                        &emsp;传递参数                        |                        &emsp;返回结果                        | &emsp;参数说明 |
| :----------------: | :--------: | :----------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :------------: |
|   &emsp;注册请求   | &emsp;POST |  &emsp;/register   |             <p>&emsp;uname,</p><p>&emsp;pwd</p>              | <p>&emsp;成功: successful</p><p>&emsp;重名：Failed\_name</p><p>&emsp;注册失败（数据库错误）：ACCOUNT\_REGISTER\_FAILED</p> |     &emsp;     |
|   &emsp;登录请求   | &emsp;POST |    &emsp;/login    |             <p>&emsp;uname,</p><p>&emsp;pwd</p>              | <p>&emsp;成功:successful+token</p><p>&emsp;没有此用户:No\_user</p><p>&emsp;密码错误：Password mistake</p><p>&emsp;数据库错误：mysql mistake</p> |     &emsp;     |
|   &emsp;上传请求   | &emsp;POST | &emsp;/uploadfiles | <p>&emsp;uname,</p><p>&emsp;token,</p><p>&emsp;file\_send,</p><p>&emsp;img\_format</p> | <p>&emsp;登录失效:Logon\_failure</p><p>&emsp;识别成功：successful</p> |     &emsp;     |

   ## **4. 服务端处理**

   （1）注册响应：

   从前端得到用户名和密码，在数据库中搜索有没有同名用户，如果有，返回前端“Failed\_name”，如果没有，则返回“successful”，将密码加密存入数据库。注意：数据库连接失败返回“ACCOUNT\_REGISTER\_FAILED”

   （2）登录响应：

   从前端得到用户名和密码，在数据库中搜索有没有该用户，如果没有，返回前端“No\_user”，如果有，对比密码是否相同，若密码不同，返回前端：“Password mistake”，若密码相同，则生成token存入数据库，返回“successful”+token。注意：数据库连接失败返回“mysql mistake”

   （3）上传响应：

   从前端得到用户名、token值、表单类型、图片内容和图片格式。

   图片保存模块：将图片内容转化成图片保存到服务器本地的文件夹里，并生成图片id、输出模板id。将用户名、图片id、图片路径、图片格式、时间戳和输入模板id保存至数据库。

   模板识别模块：用token值判断用户登录是否失效，如果失效直接返回“Logon\_failure”，无需进行后续操作。从文件夹中提取图片，进行模板识别，将提取的特征和数据库中已有模板进行匹配，返回匹配结果，如果匹配失败，返回“Module\_failed+PictureID”，如果有模板，将输入模板id保存至数据库，并将绝对坐标传递至图片裁剪模块。

   图片裁剪模块：根据绝对坐标对图片进行裁剪，保存到服务器文件夹中，返回图片所在路径至OCR模块。

   OCR模块：根据图片路径，进行图像识别，将识别结果返回至前端。

   （4）保存响应：

   从前端得到用户名、图片id、图片格式、框选长宽比、每次框选的信息（包括：序号、关键字、左上坐标、右下坐标）。

   模板保存模块：生成输入模板id，并将时间戳、框选信息、模板特征保存至数据库。将坐标信息发送至图片裁剪模块。

   图片裁剪模块：根据绝对坐标对图片进行裁剪，保存到服务器文件夹中，返回图片所在路径至OCR模块。

   OCR模块：根据图片路径，进行图像识别，将识别结果返回至前端。

   （5）确认响应

   从前端得到用户名、图片id和确认后的OCR识别结 果，将识别结果存储至数据库中。成功保存返回“Save\_success”，数据库连接失败返回“mysql mistake”

   ## **5. 数据库存储**

   ## **附录**

   moduleJson包括以下内容：用户名、第一个左上绝对坐标、长总像素、宽总像素、图片id、图片格式、框选总次数、每次框选的信息（包括：序号、关键字、左上相对坐标、右下相对坐标）

   例如：

   {"uname":xxx, "c1":"23,123", "length":2371, "width":2423,"PictureID":”xxx34”, "img\_format":".jpg","coordinateAmount":2, "order":1,"key":"序号","Coordinate1":"0,0","Coordinate2":"0.03923357664, 0.159509" ,"order":2,"key":"药品名称","Coordinate1":"0.03923357664,0","Coordinate2":"0.1824817518, 0.159509"}
