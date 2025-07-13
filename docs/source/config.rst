Default Config
===============

Server Configuration
--------------------

.. code-block:: yaml

  server:
    name: Fast web
    host: 0.0.0.0
    port: 13000
    version: 2.0.0
    app_desc: Fast web aims to one of the best scaffolding in the PyWeb field.
    api_prefix: /v1
    workers: 1
    log_file_path: /var/log/fast_web/fast_web.log
    win_tz: china standard time
    linux_tz: asia/shanghai
    enable_rate_limit: False
    global_default_limits: 10/second

Database Configuration
-----------------------

.. code-block:: yaml

  database:
    # sqlite+aiosqlite:///your/absolute/path/xxx.db
    # postgresql+asyncpg://user:pass@localhost:port/dbname
    # mysql+aiomysql://user:pass@localhost:port/dbname
    url: mysql+aiomysql://root:123456@localhost:3306/fast_web
    pool_size: 10
    max_overflow: 20
    pool_recycle: 1800
    echo_sql: True
    pool_pre_ping: True
    enable_redis: False
    cache_host: 127.0.0.1
    cache_port: 6379
    cache_pass: ""
    db_num: 0

Security Configuration
----------------------

.. code-block:: yaml

  security:
    enable: False
    enable_swagger: False
    algorithm: HS256
    secret_key: 43365f0e3e88863ff5080ac382d7717634a8ef72d8f2b52d436fc9847dbecc64
    access_token_expire_minutes: 30
    refresh_token_expire_minutes: 43200
    white_list_routes: /v1/probe/liveness, /v1/probe/readiness, /v1/user/register, /v1/user/login, /v1/user/refreshTokens
    backend_cors_origins: http://127.0.0.1:7000, http://localhost:7000, http://localhost
    black_ip_list: ""
