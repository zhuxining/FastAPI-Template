## 关于项目

这是一个使用 FastAPI 最佳实践构建的纯后端项目，参考官方实践。

### 构建工具

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Granian](https://github.com/emmett-framework/granian)
- [Loguru](https://loguru.readthedocs.io/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)

## 入门指南


### 安装

1. 克隆仓库
    ```sh
    git clone https://github.com/your_username/ylsh-backend.git
    ```
2. 进入项目目录
    ```sh
    cd ylsh-backend
    ```
3. 安装依赖
    ```sh
    uv sync
    ```

## 使用方法

启动项目：
```sh
granian --interface rsgi app.main:app --reload --log --access-log
```

## 路线图

- [ ] code
	- [ ] 增删改查 - CRUD
	- [x] 数据库模型 - base_model 
		- [x] 表默认字段 
		- [x] 数据库注释 
		- [ ] 数据关系 
	- [ ] 日志
	- [ ] 工厂函数
		- [ ] api 文档是否显示
		- [ ] 数据初始化
	- [ ] 返回数据格式
		- [ ] 异常定义
	- [ ] 完善 FastAPI User 的增删改差及时间记录
- [ ] deploy
	- [ ] docker 部署
	- [ ] work 配置
	- [ ] 开发/生产环境依赖隔离安装
- [ ] alembic
	- [ ] 数据迁移
- [ ] docs
    - [ ] 使用的一些注意事项


## 许可证

该项目使用 MIT 许可证。详情请参阅 [LICENSE](LICENSE)。

## 感谢
