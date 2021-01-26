# grpc-demo
grpc-demo-project and notes

# gRPC

## 介绍

gRPC （Google Remote Procedure Call，Google远程过程调用）：

​	支持多种编程语言，对网络设备进行配置和纳管的方法。开源，客户端和服务器之间的通信更加专注于业务层面的内容，减少了对由g RPC框架实现的底层通信的关注。

![img](https://tva1.sinaimg.cn/large/008eGmZEly1gmxy9sxpdrj30hs07fdgc.jpg)

**gRPC 交互过程：**

1. 交换机在开启gRPC 功能后充当gRPC 客户端的角色，采集服务器充当gRPC 服务器角色；
2. 交换机会根据订阅的事件构建对应数据的格式（GPB/JSON），通过Protocol Buffers进行编写proto文件，交换机与服务器建立gRPC 通道，通过gRPC 协议向服务器发送请求消息；
3. 服务器收到请求消息后，服务器会通过Protocol Buffers解译proto文件，还原出最先定义好格式的数据结构，进行业务处理；
4. 数据梳理完后，服务器需要使用Protocol Buffers重编译应答数据，通过gRPC协议向交换机发送应答消息；
5. 交换机收到应答消息后，结束本次的gRPC交互

**PS：**Protocol Buffers是一种更加灵活、高效的数据格式，与XML、JSON类似，在一些高性能且对响应速度有要求的数据传输场景非常适用。

**特点：**

- 更快的传输速度——序列化的成果
- 跨平台多语言
- 基于HTTP2.0标准设计



## demo实战

**Proto buf：**

proto文件

Protoc ： 编译时

Protobuf runtime：运行时

protobuf使用：

`编写 proto 文件 -> 使用 protoc 编译 -> 添加 protobuf 运行时 -> 项目中集成`

protobuf更新：

`修改 proto 文件 -> 使用 protoc 重新编译 -> 项目中修改集成的地方`



**1.工具包安装：**

`pip install grpcio`

`pip install grpcio-tools`

**2.编写proto文件**

```
// [python quickstart](https://grpc.io/docs/quickstart/python.html#run-a-grpc-application)
// python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto

// helloworld.proto
syntax = "proto3";

service Greeter {
    rpc SayHello(HelloRequest) returns (HelloReply) {}
    rpc SayHelloAgain(HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
    string name = 1;
}

message HelloReply {
    string message = 1;
}
```

**3.编译proto文件——生成.**

..pb2.py和protobuf数据进行交互

和...pb2_grpc.py和grpc进行交互

```bash
# 编译 proto 文件
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto

python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
--python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
--grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
-I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录
```

**4.编写server和client**

## protobuf3 语言指南

**定义一个消息类型**

```protobuf
syntax="proto3"

message SearchRequest {
	string query=1;
	int32 page_number = 2;
	int32 result_per_page = 3;
}
```

指定字段数据类型

**保留标识符(reserved)**

**默认值**

**枚举**：enum

**.proto文件生成了什么？**

​	**对C++来说，**编译器会为每个.proto文件生成一个.h文件和一个.cc文件，.proto文件中的每一个消息有一个对应的类。

​	**对Java来说，**编译器为每一个消息类型生成了一个.java文件，以及一个特殊的Builder类（该类是用来创建消息类接口的）。

​	**对Python来说，**有点不太一样——Python编译器为.proto文件中的每个消息类型生成一个含有静态描述符的模块，该模块与一个元类（metaclass）在运行时（runtime）被用来创建所需的Python数据访问类。

……



**定义服务service**

```protobuf
service SearchService {
  rpc Search (SearchRequest) returns (SearchResponse);
}
```


## gRPC basic: 4种通信方式

hello world 使用了最简单的grpc通信方式：request+respones

grpc支持4种通信方式：

- 客户端一次请求，服务器一次应答
- 客户端一次请求，服务器多次应答（流式）
- 客户端多次请求（流式），服务器一次应答
- 客户端多次请求（流式），服务器多次应答（流式）

Demo:**routeguide**应用到了4种通信方式，具体业务如下：

- 数据：json数据——包括地点经纬度（location）和地名name组成
- 通信方式1:客户端请求一个地点——是否在数据源中
- 通信方式2:客户端指定一个矩形（给定矩阵的对角点坐标），服务器返回这个矩阵范围内的地点信息
- 通信方式3:客户端给服务器发送多个地点信息，服务器返回汇总信息（RouteSummary）
- 通信方式4:客户端和服务器使用地点信息聊天（chat）

## 跨语言服务java&python





# 参考网址：

grpc| python 实战 grpc：

https://www.jianshu.com/p/43fdfeb105ff?isappinstalled=0

官方文档：


## 跨语言服务java&python


