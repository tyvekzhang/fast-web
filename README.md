<div  align="center" style="margin-top: 3%">
   <h1>
     Fast Web
   </h1>
   <p>
     <img src="https://raw.githubusercontent.com/tyvekzhang/fast-web/main/docs/source/_static/img/fast_web.svg" alt="logo" style="vertical-align:middle; margin: 0.5%"/>
   </p>
   <p>
     <img alt="GitHub License" src="https://img.shields.io/github/license/tyvekzhang/fast-web">
     <img alt="CI" src="https://github.com/tyvekzhang/fast-web/actions/workflows/ci.yaml/badge.svg">
     <img alt="Read the Docs" src="https://img.shields.io/readthedocs/fast-web">
   </p>
   <h4>
      <p>
        <b>简体中文</b> |
        <a href="https://github.com/tyvekzhang/fast-web/blob/main/docs/README_en.md">English</a>
     </p>
   </h4>
   <h3>
    PyWeb领域最好用的脚手架之一。
   </h3>
</div>


## 特性

- ⚡ 开箱即用, 完全实现中间件零依赖
   - 默认使用Sqlite, 也可自由切换PostgreSQL、MySQL
   - 默认使用文件缓存, 支持切换为Redis
- 🚢 开启Python操作数据库表结构的新体验
- 🚀 内置单表常见操作, 简化ORM操作
- 🎨 丰富插件机制
   - Jwt安全认证
   - 访问限流
   - Ip黑名单
- 🐋 完备容器化解决方案
  - Docker
  - Docker-compose
  - Kubernetes
- ✅ 基于GitHub Actions的CI (持续集成) 和 CD (持续交付)

## 文档
- 在线文档: [Read the docs](https://fast-web.readthedocs.io/en/latest/)
- 交互式API文档示意
  <img alt="API doc"  src="https://raw.githubusercontent.com/tyvekzhang/fast-web/main/docs/img/api_doc.png">

## 设置一个虚拟环境
> 这部分是可选的，但可能对新学 Python 的用户有用。[虚拟环境设置](https://github.com/tyvekzhang/fast-web/blob/main/docs/VIRTUAL_ENV.md)

## 快速开始
1. 克隆代码
```shell
git clone https://github.com/tyvekzhang/fast-web.git
cd fast-web
```
2. 下载依赖
通过[uv](https://docs.astral.sh/uv)创建环境并下载依赖
```shell
uv sync
```
3. 数据库迁移
```shell
alembic upgrade head
```
4. 启动
```shell
python apiserver.py
```
5. 交互式文档地址: http://127.0.0.1:13000/docs
6. 恭喜你, 运行成功. 接口访问前需创建用户, 并进行认证
7. 可以随时按CTRL+C停止运行

## 许可证

FastWeb采用 [MIT 许可证](https://opensource.org/licenses/MIT)开源。
