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
        <b>English</b> |
        <a href="https://github.com/tyvekzhang/fast-web/blob/main/README.md">简体中文</a>
     </p>
   </h4>
   <h3>
    Fast web aims to be one of the best scaffold in PyWeb.
   </h3>
</div>

## Features
- ⚡ Out-of-the-box, completely middleware-free
   - Uses SQLite by default, but can freely switch to PostgreSQL or MySQL
   - Uses file caching by default, supports switching to Redis
- 🚢 Embark on a new experience for Python database table structure operations
- 🚀 Built-in common single-table operations, simplifying ORM operations
- 🎨 Rich plugin mechanism
   - JWT security authentication
   - Access rate limiting
   - IP blacklist
- 🐋 Comprehensive containerization solution
  - Docker
  - Docker-compose
  - Kubernetes
- ✅ CI (Continuous Integration) and CD (Continuous Delivery) based on GitHub Actions

## Documentation
- Online documentation: [Read the docs](https://fast-web.readthedocs.io/en/latest/)
- Interactive API documentation demonstration
  <img alt="API doc"  src="https://raw.githubusercontent.com/tyvekzhang/fast-web/main/docs/img/api_doc.png">


## Setting up a Conda Virtual Environment
> This part is optional, but may be useful for new Python learners. [Virtual Environment Setup](https://github.com/tyvekzhang/fast-web/blob/main/docs/VIRTUAL_ENV_en.md)

## Quick Start
1. Clone the code
```shell
git clone https://github.com/tyvekzhang/fast-web.git
cd fast-web
```
2. Download dependencies with [uv](https://docs.astral.sh/uv)
```shell
uv sync
```
3. Database migration
```shell
alembic upgrade head
```
4. Start the server
```shell
python apiserver.py
```
5. Interactive documentation address: http://127.0.0.1:9010/docs
6. Congratulations, you've successfully started the server! You need to create a user and authenticate before
   accessing the API.
7. You can stop the server at any time by pressing CTRL+C.

## License

FastWebis open-sourced under the [MIT License](https://opensource.org/licenses/MIT).
