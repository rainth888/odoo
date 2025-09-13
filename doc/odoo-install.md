
# 运行总结


## 启动docker 数据库
- 查看状态
docker ps -a --filter name=pg170

- 启动它
docker start pg170
- 快速自测
docker exec -it pg170 psql -U postgres -c "SELECT version();"

- 给它补上自动重启策略（可在运行中修改）
docker update --restart unless-stopped pg170

## 启动odoo
- 进入虚拟环境
cd /mnt/d/_projects/odoo.github.rainth888/
source .venv/bin/activate

- 直接执行
  
python odoo-bin --addons-path=addons,addons_custom -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot -u sale_receipt_thermal
 

# 访问odoo
浏览器打开：`http://localhost:8069`

- 退出虚拟环境
deactivate

# *********************************************************************************************************************************************************

# 复制模块副本
cd /opt/odoo/custom-addons
python /data/odoo.github.rainth888/odoo-bin scaffold sale_receipt_thermal .

# shell
# Odoo Shell 方式（推荐）
python odoo-bin shell -d hello_demo

python odoo-bin shell --addons-path=addons,addons_custom -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot -u  hello_demo

# 进入交互后执行：
env.cr.execute("SELECT id,name,type,key FROM ir_ui_view WHERE name LIKE 'hello.item%' OR key LIKE '%hello_demo%';")
print(env.cr.fetchall())

# psql 方式
psql -U <db_user> -d <你的库> -c "SELECT id,name,type,key FROM ir_ui_view WHERE name LIKE 'hello.item%' OR key LIKE '%hello_demo%';"


# *********************************************************************************************************************************************************



# 创建数据库odoo

## 连接到 PostgreSQL 容器
docker exec -it pg170 psql -U postgres

## 在 PostgreSQL 中执行以下命令：
CREATE USER proot WITH PASSWORD 'proot';
CREATE DATABASE odoo OWNER proot;
GRANT ALL PRIVILEGES ON DATABASE odoo TO proot;
\q

## postgres加上强密码
docker exec -it pg170 psql -U postgres -c  "ALTER USER postgres PASSWORD '';"
docker exec -it pg170 psql -U postgres -d postgres -c "ALTER USER postgres WITH PASSWORD 'Qd#Asdfyghbk&chFdv629JkH+wq7';"


## 使用新创建的数据库运行 Odoo
python odoo-bin --addons-path=addons -d odoo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot
python odoo-bin --addons-path=addons -d odoo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i base

## 假设容器 IP 是 172.17.0.2（请根据实际 IP 调整）
python odoo-bin --addons-path=addons -d odoo --db_host=172.17.0.2 --db_port=5432 --db_user=proot --db_password=proot -i base
python odoo-bin --addons-path=addons -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot  -i base
python odoo-bin --addons-path=addons -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot



python odoo-bin --addons-path=addons,addons_custom -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot -u  hello_demo

python odoo-bin --addons-path=addons,addons_custom -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot -u sale_receipt_thermal

# ubuntu20
python odoo-bin --addons-path=addons -d odoo --db_host=172.17.0.1 --db_port=5432 --db_user=proot --db_password=Qd#969kyghb!k&chFdv5axsuH+wq7 -i base

## 给proot授权
docker exec -it pg170 psql -U postgres -c  "ALTER USER proot CREATEDB;"
  
python odoo-bin --addons-path=addons -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password='Qd#969kyghb!k&chFdv5axsuH+wq7' -i base --stop-after-init

python3 odoo-bin \
  --addons-path=addons \
  -d odoo \
  --db_host=127.0.0.1 \
  --db_port=5432 \
  --db_user=proot \
  --db_password='你的密码' \
  -i base

python odoo-bin \
  --addons-path=addons \
  -d odoo \
  --db_host=127.0.0.1 \
  --db_port=5432 \
  --db_user=proot \
  --db_password='Q*************H+wq7' \
  -i base \
  --stop-after-init

# *********************************************************************************************************************************************************


# *********************************************************************************************************************************************************


# python3.11安装


------------------------------------------------
路线 2：留在 18.04，但手动编译 3.11（**不升级系统**也能用）

1. 装编译依赖  
   ```bash
   sudo apt update
   sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
                       libnss3-dev libssl-dev libreadline-dev libffi-dev \
                       libsqlite3-dev wget libbz2-dev
   ```

2. 下载源码 & 编译  
   ```bash
   cd /tmp
   wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
   tar -xf Python-3.11.9.tgz
   cd Python-3.11.9
   ./configure --enable-optimizations --prefix=/usr/local
   make -j$(nproc)
   sudo make altinstall   # 注意 altinstall，不会覆盖系统 python3
   ```

3. 验证  
   ```bash
   /usr/local/bin/python3.11 --version
   ```

4. (可选) 做软链接/alias 方便调用  
   ```bash
   echo 'alias py311=/usr/local/bin/python3.11' >> ~/.bashrc
   source ~/.bashrc
   ```

- 运行结果：
```
postgres@leiyu-pc:~$ /usr/local/bin/python3.11 --version
Python 3.11.9
postgres@leiyu-pc:~$
postgres@leiyu-pc:~$ echo 'alias py311=/usr/local/bin/python3.11' >> ~/.bashrc
postgres@leiyu-pc:~$ vim ~/.bashrc
postgres@leiyu-pc:~$ source ~/.bashrc
postgres@leiyu-pc:~$
postgres@leiyu-pc:~$ py311
Python 3.11.9 (main, Aug 27 2025, 13:58:12) [GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
Use exit() or Ctrl-D (i.e. EOF) to exit
>>>
postgres@leiyu-pc:~$
```

## 3.11 安装 pip：

```bash
# 用 3.11 自带的 ensurepip 装（最简）
/usr/local/bin/python3.11 -m ensurepip --upgrade
```

验证：
```bash
/usr/local/bin/python3.11 -m pip --version
# 输出示例：pip 24.2 from /usr/local/lib/python3.11/site-packages/pip (python 3.11)
```

以后用 `py311 -m pip install xxx` 或进入虚拟环境后直接用 `pip install xxx`，都不会跟系统 3.6 冲突。


*********************************************************************************************************************************************************
# py311进入虚拟环境

```bash
# 先更新系统
sudo apt update
sudo apt install -y \
  build-essential pkg-config \
  libxml2-dev libxslt1-dev        # lxml
  libpq-dev                        # psycopg2
  libldap2-dev libsasl2-dev       # python-

python3.11 -m venv .venv
source .venv/bin/activate
# 验证
python -V     # Python 3.11.x
pip -V
python -m pip install --upgrade pip wheel setuptools
python -m pip install Babel

# 1) 安装编译依赖 + libpq（提供 pg_config）
apt-get update
apt-get install -y build-essential libpq-dev pkg-config

# （若随后遇到 “Python.h: No such file or directory” 再补）
# apt-get install -y python3.11-dev  || apt-get install -y python3-dev

# 2) 验证 pg_config 是否就绪
pg_config --version

# 3) 先单独装 psycopg2（可见报错更清楚），再装全体依赖
python -m pip install -U pip wheel setuptools
pip install --no-cache-dir psycopg2==2.9.5

sudo apt-get update
sudo apt-get install -y \
  build-essential pkg-config \
  libldap2-dev libsasl2-dev \
  libssl-dev libffi-dev
# 可选：若需要 Python 头文件再补（通常不必，但备着）
# sudo apt-get install -y python3-dev


# 如果项目有 requirements.txt：
pip install -r requirements.txt
# 国内可加镜像，例如：
# pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```


- 运行结果：
```
bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ python3.11 -m venv .venv
bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ source .venv/bin/activate
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ python -V
Python 3.11.9
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ pip -V
pip 24.0 from /mnt/d/_projects/odoo.github.rainth888/.venv/lib/python3.11/site-packages/pip (python 3.11)
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$
```

运行结果：
```
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ python -m pip install --upgrade pip wheel setuptools
Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (24.0)
Collecting pip
  Downloading pip-25.2-py3-none-any.whl.metadata (4.7 kB)
Collecting wheel
  Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
Requirement already satisfied: setuptools in ./.venv/lib/python3.11/site-packages (65.5.0)
Collecting setuptools
  Downloading setuptools-80.9.0-py3-none-any.whl.metadata (6.6 kB)
Downloading pip-25.2-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 1.6 MB/s eta 0:00:00
Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 5.6 MB/s eta 0:00:00
Downloading setuptools-80.9.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 5.1 MB/s eta 0:00:00
Installing collected packages: wheel, setuptools, pip
  Attempting uninstall: setuptools
    Found existing installation: setuptools 65.5.0
    Uninstalling setuptools-65.5.0:
      Successfully uninstalled setuptools-65.5.0
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-25.2 setuptools-80.9.0 wheel-0.45.1
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$
```

5. 退出虚拟环境

```bash
deactivate
```


##  总结：
> 
**创建** `python3.11 -m venv .venv`（或 `py -3.11 -m venv .venv`），
**进入** `source .venv/bin/activate`（WSL）或 `.\.venv\Scripts\Activate.ps1`（PowerShell），
然后 `pip install -r requirements.txt` 即可。



*********************************************************************************************************************************************************

# postpresql17安装


## 0) 前置确认

* **WSL2 已可用**（Ubuntu/Debian 等）。
* **Docker 可用**（任选其一）

  * **Docker Desktop + WSL 集成**（最省心），或
  * **WSL 内原生 Docker Engine**（需启用 systemd 并启动 `docker` 服务）。

自检：

```bash
apt  install docker.io  # version 26.1.3-0ubuntu1~20.04.1
docker version
docker run --rm hello-world
```

---

## 1) 拉起 PostgreSQL 17 容器（持久化 + 端口）

> 推荐把数据放在 WSL 的 Linux 目录（非 `/mnt/c`），性能更好。

```bash
# 创建数据目录（宿主机）
mkdir -p $HOME/pg17-data
mkdir -p pg17-data

# 启动容器（固定 17.0；想跟随 17.x 最新补丁可改为 postgres:17）
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0

# ubuntu20  
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v /data/pg17-data:/var/lib/postgresql/data \
  postgres:17.0

```

> 如果 `-p 5432:5432` 报“address already in use”，说明宿主 5432 被占：
>
> * 查占用：`sudo ss -ltnp | grep :5432`
> * 临时改宿主口：`-p 5433:5432`（连接改用 5433），或停止占用者（本地 pg/其他容器）。

---

## 2) 启动后自检（日志、就绪、版本）

```bash
# 看启动日志（应出现 ready to accept connections）
docker logs -f pg170 | sed -n '1,120p'

# 数据库就绪探测
docker exec pg170 pg_isready -U postgres -h 127.0.0.1 -p 5432

# 版本验证
docker exec -it pg170 psql -U postgres -c "SELECT version();"
```

---

## 3) 账号/密码/数据库配置（两种方式）

### 方式 A：**一次性在首次启动时用环境变量初始化**（最简单）

> 仅对**第一次**初始化数据目录有效，已有数据目录不会再次应用。

```bash
docker rm -f pg170
rm -rf $HOME/pg17-data/*   # ⚠️ 清空旧数据（谨慎）

docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_USER=proot \
  -e POSTGRES_PASSWORD=proot \
  -e POSTGRES_DB=pdemo \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0

# ubuntu20  
docker rm -f pg170
rm -rf /data/pg17-data/*   # ⚠️ 清空旧数据（谨慎）
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_USER=proot \
  -e POSTGRES_PASSWORD=proot \
  -e POSTGRES_DB=odoo \
  -p 5432:5432 \
  -v /data/pg17-data:/var/lib/postgresql/data \
  postgres:17.0  
```



## 4) 常用运行状态与管理

```bash
# 查看容器
docker ps
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"

# 查看日志
docker logs -f pg170

# 进容器 shell
docker exec -it pg170 bash

# 重启/停止/删除
docker restart pg170
docker stop pg170
docker rm -f pg170
```






## 模块安装

是的，完全可以！Odoo 支持动态安装和卸载模块，这是它的一个重要特性。

**后续安装模块的方法：**

**1. 通过命令行安装：**
```bash
# 安装单个模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i sale

# 安装多个模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i sale,purchase,stock

# 更新已安装的模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -u sale
```

**2. 通过 Web 界面安装（推荐）：**
```bash
# 先启动 Odoo 服务
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot

# 然后在浏览器中访问：http://localhost:8069
# 使用管理员账户登录后，可以：
# - 进入 Apps 菜单
# - 搜索需要的模块
# - 点击 Install 按钮安装

# ubuntu20
# 然后在浏览器中访问：http://103.100.211.232:8069

```

**3. 常用模块组合：**
```bash
# 基础业务模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i sale,purchase,stock

# 人力资源模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i hr,hr_recruitment,hr_timesheet

# CRM 模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i crm,crm_livechat
```

**4. 模块管理命令：**
```bash
# 列出已安装的模块
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot --list-modules

# 卸载模块（谨慎使用）
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot --uninstall-module sale
```

**重要提示：**
- 安装新模块时，Odoo 会自动处理模块间的依赖关系
- 某些模块卸载可能会影响数据完整性，建议在测试环境中先尝试
- 通过 Web 界面安装更直观，可以预览模块功能
- 建议先安装基础模块（如 `base`），再根据需要逐步添加其他模块

所以你现在可以放心地只安装 `base` 模块来初始化数据库，后续需要什么功能再随时添加对应的模块！


*********************************************************************************************************************************************************


# postgreSQL 数据库创建

下面给出**正确的三步式写法**（角色用 DO；建库用 `\gexec`，这样不在事务里；最后再切库建扩展）。可以直接复制逐段执行——每段都可反复执行，幂等。

---

## ① 创建/更新角色（幂等）

```bash
docker exec -i pg170 psql -U postgres <<'SQL'
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'proot') THEN
    CREATE ROLE proot LOGIN PASSWORD 'proot';
  ELSE
    ALTER ROLE proot WITH LOGIN PASSWORD 'proot';
  END IF;
END$$;
SQL
```

## ② “如果不存在就建库”（不能放在 DO 里）

> 这里用 `\gexec`：当查询返回一行 `CREATE DATABASE ...` 时，psql 会把它当 SQL 立刻执行。默认是自动提交，不在事务里，所以 **CREATE DATABASE** 可执行。

```bash
docker exec -i pg170 psql -U postgres <<'SQL'
-- 仅当 pdemo 不存在时创建
SELECT 'CREATE DATABASE pdemo OWNER proot'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pdemo') \gexec
SQL
```

## ③ 切到 pdemo 库开常用扩展（幂等）

```bash
docker exec -i pg170 psql -U postgres -d pdemo <<'SQL'
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SQL
```

---

## 验证（可选）

```bash
# 看角色
docker exec -it pg170 psql -U postgres -c "\du+ proot"

# 看库
docker exec -it pg170 psql -U postgres -c "\l+ pdemo"

# 在 pdemo 里看扩展
docker exec -it pg170 psql -U postgres -d pdemo -c "\dx"
```

---

### 进阶：把上面三段合并为“一次执行”的脚本（仍然分三次 psql 调用）

```bash
docker exec -i pg170 bash <<'BASH'
set -e

psql -U postgres <<'SQL'
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'proot') THEN
    CREATE ROLE proot LOGIN PASSWORD 'proot';
  ELSE
    ALTER ROLE proot WITH LOGIN PASSWORD 'proot';
  END IF;
END$$;
SQL

psql -U postgres <<'SQL'
SELECT 'CREATE DATABASE pdemo OWNER proot'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pdemo') \gexec
SQL

psql -U postgres -d pdemo <<'SQL'
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SQL
BASH
```

> 关键点回顾：
>
> * **DO/函数/事务块里不能 `CREATE DATABASE`**。
> * 用 `\gexec` 生成并执行 `CREATE DATABASE`，它走自动提交，不在事务里。
> * 只有**确认库已存在**之后再 `\c pdemo` 或在 `-d pdemo` 上执行后续 SQL。


### 运行结果
```
bill@leiyu-pc:~$ docker exec -i pg170 psql -U postgres <<'SQL'
> DO $$
OT EXISTS (SELEC> BEGIN
>   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'proot') THEN
>     CREATE ROLE proot LOGIN PASSWORD 'proot';
>   ELSE
>     ALTER ROLE proot WITH LOGIN PASSWORD 'proot';
>   END IF;
ND$$;
SQL> END$$;
> SQL
DO
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$ docker exec -i pg170 psql -U postgres <<'SQL'
> -- 仅当 pdemo 不存在时创建
> SELECT 'CREATE DATABASE pdemo OWNER proot'
> WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pdemo') \gexec
> SQL
CREATE DATABASE
bill@leiyu-pc:~$
bill@leiyu-pc:~$ docker exec -i pg170 psql -U postgres -d pdemo <<'SQL'
> CREATE EXTENSION IF NOT EXISTS pg_trgm;
> CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
> SQL
CREATE EXTENSION
CREATE EXTENSION
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$ docker exec -it pg170 psql -U postgres -c "\du+ proot"
            List of roles
 Role name | Attributes | Description
-----------+------------+-------------
 proot     |            |

bill@leiyu-pc:~$ docker exec -it pg170 psql -U postgres -c "\l+ pdemo"
                                                                 List of databases
 Name  | Owner | Encoding | Locale Provider |  Collate   |   Ctype    | Locale | ICU Rules | Access privileges |  Size   | Tablespace | Description
-------+-------+----------+-----------------+------------+------------+--------+-----------+-------------------+---------+------------+-------------
 pdemo | proot | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           |                   | 7619 kB | pg_default |
(1 row)

bill@leiyu-pc:~$
bill@leiyu-pc:~$ docker exec -it pg170 psql -U postgres -d pdemo -c "\dx"
                                     List of installed extensions
   Name    | Version |   Schema   |                            Description
-----------+---------+------------+-------------------------------------------------------------------
 pg_trgm   | 1.6     | public     | text similarity measurement and index searching based on trigrams
 plpgsql   | 1.0     | pg_catalog | PL/pgSQL procedural language
 uuid-ossp | 1.1     | public     | generate universally unique identifiers (UUIDs)
(3 rows)

bill@leiyu-pc:~$
```

```
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ docker inspect pg170 | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.2",
                    "IPAddress": "172.17.0.2",
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$ docker port pg170
5432/tcp -> 0.0.0.0:5432
5432/tcp -> [::]:5432
(.venv) bill@leiyu-pc:/d/_projects/odoo.github.rainth888$


# 假设容器 IP 是 172.17.0.2（请根据实际 IP 调整）
python odoo-bin --addons-path=addons -d pdemo --db_host=172.17.0.2 --db_port=5432 --db_user=proot --db_password=proot

# 如果容器在默认网络中，使用容器名
python odoo-bin --addons-path=addons -d pdemo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot

```

* 角色 **proot** 已创建（`\du+ proot` 显示存在；无特殊属性=正常）。
* 数据库 **pdemo** 已创建，**Owner=proot**。
* 扩展 **pg\_trgm**、**uuid-ossp** 已在 **pdemo** 中启用（`\dx` 显示 ok）。

下面给你几步“收尾优化 + 自测 + 远程访问”小清单（可选但推荐）。

---

## 1) 用业务账号自测连接

```bash
docker exec -e PGPASSWORD=proot -it pg170 \
  psql -U proot -d pdemo -h 127.0.0.1 -c "select current_user, current_database();"
```

期望输出 `proot | pdemo`。

---

## 2) 建独立 schema + 设默认权限（推荐做法）

避免直接在 `public` 下建表，给业务一个独立 schema 和清晰的默认权限。

```bash
# 在 pdemo 库中执行
docker exec -it pg170 psql -U postgres -d pdemo <<'SQL'
-- 1) 业务 schema
CREATE SCHEMA IF NOT EXISTS app AUTHORIZATION proot;

-- 2) 设默认搜索路径（先找 app，再找 public）
ALTER DATABASE pdemo SET search_path = app, public;

-- 3) 将现有对象授权（第一次初始化时一般没有对象，可留作模板）
GRANT USAGE ON SCHEMA app TO proot;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA app TO proot;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA app TO proot;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA app TO proot;

-- 4) 未来新建对象的默认权限（proot 创建的对象对自己当然有权限；
-- 如果你还有其他读写账号，可在这里一并 GRANT）
ALTER DEFAULT PRIVILEGES FOR USER proot IN SCHEMA app
  GRANT ALL ON TABLES TO proot;
ALTER DEFAULT PRIVILEGES FOR USER proot IN SCHEMA app
  GRANT ALL ON SEQUENCES TO proot;
ALTER DEFAULT PRIVILEGES FOR USER proot IN SCHEMA app
  GRANT ALL ON FUNCTIONS TO proot;
SQL
```

> 以后应用里直接用 `schema.table` 或依赖 `search_path` 即可。

---

## 3) 可选的角色属性/安全强化

```bash
# 如需创建库：给 proot 赋权（通常不必）
# docker exec -it pg170 psql -U postgres -c "ALTER ROLE proot CREATEDB;"

# 修改超管密码（容器初始是 postgres/postgres，建议修改）
# docker exec -it pg170 psql -U postgres -c "ALTER USER postgres WITH PASSWORD '更强的密码';"
```

---

## 4) 远程访问（仅在需要从其他主机访问时）

进入容器修改配置，然后重启容器。

```bash
# 进入容器
docker exec -it pg170 bash

# 1) 监听所有地址（或内网地址）
sed -i "s/^#\?listen_addresses.*/listen_addresses = '*'/" /var/lib/postgresql/data/postgresql.conf

# 2) 访问控制：允许内网网段用密码认证（举例 192.168.0.0/16）
echo "host  all  all  192.168.0.0/16  md5" >> /var/lib/postgresql/data/pg_hba.conf
exit

# 重启
docker restart pg170
```

> 在 Windows/Docker Desktop 场景，**还要**确保 Windows 防火墙放行 5432（或你映射的端口）。
> 仅在可信内网开放，强密码 + 精确网段白名单，不要对公网裸露。

---

## 5) 常用状态检查

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
docker logs -f pg170
docker exec pg170 pg_isready -U postgres -h 127.0.0.1 -p 5432
```

---

## 6) 备份/恢复（随手可用）

```bash
# 备份单库（压缩格式）
docker exec pg170 pg_dump -U postgres -Fc pdemo > ~/pg17-backups/pdemo_$(date +%F_%H%M%S).dump

# 恢复到 pdemo（已存在库）
docker exec -i pg170 pg_restore -U postgres --clean --if-exists -d pdemo < ~/pg17-backups/pdemo_xxx.dump
```



## 问题

wsl2中执行结果如下：
```
bill@leiyu-pc:~$ ip route | awk '/default/ {print $3}'
172.19.128.1
bill@leiyu-pc:~$
```
windows11下执行结果如下：
```
E:\_projects\ax-ipcdemo-webserver>ping 172.19.128.1                                                                                                                                                                                             Pinging 172.19.128.1 with 32 bytes of data:                                                                             Reply from 172.19.128.1: bytes=32 time<1ms TTL=128                                                                      Reply from 172.19.128.1: bytes=32 time<1ms TTL=128                                                                      Reply from 172.19.128.1: bytes=32 time<1ms TTL=128                                                                                                                                                                                              172.19.128.1 的 Ping 统计信息:                                                                                              数据包: 已发送 = 3，已接收 = 3，丢失 = 0 (0% 丢失)，                                                                往返行程的估计时间(以毫秒为单位):                                                                                           最短 = 0ms，最长 = 0ms，平均 = 0ms                                                                                  Control-C                                                                                                               ^C                                                                                                                      E:\_projects\ax-ipcdemo-webserver>telnet 172.19.128.1 5432                                                              Connecting To 172.19.128.1...Could not open connection to the host, on port 5432: Connect failed                         
```





*********************************************************************************************************************************************************

# windows11连接postgresql

你在 Windows 里 `telnet 172.19.128.1 5432` 连不上，是因为：

* **172.19.128.1 是 Windows 在 WSL 网段的网关 IP**（WSL → Windows 用的），并不是 WSL 实例或容器的地址；
* 你要从 **Windows → WSL 容器**，应连 **WSL 实例的 IP** 或（若开启了端口映射）直接连 **localhost**。

按下面检查与连接即可：

---

## 1) 确认容器端口是否已对外发布

在 WSL 中执行：

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
# 期望看到类似：pg170   0.0.0.0:5432->5432/tcp
```

再看绑定：

```bash
sudo ss -ltnp | grep :5432
# 期望看到 0.0.0.0:5432 ... docker-proxy(或 dockerd)
```

> 如果这里显示 `127.0.0.1:5432`，说明只绑定了回环；重建容器时用：
>
> ```bash
> docker rm -f pg170
> docker run -d --name pg170 \
>   -p 0.0.0.0:5432:5432 \
>   -e POSTGRES_PASSWORD=postgres \
>   -v $HOME/pg17-data:/var/lib/postgresql/data \
>   postgres:17.0
> ```

---

## 2) 取 **WSL 实例的 IP**（不是 172.19.128.1）

在 WSL 里：

```bash
ip -4 addr show eth0 | awk '/inet /{print $2}'        # 例如输出 172.19.134.133/20
```

取斜杠前的地址，例如 `172.19.134.133`。

在 **Windows PowerShell** 测试：

```powershell
Test-NetConnection 172.19.134.133 -Port 5432
# 或老办法：telnet 172.19.134.133 5432
```

成功就能用客户端连了：

```powershell
# 用 psql（若已安装在 Windows）
psql -h 172.19.134.133 -p 5432 -U proot -d pdemo
```

---

## 3) 如果你的 WSL 开了 “localhost 端口转发”

新版本 WSL 会把 WSL 的监听端口映射到 Windows 的 `localhost`。直接在 Windows 测：

```powershell
Test-NetConnection 127.0.0.1 -Port 5432
# 通过则客户端直接连 localhost:5432
```

> 若不通，可能该功能没启或被策略影响，就按 **步骤 2** 用 WSL 实例 IP 连接即可。

---

## 4) 远程访问（从其他机器连）

仅当你要让**别的机器**访问本机时需要这步：

1. 进入容器，确认 `listen_addresses='*'`（官方镜像一般默认放开）与 `pg_hba.conf` 添加内网白名单：

   ```bash
   docker exec -it pg170 bash
   sed -i "s/^#\?listen_addresses.*/listen_addresses = '*'/" /var/lib/postgresql/data/postgresql.conf
   echo "host  all  all  192.168.0.0/16  md5" >> /var/lib/postgresql/data/pg_hba.conf
   exit
   docker restart pg170
   ```
2. 在 **Windows 防火墙** 放行 5432（Docker Desktop 场景下尤需注意）。

---

## 5) 一行自检总览（可贴回结果）

在 WSL 执行：

```bash
echo "WSL_IP=$(hostname -I)"; \
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"; \
sudo ss -ltnp | grep :5432 || true
```

* 确认 **WSL\_IP**（用它在 Windows 连接）。
* `Ports` 一列应有 `0.0.0.0:5432->5432/tcp`。
* `ss` 输出应是 `0.0.0.0:5432` 由 docker-proxy/dockerd 监听。

---

### 小结

* **从 Windows 连 WSL 容器**：用 **WSL 实例 IP:端口**（例如 `172.19.134.xxx:5432`），或者如果开启了**localhost 转发**，直接 `localhost:5432`。
* **172.19.128.1 是 Windows 的网关地址**，不是你要连的目标。

### 运行结果
```
bill@leiyu-pc:~$ ip route | awk '/default/ {print $3}'
172.19.128.1
bill@leiyu-pc:~$ docker exec -it pg170 bash
root@2a1ca53db6b0:/# sed -i "s/^#\?listen_addresses.*/listen_addresses = '*'/" /var/lib/postgresql/data/postgresql.conf
root@2a1ca53db6b0:/# echo "host  all  all  192.168.0.0/16  md5" >> /var/lib/postgresql/data/pg_hba.conf
root@2a1ca53db6b0:/# exit
exit
bill@leiyu-pc:~$ docker restart pg170
pg170
bill@leiyu-pc:~$ docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
NAMES     PORTS                                       STATUS
pg170     0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   Up 9 minutes
bill@leiyu-pc:~$
bill@leiyu-pc:~$ sudo ss -ltnp | grep :5432
[sudo] password for bill:
LISTEN   0         4096                 0.0.0.0:5432            0.0.0.0:*        users:(("docker-proxy",pid=4409,fd=4))
LISTEN   0         4096                    [::]:5432               [::]:*        users:(("docker-proxy",pid=4434,fd=4))
bill@leiyu-pc:~$
bill@leiyu-pc:~$ ip -4 addr show eth0 | awk '/inet /{print $2}'
172.19.134.133/20
bill@leiyu-pc:~$

```

telnet 172.19.134.133是成功的，但是使用客户端数据库连接工具navicat premium就连接不上，显示见附件。


*********************************************************************************************************************************************************
# docker 引擎安装 

## 方案 B：在 WSL 里安装原生 Docker Engine（Ubuntu/Debian）

> 仅当你**不想装 Docker Desktop** 时使用。WSL 里建议启用 systemd，方便管理服务。

1. **启用 systemd（WSL 新版支持）**
   在 WSL 编辑 `/etc/wsl.conf`：

   ```ini
   [boot]
   systemd=true
   ```

   退出到 Windows PowerShell：

   ```powershell
   wsl --shutdown
   ```

   重新进入 WSL。

2. **安装 Docker 官方仓库与引擎**

   ```bash
   sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
   sudo apt update
   sudo apt install -y ca-certificates curl gnupg lsb-release

   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
     sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
     https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo $VERSION_CODENAME) stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

3. **启动并设置自启动**

   ```bash
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   newgrp docker   # 或重新登录一次，让 docker 组生效
   docker run --rm hello-world
   ```

4. **运行 PostgreSQL 17.0**

   ```bash
   docker run -d --name pg170 \
     -e POSTGRES_PASSWORD=postgres \
     -p 5432:5432 \
     -v $HOME/pg17-data:/var/lib/postgresql/data \
     postgres:17.0
   docker exec -it pg170 psql -U postgres -c "SELECT version();"
   ```

---

## 常见排错

* **客户端能用但仍报 sock 连接失败**：说明**引擎没跑**。

  * Docker Desktop：确保小鲸鱼 Running，WSL Integration 开启，`docker context use desktop-linux`。
  * 原生 Engine：确认 `sudo systemctl status docker` 为 active。
* **端口占用**：`0.0.0.0:5432` 被占时，改容器映射为 `-p 5433:5432`，从 Windows 用 `localhost:5433` 连接。
* **磁盘路径**：建议把卷挂到 WSL 的 Linux 路径（如 `$HOME/pg17-data`），**不要挂 `/mnt/c/...`**（性能差）。
* **公司/代理网络**：Docker 拉镜像失败时，配置代理（Docker Desktop Settings → Resources → Proxies，或 Engine 配置 `/etc/systemd/system/docker.service.d/proxy.conf`）。

---

### 一键验证清单（你可以逐条执行）

```bash
# 检查上下文
docker context ls

# 版本信息（客户端+服务端）
docker version

# 拉取并跑一次 hello-world
docker run --rm hello-world
```

确认通过后，再跑你原来的 `postgres:17.0` 命令就好了。需要我给你做一个“安装 + 启动 + 运行 PG17”的一键脚本（按你选择 A 或 B）吗？

```
bill@leiyu-pc:~$ sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
[sudo] password for bill:
Reading package lists... Done
Building dependency tree
Reading state information... Done
Package 'docker-engine' is not installed, so not removed
Package 'docker' is not installed, so not removed
The following packages were automatically installed and are no longer required:
  bridge-utils pigz ubuntu-fan
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  containerd docker.io runc
0 upgraded, 0 newly installed, 3 to remove and 0 not upgraded.
After this operation, 291 MB disk space will be freed.
(Reading database ... 53326 files and directories currently installed.)
Removing docker.io (20.10.21-0ubuntu1~18.04.3) ...
invoke-rc.d: unknown initscript, /etc/init.d/docker not found.
invoke-rc.d: could not determine current runlevel
Removing containerd (1.6.12-0ubuntu1~18.04.1) ...
Removing runc (1.1.4-0ubuntu1~18.04.2) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
[master 9c1aa2c] committing changes in /etc after apt run
 Author: bill <bill@leiyu-pc.localdomain>
 4 files changed, 3 insertions(+), 2 deletions(-)
 create mode 120000 systemd/system/containerd.service
 create mode 120000 systemd/system/docker.service
 create mode 120000 systemd/system/docker.socket

bill@leiyu-pc:~$ sudo apt update
Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [102 kB]
Hit:2 http://archive.ubuntu.com/ubuntu bionic InRelease
Get:4 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [102 kB]
Get:3 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease [15.9 kB]
Err:3 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
Get:5 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [102 kB]
Reading package lists... Done
W: GPG error: http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
E: The repository 'http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
bill@leiyu-pc:~$ sudo apt install -y ca-certificates curl gnupg lsb-release
Reading package lists... Done
Building dependency tree
Reading state information... Done
lsb-release is already the newest version (9.20170808ubuntu1).
lsb-release set to manually installed.
ca-certificates is already the newest version (20230311ubuntu0.18.04.1).
curl is already the newest version (7.58.0-2ubuntu3.24).
gnupg is already the newest version (2.2.4-1ubuntu1.6).
gnupg set to manually installed.
The following packages were automatically installed and are no longer required:
  bridge-utils pigz ubuntu-fan
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
bill@leiyu-pc:~$ sudo install -m 0755 -d /etc/apt/keyrings
bill@leiyu-pc:~$

bill@leiyu-pc:~$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
 sudo gpg --dear>      sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
gpg: WARNING: unsafe ownership on homedir '/home/bill/.gnupg'
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$ echo \
>      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
>      https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo $VERSION_CODENAME) stable" | \
>      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
bill@leiyu-pc:~$ sudo apt update
Hit:1 http://security.ubuntu.com/ubuntu bionic-security InRelease
Hit:3 http://archive.ubuntu.com/ubuntu bionic InRelease
Get:4 https://download.docker.com/linux/ubuntu bionic InRelease [64.4 kB]
Get:2 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease [15.9 kB]
Hit:5 http://archive.ubuntu.com/ubuntu bionic-updates InRelease
Get:6 https://download.docker.com/linux/ubuntu bionic/stable amd64 Packages [39.0 kB]
Err:2 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
Hit:7 http://archive.ubuntu.com/ubuntu bionic-backports InRelease
Reading package lists... Done
W: GPG error: http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
E: The repository 'http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.

bill@leiyu-pc:~$ sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following packages were automatically installed and are no longer required:
  bridge-utils ubuntu-fan
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  docker-ce-rootless-extras libltdl7
Suggested packages:
  aufs-tools cgroupfs-mount | cgroup-lite
Recommended packages:
  slirp4netns
The following NEW packages will be installed:
  containerd.io docker-buildx-plugin docker-ce docker-ce-cli docker-ce-rootless-extras docker-compose-plugin libltdl7
0 upgraded, 7 newly installed, 0 to remove and 0 not upgraded.
Need to get 111 MB of archives.
After this operation, 401 MB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu bionic/main amd64 libltdl7 amd64 2.4.6-2 [38.8 kB]
Get:2 https://download.docker.com/linux/ubuntu bionic/stable amd64 containerd.io amd64 1.6.21-1 [28.3 MB]
Get:3 https://download.docker.com/linux/ubuntu bionic/stable amd64 docker-buildx-plugin amd64 0.10.5-1~ubuntu.18.04~bionic [26.1 MB]
Get:4 https://download.docker.com/linux/ubuntu bionic/stable amd64 docker-ce-cli amd64 5:24.0.2-1~ubuntu.18.04~bionic [13.3 MB]
Get:5 https://download.docker.com/linux/ubuntu bionic/stable amd64 docker-ce amd64 5:24.0.2-1~ubuntu.18.04~bionic [22.9 MB]
Get:6 https://download.docker.com/linux/ubuntu bionic/stable amd64 docker-ce-rootless-extras amd64 5:24.0.2-1~ubuntu.18.04~bionic [9014 kB]
Get:7 https://download.docker.com/linux/ubuntu bionic/stable amd64 docker-compose-plugin amd64 2.18.1-1~ubuntu.18.04~bionic [10.9 MB]
Fetched 111 MB in 11s (9664 kB/s)
[master b360ed2] saving uncommitted changes in /etc prior to apt run
 Author: bill <bill@leiyu-pc.localdomain>
 3 files changed, 4 insertions(+)
 create mode 100644 apt/keyrings/docker.gpg
 create mode 100644 apt/sources.list.d/docker.list
Selecting previously unselected package containerd.io.
(Reading database ... 53062 files and directories currently installed.)
Preparing to unpack .../0-containerd.io_1.6.21-1_amd64.deb ...
Unpacking containerd.io (1.6.21-1) ...
Selecting previously unselected package docker-buildx-plugin.
Preparing to unpack .../1-docker-buildx-plugin_0.10.5-1~ubuntu.18.04~bionic_amd64.deb ...
Unpacking docker-buildx-plugin (0.10.5-1~ubuntu.18.04~bionic) ...
Selecting previously unselected package docker-ce-cli.
Preparing to unpack .../2-docker-ce-cli_5%3a24.0.2-1~ubuntu.18.04~bionic_amd64.deb ...
Unpacking docker-ce-cli (5:24.0.2-1~ubuntu.18.04~bionic) ...
Selecting previously unselected package docker-ce.
Preparing to unpack .../3-docker-ce_5%3a24.0.2-1~ubuntu.18.04~bionic_amd64.deb ...
Unpacking docker-ce (5:24.0.2-1~ubuntu.18.04~bionic) ...
Selecting previously unselected package docker-ce-rootless-extras.
Preparing to unpack .../4-docker-ce-rootless-extras_5%3a24.0.2-1~ubuntu.18.04~bionic_amd64.deb ...
Unpacking docker-ce-rootless-extras (5:24.0.2-1~ubuntu.18.04~bionic) ...
Selecting previously unselected package docker-compose-plugin.
Preparing to unpack .../5-docker-compose-plugin_2.18.1-1~ubuntu.18.04~bionic_amd64.deb ...
Unpacking docker-compose-plugin (2.18.1-1~ubuntu.18.04~bionic) ...
Selecting previously unselected package libltdl7:amd64.
Preparing to unpack .../6-libltdl7_2.4.6-2_amd64.deb ...
Unpacking libltdl7:amd64 (2.4.6-2) ...
Setting up containerd.io (1.6.21-1) ...
Setting up docker-ce-rootless-extras (5:24.0.2-1~ubuntu.18.04~bionic) ...
Setting up docker-buildx-plugin (0.10.5-1~ubuntu.18.04~bionic) ...
Setting up libltdl7:amd64 (2.4.6-2) ...
Setting up docker-compose-plugin (2.18.1-1~ubuntu.18.04~bionic) ...
Setting up docker-ce-cli (5:24.0.2-1~ubuntu.18.04~bionic) ...
Setting up docker-ce (5:24.0.2-1~ubuntu.18.04~bionic) ...
invoke-rc.d: could not determine current runlevel
Processing triggers for libc-bin (2.27-3ubuntu1.6) ...
Processing triggers for systemd (237-3ubuntu10.57) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
Processing triggers for ureadahead (0.100.0-21) ...
[master fb949a6] committing changes in /etc after apt run
 Author: bill <bill@leiyu-pc.localdomain>
 15 files changed, 293 insertions(+), 3 deletions(-)
 create mode 100644 containerd/config.toml
 create mode 100644 default/docker
 create mode 100755 init.d/docker
 create mode 100644 init/docker.conf
 create mode 120000 rc0.d/K01docker
 create mode 120000 rc1.d/K01docker
 create mode 120000 rc2.d/S01docker
 create mode 120000 rc3.d/S01docker
 create mode 120000 rc4.d/S01docker
 create mode 120000 rc5.d/S01docker
 create mode 120000 rc6.d/K01docker
 delete mode 120000 systemd/system/containerd.service
 delete mode 120000 systemd/system/docker.service
 delete mode 120000 systemd/system/docker.socket

bill@leiyu-pc:~$ sudo systemctl enable --now docker
Synchronizing state of docker.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable docker
System has not been booted with systemd as init system (PID 1). Can't operate.
bill@leiyu-pc:~$

```


*********************************************************************************************************************************************************


## 路线 1（推荐）：启用 systemd，再安装/启动 Docker Engine

1. **在 WSL 里启用 systemd**

```bash
# 编辑 /etc/wsl.conf，增加如下内容
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

在 **Windows PowerShell** 完全重启 WSL：

```powershell
wsl --shutdown
```

重新进入 WSL，确认：

```bash
ps -p 1 -o comm=       # 应显示 systemd
systemctl is-system-running
```

2. **安装 Docker（Ubuntu/Debian 示例）**

```bash
# 清理旧包（忽略报错）
sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true

sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo $VERSION_CODENAME) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. **启动 Docker 服务并加入用户组**

```bash
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker       # 或退出重登终端
docker run --rm hello-world
```

4. **跑你的 PostgreSQL 17.0**

```bash
docker run -d --name pg170 \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0

docker exec -it pg170 psql -U postgres -c "SELECT version();"
```

> 若 5432 被占用，改成 `-p 5433:5432`，Windows 端用 `localhost:5433` 连接。

---

## 路线 2（更省事）：用 **Docker Desktop** 的 WSL 集成

1. Windows 装并启动 **Docker Desktop**。
2. Settings → **General**：勾 **Use the WSL 2 based engine**。
   Settings → **Resources → WSL Integration**：勾选你的发行版。
3. 回到 WSL 测试：

```bash
docker version
docker run --rm hello-world
```

通过后直接运行你的 PG 容器命令即可（与上面相同）。

---

## 备选：不启用 systemd 时临时拉起 dockerd（不建议长期用）

```bash
# 前提是已安装 docker-ce / containerd
sudo /usr/bin/dockerd >/tmp/dockerd.log 2>&1 &
docker info
```

> 这种方式缺少服务管理与自启，适合临时测试。

---

报错关键信息：

```
lookup registry-1.docker.io on [::1]:53: read udp [::1]:53251->[::1]:53: read: connection refused
```

这表示 **Docker 守护进程在用本机 IPv6 回环地址 `::1:53` 做 DNS**，但本机没有在该端口提供解析服务 → **拉镜像前的域名解析就失败**。

给你两条修法，按你实际使用的是 **Docker Desktop** 还是 **WSL 内原生 Docker Engine** 选择其一即可。

---

## 方案 A：你在用 Docker Desktop（最常见、最省心）

1. 打开 **Docker Desktop → Settings**
2. **Resources → Network**：把 **DNS Server** 改为手动，比如：

   * `1.1.1.1`、`8.8.8.8`（或你公司内网 DNS，如 `192.168.110.1` 但需支持递归）
3. （可选）**Proxies**：若公司需代理，填上 `HTTP/HTTPS Proxy`（你之前可用的是 `http://172.19.128.1:7890`）。
4. **Apply & Restart** Docker Desktop。
5. 回到 WSL 测试：

   ```bash
   docker run --rm hello-world
   ```

---

## 方案 B：你在 WSL 里跑原生 Docker Engine（非 Desktop）

给 Docker 守护进程显式指定可用 DNS，并重启守护进程。

1. 写入守护进程配置（**/etc/docker/daemon.json**）：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json >/dev/null <<'EOF'
{
  "dns": ["1.1.1.1", "8.8.8.8"],
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF
```

2. 重启 Docker（取决于你是否启用了 systemd）：

```bash
# 启用了 systemd（推荐做法）
sudo systemctl daemon-reload
sudo systemctl restart docker

# 如果还没启用 systemd，就临时手动重启 dockerd：
# (确保已安装 docker-ce/containerd)
# sudo pkill dockerd
# sudo nohup dockerd >/tmp/dockerd.log 2>&1 &
```

3. 再试：

```bash
docker run --rm hello-world
```

> 说明：拉取镜像前的 DNS 解析发生在 **Docker 守护进程** 一侧，
> 仅给 “容器” 加 `--dns` **无法**解决“拉取前解析”的问题；必须改 **daemon 级 DNS**（或在 Docker Desktop 里改）。

---

## 可能的企业网络加固（如需）

* **为 Docker 守护进程设置代理**（拉镜像要走公司代理时）：

  ```bash
  sudo mkdir -p /etc/systemd/system/docker.service.d
  sudo tee /etc/systemd/system/docker.service.d/proxy.conf >/dev/null <<'EOF'
  [Service]
  Environment="HTTP_PROXY=http://172.19.128.1:7890"
  Environment="HTTPS_PROXY=http://172.19.128.1:7890"
  Environment="NO_PROXY=localhost,127.0.0.1,::1,.local,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
  EOF

  sudo systemctl daemon-reload
  sudo systemctl restart docker
  ```
* **校验证书**：若公司代理有自签 CA，把根证书装进 WSL：`sudo cp corp-root-ca.crt /usr/local/share/ca-certificates/ && sudo update-ca-certificates`。

---

### 快速自检清单

```bash
# 看 docker 服务端是否可用
docker version

# 解析是否恢复（跑一次拉取）
docker run --rm hello-world

# 如仍失败，贴出：
# 1) cat /etc/docker/daemon.json
# 2) docker info | sed -n '1,80p'（前 80 行）
# 3) 你使用的是 Docker Desktop 还是 WSL 原生 Engine
```

按上面把 **daemon 的 DNS** 指到可用服务器后，你的 `docker run --rm hello-world` 就能正常拉取并运行了。









### 运行结果
```
bill@leiyu-pc:~$ ps -p 1 -o comm=
systemd
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$ systemctl is-system-running
running
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$ sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
[sudo] password for bill:
Reading package lists... Done
Building dependency tree
Reading state information... Done
Package 'docker-engine' is not installed, so not removed
Package 'docker' is not installed, so not removed
Package 'containerd' is not installed, so not removed
Package 'docker.io' is not installed, so not removed
Package 'runc' is not installed, so not removed
The following packages were automatically installed and are no longer required:
  bridge-utils ubuntu-fan
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
bill@leiyu-pc:~$ sudo apt update
Hit:1 http://archive.ubuntu.com/ubuntu bionic InRelease
Hit:2 http://security.ubuntu.com/ubuntu bionic-security InRelease
Hit:4 https://download.docker.com/linux/ubuntu bionic InRelease
Hit:5 http://archive.ubuntu.com/ubuntu bionic-updates InRelease
Get:3 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease [15.9 kB]
Err:3 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
Hit:6 http://archive.ubuntu.com/ubuntu bionic-backports InRelease
Reading package lists... Done
W: GPG error: http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
E: The repository 'http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
bill@leiyu-pc:~$ sudo apt install -y ca-certificates curl gnupg lsb-release
Reading package lists... Done
Building dependency tree
Reading state information... Done
lsb-release is already the newest version (9.20170808ubuntu1).
ca-certificates is already the newest version (20230311ubuntu0.18.04.1).
curl is already the newest version (7.58.0-2ubuntu3.24).
gnupg is already the newest version (2.2.4-1ubuntu1.6).
The following packages were automatically installed and are no longer required:
  bridge-utils ubuntu-fan
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
bill@leiyu-pc:~$ sudo install -m 0755 -d /etc/apt/keyrings
bill@leiyu-pc:~$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
 -o /etc/apt/key>   sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
gpg: WARNING: unsafe ownership on homedir '/home/bill/.gnupg'
File '/etc/apt/keyrings/docker.gpg' exists. Overwrite? (y/N)
Enter new filename: docker
gpg: signal Interrupt caught ... exiting

bill@leiyu-pc:~$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg |   sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
gpg: WARNING: unsafe ownership on homedir '/home/bill/.gnupg'
File '/etc/apt/keyrings/docker.gpg' exists. Overwrite? (y/N) Y
bill@leiyu-pc:~$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
> https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo $VERSION_CODENAME) stable" | \
> sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
bill@leiyu-pc:~$ sudo apt update
Hit:1 http://archive.ubuntu.com/ubuntu bionic InRelease
Hit:3 http://security.ubuntu.com/ubuntu bionic-security InRelease
Hit:4 https://download.docker.com/linux/ubuntu bionic InRelease
Get:2 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease [15.9 kB]
Hit:5 http://archive.ubuntu.com/ubuntu bionic-updates InRelease
Err:2 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
Hit:6 http://archive.ubuntu.com/ubuntu bionic-backports InRelease
Reading package lists... Done
W: GPG error: http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY BA6932366A755776
E: The repository 'http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
bill@leiyu-pc:~$ sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
Reading package lists... Done
Building dependency tree
Reading state information... Done
containerd.io is already the newest version (1.6.21-1).
docker-buildx-plugin is already the newest version (0.10.5-1~ubuntu.18.04~bionic).
docker-ce-cli is already the newest version (5:24.0.2-1~ubuntu.18.04~bionic).
docker-ce is already the newest version (5:24.0.2-1~ubuntu.18.04~bionic).
docker-compose-plugin is already the newest version (2.18.1-1~ubuntu.18.04~bionic).
The following packages were automatically installed and are no longer required:
  bridge-utils ubuntu-fan
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
bill@leiyu-pc:~$

bill@leiyu-pc:~$ sudo systemctl enable --now docker
Synchronizing state of docker.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable docker

bill@leiyu-pc:~$ sudo usermod -aG docker $USER
bill@leiyu-pc:~$ newgrp docker
[AX620E] TOOLCHAIN=/mnt/e/_projects/ax-ipcdemo-webserver/gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu
[AX620E] SRC_DEMO=/mnt/e/_projects/ax-ipcdemo-webserver/beilu_ax630c_ipc_AX620E_SDK/app/demo/FRTDemo
[AX620E] GCC: Using built-in specs.
bill@leiyu-pc:~$

```
### docker 运行成功
```
bill@leiyu-pc:~$ docker run --rm hello-world
Unable to find image 'hello-world:latest' locally
docker: Error response from daemon: Get "https://registry-1.docker.io/v2/": dial tcp: lookup registry-1.docker.io on [::1]:53: read udp [::1]:50036->[::1]:53: read: connection refused.
See 'docker run --help'.
bill@leiyu-pc:~$ sudo mkdir -p /etc/systemd/system/docker.service.d
bill@leiyu-pc:~$ sudo vim /etc/systemd/system/docker.service.d/proxy.conf
bill@leiyu-pc:~$ sudo systemctl daemon-reload
bill@leiyu-pc:~$ sudo systemctl restart docker
bill@leiyu-pc:~$ docker run --rm hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
17eec7bbc9d7: Pull complete
Digest: sha256:a0dfb02aac212703bfcb339d77d47ec32c8706ff250850ecc0e19c8737b18567
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

bill@leiyu-pc:~$

bill@leiyu-pc:~$ docker version
Client: Docker Engine - Community
 Version:           24.0.2
 API version:       1.43
 Go version:        go1.20.4
 Git commit:        cb74dfc
 Built:             Thu May 25 21:52:13 2023
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          24.0.2
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.4
  Git commit:       659604f
  Built:            Thu May 25 21:52:13 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.21
  GitCommit:        3dce8eb055cbb6872793272b4f20ed16117344f8
 runc:
  Version:          1.1.7
  GitCommit:        v1.1.7-0-g860f061
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
bill@leiyu-pc:~$

```

### 安装 postgresql17 by docker

```
bill@leiyu-pc:~$ docker run -d --name pg170 \
e POSTGRES_PASSW>   -e POSTGRES_PASSWORD=postgres \
>   -p 5432:5432 \
>   -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0
>   postgres:17.0
Unable to find image 'postgres:17.0' locally
17.0: Pulling from library/postgres
2d429b9e73a6: Pull complete
8cd18d1b1f3c: Pull complete
efe013fcce98: Pull complete
e5f0c600cf82: Pull complete
f1c903b2aeee: Pull complete
49faa60cc715: Pull complete
744e496a897f: Pull complete
83c689f809e5: Pull complete
5dc6568b6a72: Pull complete
5e679d2c32d2: Pull complete
4905c4cdeae1: Pull complete
15266ecdce80: Pull complete
37c10b51b83c: Pull complete
3c636afee197: Pull complete
Digest: sha256:f176fef320ed02c347e9f85352620945547a9a23038f02b57cf7939a198182ae
Status: Downloaded newer image for postgres:17.0
554f29fe542f2136a422a770e3ca67858e6af7807645a184f407cbb102ba57de
docker: Error response from daemon: driver failed programming external connectivity on endpoint pg170 (0db5bf733c8874212e89a47facea053fa35b0aaee80eede7aae2ac0314a3a5d8): Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use.
bill@leiyu-pc:~$
```

```
### postpresql运行成功  by docker
```
bill@leiyu-pc:~$ docker rm -f pg170 2>/dev/null
pg170
bill@leiyu-pc:~$ docker run -d --name pg170 \
e POSTGRES_PASSWORD=postgres \
 >   -e POSTGRES_PASSWORD=postgres \
>   -p 5432:5432 \
>   -v $HOME/pg17-data:/var/lib/postgresql/data \
>   postgres:17.0
2a1ca53db6b0a5ebd33052273d1ba86e0f34ea6cd3fc0a316cbebeeeaedc1bbe
bill@leiyu-pc:~$ docker exec -it pg170 psql -U postgres -c "SELECT version();"
                                                       version
---------------------------------------------------------------------------------------------------------------------
 PostgreSQL 17.0 (Debian 17.0-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
(1 row)

bill@leiyu-pc:~$
```

*********************************************************************************************************************************************************
# postpresql 总结
太好了，已经成功跑起 **PostgreSQL 17.0** 容器并能查询版本了 ✅
接下来给你一份“把它用好”的速用清单（含连接、持久化、常用操作、升级与备份）。

---

## 1) 连接方式

* **WSL/Windows 本机连接**：
  Host：`localhost`，Port：`5432`，User：`postgres`，Password：`postgres`（你 `-e POSTGRES_PASSWORD` 设的）。
  工具：`psql`、DBeaver、pgAdmin 等。

* **容器内连接**（已在用）：

  ```bash
  docker exec -it pg170 psql -U postgres
  ```

---

## 2) 数据持久化（你已经做对了）

你挂载了：`-v $HOME/pg17-data:/var/lib/postgresql/data`

* 数据会保存在 **WSL 的 Linux 文件系统**，性能与稳定性好（比 `/mnt/c` 更推荐）。
* 若要换目录，保持目标目录属主为 `999:999`（容器内 postgres 用户）或用 `chown -R`.

---

## 3) 安全与常用初始化

进入 psql 后执行（创建业务用户/库，避免用 `postgres` 超管跑业务）：

```sql
-- 创建应用账号与数据库
CREATE ROLE app WITH LOGIN PASSWORD 'Strong!Passw0rd';
CREATE DATABASE appdb OWNER app;
GRANT ALL PRIVILEGES ON DATABASE appdb TO app;

-- 可选：启用常用扩展（在目标库执行）
\c appdb
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS uuid-ossp;
```

> 提醒：尽快把 `postgres` 用户密码改成强密码。

---

## 4) 常用容器管理

```bash
# 查看日志（启动/错误排查）
docker logs -f pg170

# 进入容器 Shell
docker exec -it pg170 bash

# 重启 / 停止 / 删除
docker restart pg170
docker stop pg170
docker rm -f pg170
```

建议把重启策略加上（下次重建时使用）：

```bash
--restart unless-stopped
```

完整示例：

```bash
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0
```

---

## 5) 备份 / 恢复（从宿主机直接做）

```bash
# 逻辑备份（自带压缩格式）
docker exec pg170 pg_dump -U postgres -Fc appdb > ~/appdb_$(date +%F).dump

# 恢复到空库（确保先 CREATE DATABASE）
docker exec -i pg170 pg_restore -U postgres -d appdb < ~/appdb_2025-08-26.dump

# 全库备份（含角色/库定义）
docker exec pg170 pg_dumpall -U postgres > ~/pg_all_$(date +%F).sql


---

## 6) 配置 & 远程访问

* 主配置：容器里 `/var/lib/postgresql/data/postgresql.conf`
* 访问控制：`/var/lib/postgresql/data/pg_hba.conf`
  如需允许局域网访问，修改 `pg_hba.conf` 增加网段白名单，`postgresql.conf` 里设 `listen_addresses='*'`，然后：

  ```bash
  docker restart pg170
  ```

---

## 7) 小版本升级（17.0 → 17.x）

逻辑：**同一大版本**只需换镜像、复用数据目录即可。

```bash
docker pull postgres:17
docker stop pg170
docker rm pg170
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17
```

容器会检测老的数据目录并进行**同版本线升级**（安全补丁）。

---

## 8) 端口冲突提示

你之前 5432 被本机 pg 进程占用（`127.0.0.1:5432`），现在容器已成功占 5432，说明你已停掉本机 pg。
若将来再冲突，可用 `-p 5433:5432` 临时避让，连接改 `localhost:5433`。

---

需要我把上面的“初始化 SQL + 备份脚本 + 重启策略”整合成一键脚本吗？你告诉我希望的用户名/库名/密码，我直接给你可执行版。

用户名：proot
库名：pdemo
密码：proot




# *********************************************************************************************************************************************************
# postpresql17安装总结

结合上面的过程，详细叙述一下wsl2下，docker操作postpresql17的安装、启动、检测、配置用户名/密码/库、状态检查，已经如何远程访问等。

下面把你刚才在 WSL2 里用 Docker 跑 **PostgreSQL 17.0** 的全过程梳理成一份可执行“作业手册”，涵盖：安装 → 启动 → 自检 → 创建账户/数据库 → 运行状态检查 → 远程访问（含常见故障排查）。

---

## 0) 前置确认

* **WSL2 已可用**（Ubuntu/Debian 等）。
* **Docker 可用**（任选其一）

  * **Docker Desktop + WSL 集成**（最省心），或
  * **WSL 内原生 Docker Engine**（需启用 systemd 并启动 `docker` 服务）。

自检：

```bash
docker version
docker run --rm hello-world
```

---

## 1) 拉起 PostgreSQL 17 容器（持久化 + 端口）

> 推荐把数据放在 WSL 的 Linux 目录（非 `/mnt/c`），性能更好。

```bash
# 创建数据目录（宿主机）
mkdir -p $HOME/pg17-data

# 启动容器（固定 17.0；想跟随 17.x 最新补丁可改为 postgres:17）
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0
```

> 如果 `-p 5432:5432` 报“address already in use”，说明宿主 5432 被占：
>
> * 查占用：`sudo ss -ltnp | grep :5432`
> * 临时改宿主口：`-p 5433:5432`（连接改用 5433），或停止占用者（本地 pg/其他容器）。

---

## 2) 启动后自检（日志、就绪、版本）

```bash
# 看启动日志（应出现 ready to accept connections）
docker logs -f pg170 | sed -n '1,120p'

# 数据库就绪探测
docker exec pg170 pg_isready -U postgres -h 127.0.0.1 -p 5432

# 版本验证
docker exec -it pg170 psql -U postgres -c "SELECT version();"
```

---

## 3) 账号/密码/数据库配置（两种方式）

### 方式 A：**一次性在首次启动时用环境变量初始化**（最简单）

> 仅对**第一次**初始化数据目录有效，已有数据目录不会再次应用。

```bash
docker rm -f pg170
rm -rf $HOME/pg17-data/*   # ⚠️ 清空旧数据（谨慎）

docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_USER=proot \
  -e POSTGRES_PASSWORD=proot \
  -e POSTGRES_DB=pdemo \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0
```

### 方式 B：**事后用 SQL 幂等创建/修改**

> 适合已经跑起来的实例（你刚才就是这样做的）。

```bash
docker exec -i pg170 psql -U postgres <<'SQL'
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='proot') THEN
    CREATE ROLE proot LOGIN PASSWORD 'proot';
  ELSE
    ALTER ROLE proot WITH LOGIN PASSWORD 'proot';
  END IF;
END$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname='pdemo') THEN
    CREATE DATABASE pdemo OWNER proot;
  END IF;
END$$;

GRANT ALL PRIVILEGES ON DATABASE pdemo TO proot;

\c pdemo
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SQL
```

---

## 4) 常用运行状态与管理

```bash
# 查看容器
docker ps
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"

# 查看日志
docker logs -f pg170

# 进容器 shell
docker exec -it pg170 bash

# 重启/停止/删除
docker restart pg170
docker stop pg170
docker rm -f pg170
```

### （可选）为容器加健康检查

```bash
docker rm -f pg170
docker run -d --name pg170 \
  --restart unless-stopped \
  --health-cmd='pg_isready -U postgres -h 127.0.0.1 -p 5432 || exit 1' \
  --health-interval=10s --health-timeout=3s --health-retries=3 \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0

# 查看健康状态
docker inspect --format='{{json .State.Health}}' pg170 | jq
```

---

## 5) 从哪里连？（本机 / Windows / 其他机器）

### A) 本机（WSL/Windows）连接

* 主机（Host）：`localhost`
* 端口（Port）：你映射的端口（上文 5432）
* 用户：`proot`（或 `postgres`）
* 数据库：`pdemo`
* 密码：`proot`（或你设置的）

命令行示例：

```bash
psql "host=localhost port=5432 user=proot dbname=pdemo password=proot"
```

GUI：DBeaver / pgAdmin 直接填上面参数。

> **Docker Desktop** 场景：Windows 直接 `localhost:5432`。
> **WSL 原生 Engine**：Win11 通常也能直连 `localhost`；不行的话，查 WSL 网关 IP：
>
> ```bash
> ip route | awk '/default/ {print $3}'
> # 得到形如 172.19.128.1，然后在 Windows 用 172.19.128.1:5432 连接
> ```

### B) 外部机器访问（谨慎）

1. 确认端口映射到 0.0.0.0（默认 `-p 5432:5432` 就是）。
2. Windows 防火墙放行 5432（Docker Desktop 绑定在 Windows 上）：

   * 允许入站规则，或临时关闭专用网络阻拦。
3. **安全**：仅在内网开放，强密码；必要时限制来源（见下一节 pg\_hba）。

---

## 6) 调整 `postgresql.conf` / `pg_hba.conf`（网络访问控制）

官方镜像的数据目录挂载在容器 `/var/lib/postgresql/data`。进入容器修改：

```bash
docker exec -it pg170 bash

# 主配置
vi /var/lib/postgresql/data/postgresql.conf
# 如需：listen_addresses = '*'

# 访问控制（基于客户端网段）
vi /var/lib/postgresql/data/pg_hba.conf
# 例如允许内网 192.168.0.0/16 使用密码连接：
# host  all  all  192.168.0.0/16  md5

exit
docker restart pg170
```

> 仅本机访问时，默认配置即可；对外开放时，一定要在 `pg_hba.conf` 里**精确白名单**来源网段，切勿对公网裸露。

---

## 7) 备份与恢复（建议日常操作）

```bash
# 备份单库（自带压缩）
docker exec pg170 pg_dump -U postgres -Fc pdemo > ~/pg17-backups/pdemo_$(date +%F_%H%M%S).dump

# 恢复（确保目标库存在或提前 CREATE DATABASE）
docker exec -i pg170 pg_restore -U postgres --clean --if-exists -d pdemo < ~/pg17-backups/pdemo_2025-08-27_120000.dump

# 全库备份（含角色/库定义）
docker exec pg170 pg_dumpall -U postgres > ~/pg17-backups/cluster_$(date +%F_%H%M%S).sql
```

---

## 8) 小版本升级（17.0 → 17.x）

同大版本可平滑切换镜像，复用数据目录：

```bash
docker pull postgres:17
docker stop pg170 && docker rm pg170
docker run -d --name pg170 \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17
```

---

## 9) 常见故障速排

* **端口冲突**：`sudo ss -ltnp | grep :5432` → 改映射为 `-p 5433:5432` 或停掉占用者（例如 `sudo pg_ctlcluster <ver> main stop`）。
* **拉镜像 DNS 失败**：为 Docker 守护进程配置 DNS（`/etc/docker/daemon.json`）：

  ```json
  { "dns": ["1.1.1.1","8.8.8.8"] }
  ```

  重启 Docker 服务。
* **WSL 没 systemd，`systemctl` 不能用**：在 `/etc/wsl.conf` 写：

  ```ini
  [boot]
  systemd=true
  ```

  然后 `wsl --shutdown`。
* **代理网络**：给 Docker 守护进程设置代理（或在 Docker Desktop 的 Proxies 里配置）。
* **性能差**：避免把数据目录挂到 `/mnt/c/...`；优先使用 WSL 原生 Linux 路径。

---

> 你已经把核心流程跑通了：容器名 `pg170`、数据卷 `$HOME/pg17-data`、端口 `5432`、并成功查询版本。上面这份手册可以当作“标准操作流程”。如果你愿意，我可以把常用命令整合成一个菜单脚本（启动/停止/创建用户库/备份恢复/健康检查/升级）。



*********************************************************************************************************************************************************

# postpresql 备份/恢复”脚本
安排！下面给你三份可直接用的一键脚本，按你给的参数**用户名：proot、库名：pdemo、密码：proot** 做初始化，并附带“自动重启策略”“备份/恢复”脚本。放到 **WSL** 里保存、赋权、执行即可。

---

## 1) 初始化 + 一键创建用户/库（幂等）

保存为 `pg17-oneclick.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail

# === 可改参数 ===
CNAME="pg170"              # 你的容器名
HOST_PORT="5432"           # 宿主机端口
DATA_DIR="$HOME/pg17-data" # 数据目录（宿主机）
PG_IMAGE="postgres:17.0"   # 固定 17.0
DB_USER="proot"
DB_PASS="proot"
DB_NAME="pdemo"

# === 准备数据目录 ===
mkdir -p "$DATA_DIR"

# === 如容器不存在则创建；存在则确保重启策略 ===
if ! docker ps -a --format '{{.Names}}' | grep -qx "$CNAME"; then
  docker run -d --name "$CNAME" \
    --restart unless-stopped \
    -e POSTGRES_PASSWORD=postgres \
    -p "${HOST_PORT}:5432" \
    -v "$DATA_DIR:/var/lib/postgresql/data" \
    "$PG_IMAGE"
else
  docker update --restart unless-stopped "$CNAME" >/dev/null
  docker start "$CNAME" >/dev/null 2>&1 || true
fi

# === 等待 PostgreSQL 就绪 ===
echo "Waiting for PostgreSQL in container [$CNAME] ..."
until docker exec "$CNAME" pg_isready -U postgres -h 127.0.0.1 -p 5432 >/dev/null 2>&1; do
  sleep 1
done

# === 初始化：创建/更新角色与库（幂等），并启用常用扩展 ===
docker exec -i "$CNAME" psql -U postgres <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
    CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASS';
  ELSE
    ALTER ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';
  END IF;
END
\$\$;

DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME') THEN
    CREATE DATABASE $DB_NAME OWNER $DB_USER;
  END IF;
END
\$\$;

GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

\\c $DB_NAME
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SQL

echo "✅ 初始化完成：user=$DB_USER db=$DB_NAME （容器：$CNAME，端口：$HOST_PORT）"
echo "连接示例：psql -h localhost -p ${HOST_PORT} -U ${DB_USER} -d ${DB_NAME}"
```

执行：

```bash
chmod +x pg17-oneclick.sh
./pg17-oneclick.sh
```

---

## 2) 备份脚本（库级 + 全库）

保存为 `pg17-backup.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail
CNAME="pg170"
DB_NAME="pdemo"
OUTDIR="$HOME/pg17-backups"
mkdir -p "$OUTDIR"

TS="$(date +%F_%H%M%S)"

# 库级逻辑备份（自带压缩格式）
docker exec "$CNAME" pg_dump -U postgres -Fc "$DB_NAME" > "$OUTDIR/${DB_NAME}_${TS}.dump"

# 全库备份（含角色/库定义）
docker exec "$CNAME" pg_dumpall -U postgres > "$OUTDIR/cluster_${TS}.sql"

echo "✅ 备份完成：
- 库备份: $OUTDIR/${DB_NAME}_${TS}.dump
- 全库备份: $OUTDIR/cluster_${TS}.sql"
```

执行：

```bash
chmod +x pg17-backup.sh
./pg17-backup.sh
```

---

## 3) 恢复脚本（从 `.dump` 恢复到 pdemo）

保存为 `pg17-restore.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "用法: $0 /path/to/pdemo_xxx.dump" >&2
  exit 1
fi

CNAME="pg170"
DB_NAME="pdemo"

DUMP="$1"

# 确保目标库存在（由初始化脚本创建），清理后恢复
docker exec -i "$CNAME" bash -c "psql -U postgres -d postgres -v ON_ERROR_STOP=1 -c \"SELECT 1 FROM pg_database WHERE datname='$DB_NAME'\" >/dev/null || createdb -U postgres '$DB_NAME'"
docker exec -i "$CNAME" pg_restore -U postgres --clean --if-exists -d "$DB_NAME" < "$DUMP"

echo "✅ 恢复完成：$DUMP -> $DB_NAME"
```

执行：

```bash
chmod +x pg17-restore.sh
./pg17-restore.sh ~/pg17-backups/pdemo_2025-08-27_120000.dump
```

---

### 小贴士

* 当前 **超管 `postgres` 的密码是 `postgres`**（在 `docker run` 的环境变量里设定）。如需修改，可：

  ```bash
  docker exec -it pg170 psql -U postgres -c "ALTER USER postgres WITH PASSWORD '更强的密码';"
  ```
* 以后若要升级到 **17.x 更高小版本**：
  `docker pull postgres:17 && docker stop pg170 && docker rm pg170 && ./pg17-oneclick.sh`（脚本会复用原数据目录，完成同版本线升级）。
* 如需从 Windows 连接：主机 `localhost`、端口 `5432`、用户 `proot`、库 `pdemo`、密码 `proot`。

需要我把这三份脚本合并成一个“菜单式”的单脚本吗？（一键：初始化 / 备份 / 恢复 / 升级）




*********************************************************************************************************************************************************

祝贺昨天首启成功！今天“正常启动”Odoo，**不要再用 `-i base`**（那是首次初始化用的，会重复安装基础模块）。按下面顺序来就行：

## 每次启动步骤（最短闭环）

1. **确保数据库容器在跑**

```bash
# 看看是否已在运行
docker ps -a --filter name=pg170
# 未运行就启动
docker start pg170
# 快速连通性自测（可选）
PGPASSWORD=proot psql -h 127.0.0.1 -p 5432 -U proot -d odoo -c "select 1;"
```

> 建议用 `127.0.0.1:5432` 连接你映射出来的端口，**别用** `172.17.x.x`（容器内网 IP 可能变）。

2. **进入项目并激活 venv**

```bash
cd /d/_projects/odoo.github.rainth888
source .venv/bin/activate
```

3. **启动 Odoo（正常运行）**

```bash
python odoo-bin \
  --addons-path=addons,odoo/addons \
  -d odoo \
  --db_host=127.0.0.1 --db_port=5432 \
  --db_user=proot --db_password=proot
```

然后浏览器打开：`http://localhost:8069`

---

## 推荐：用配置文件更省心

在项目根目录新建 `odoo.conf`：

```ini
[options]
addons_path = addons,odoo/addons
db_host = 127.0.0.1
db_port = 5432
db_user = proot
db_password = proot
db_name = odoo
logfile = /tmp/odoo.log
; http_port = 8069
```

以后只需：

```bash
python odoo-bin -c odoo.conf
```

---

## 常见操作小抄

* **更新某个模块**（而非全新安装 base）：

  ```bash
  python odoo-bin -c odoo.conf -u <module_name>
  ```
* **查看 Odoo 是否读到了两个 addons 路径**：启动日志里会打印 `addons_path=...`
* **容器 IP 变导致连不上**：把 `db_host` 固定为 `127.0.0.1`（你已做了端口映射 `-p 5432:5432`），或把 Odoo 也放进 Docker 与 Postgres 同一自定义网络后用服务名直连。

需要的话，我可以把你当前参数写成一个“一键启动脚本”，双击/执行就能起 Odoo。




*********************************************************************************************************************************************************

在 Ubuntu 环境下，有几种方法可以在后台运行 Odoo 服务。我来为你介绍几种推荐的方法：

**方法1：使用 nohup（简单快速）**
```bash
# 在后台运行并将输出重定向到日志文件
nohup python odoo-bin -c odoo.conf > odoo.log 2>&1 &

# 查看进程
ps aux | grep odoo

# 查看日志
tail -f odoo.log
```

**方法2：使用 screen（推荐，可以重新连接）**
```bash
# 安装 screen（如果没有安装）
sudo apt install screen

# 创建新的 screen 会话
screen -S odoo

# 在 screen 中运行 Odoo
python odoo-bin -c odoo.conf

# 按 Ctrl+A 然后按 D 来分离会话

# 重新连接到会话
screen -r odoo

# 查看所有会话
screen -ls
```

**方法3：使用 tmux（更现代的终端复用器）**
```bash
# 安装 tmux
sudo apt install tmux

# 创建新的 tmux 会话
tmux new-session -d -s odoo

# 在 tmux 中运行 Odoo
tmux send-keys -t odoo "python odoo-bin -c odoo.conf" Enter

# 分离会话
tmux detach -s odoo

# 重新连接
tmux attach -t odoo

# 查看会话
tmux list-sessions
```

**方法4：创建系统服务（最专业，推荐生产环境）**
```bash
# 创建服务文件
sudo nano /etc/systemd/system/odoo.service
```

在文件中添加以下内容：
```ini
[Unit]
Description=Odoo
After=network.target

[Service]
Type=simple
User=bill
Group=bill
WorkingDirectory=/mnt/d/_projects/odoo.github.rainth888
ExecStart=/mnt/d/_projects/odoo.github.rainth888/.venv/bin/python /mnt/d/_projects/odoo.github.rainth888/odoo-bin -c /mnt/d/_projects/odoo.github.rainth888/odoo.conf
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

然后启用和启动服务：
```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable odoo

# 启动服务
sudo systemctl start odoo

# 查看状态
sudo systemctl status odoo

# 查看日志
sudo journalctl -u odoo -f

# 停止服务
sudo systemctl stop odoo
```

**方法5：使用 supervisor（进程管理工具）**
```bash
# 安装 supervisor
sudo apt install supervisor

# 创建配置文件
sudo nano /etc/supervisor/conf.d/odoo.conf
```

配置文件内容：
```ini
[program:odoo]
command=/mnt/d/_projects/odoo.github.rainth888/.venv/bin/python /mnt/d/_projects/odoo.github.rainth888/odoo-bin -c /mnt/d/_projects/odoo.github.rainth888/odoo.conf
directory=/mnt/d/_projects/odoo.github.rainth888
user=bill
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/odoo/odoo.log
```

然后：
```bash
# 创建日志目录
sudo mkdir -p /var/log/odoo
sudo chown bill:bill /var/log/odoo

# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start odoo

# 查看状态
sudo supervisorctl status odoo
```

**推荐使用顺序：**
1. **开发测试：** 使用 `nohup` 或 `screen`
2. **个人使用：** 使用 `tmux`
3. **生产环境：** 使用 `systemd` 服务

对于你当前的情况，我推荐使用 **方法1（nohup）** 或 **方法2（screen）**，它们简单易用且不需要额外配置。

你想使用哪种方法？我可以提供更详细的步骤说明。



*********************************************************************************************************************************************************
# ubuntu20:
**方法4：创建系统服务（最专业，推荐生产环境）**
```bash
# 创建服务文件
sudo nano /etc/systemd/system/odoo.service
```

在文件中添加以下内容：
```ini
[Unit]
Description=Odoo
After=network.target

[Service]
Type=simple
User=bill
Group=bill
WorkingDirectory=/data/odoo.github.rainth888
ExecStart=/data/odoo.github.rainth888/.venv/bin/python /data/odoo.github.rainth888/odoo-bin -c /data/odoo.github.rainth888/odoo.conf
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

然后启用和启动服务：
```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable odoo

# 启动服务
sudo systemctl start odoo

# 查看状态
sudo systemctl status odoo

# 查看日志
sudo journalctl -u odoo -f

# 停止服务
sudo systemctl stop odoo
```



*********************************************************************************************************************************************************
从错误信息来看，主要有两个问题需要解决：

### 1. **Odoo 使用 root 用户运行的问题**

> `Running as user 'root' is a security risk.`

这是一个警告，建议你不要以 `root` 用户启动 Odoo，因为这会存在安全隐患。你应该用一个非 `root` 用户来运行 Odoo，通常是 `odoo` 或 `bill` 用户。

#### 解决方案：

1. 创建一个新的用户（如果还没有的话）：

   ```bash
   sudo useradd -m odoo
   sudo usermod -aG sudo odoo
   ```
2. 修改文件夹权限，确保 Odoo 进程可以访问相关目录：

   ```bash
   sudo chown -R odoo:odoo /data/odoo.github.rainth888
   ```
3. 切换到 `odoo` 用户：

   ```bash
   sudo su - odoo
   ```
4. 以 `odoo` 用户运行 Odoo：

   ```bash
   python odoo-bin --addons-path=addons,odoo/addons -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot
   ```

### 2. **端口冲突：OSError: \[Errno 98] Address already in use**

> `OSError: [Errno 98] Address already in use`

这个错误表明 Odoo 启动时，绑定的端口（默认是 8069）已经被其他进程占用了。你可以使用以下命令来检查端口是否被占用，并杀掉相关进程。

#### 解决方案：

1. **检查 8069 端口占用**：

   ```bash
   sudo lsof -i :8069
   ```

   或者：

   ```bash
   sudo netstat -tuln | grep 8069
   ```

2. **杀掉占用该端口的进程**：
   如果找到了占用该端口的进程，记下 PID，并执行以下命令来终止它：

   ```bash
   sudo kill -9 <PID>
   ```

3. **更改 Odoo 使用的端口（如果需要）**：
   如果你希望避免端口冲突，可以更改 Odoo 使用的端口（如 8070）：

   ```bash
   python odoo-bin --addons-path=addons,odoo/addons -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot --http-port=8070
   ```

4. **确认没有其他进程占用该端口**：
   再次执行 `sudo lsof -i :8069` 或 `sudo netstat -tuln | grep 8069`，确保端口没有被占用。

---

### 总结

* **运行 Odoo 时避免使用 `root` 用户**，可以创建一个新的用户并使用它来运行。
* **解决端口占用问题**，通过查看占用端口的进程并终止，或者更改 Odoo 的运行端口。




*********************************************************************************************************************************************************
### 修改 Odoo 和 PostgreSQL 默认用户密码的步骤

#### 1. 修改 Odoo 的管理员密码

Odoo 的管理员密码（`admin_passwd`）存储在配置文件 `odoo.conf` 中，你可以直接在配置文件中修改这个密码，或者通过数据库进行更改。

##### 1.1 修改 `odoo.conf` 中的 `admin_passwd`（直接修改配置文件）

1. 找到并编辑你的 Odoo 配置文件（`odoo.conf`）。通常，它位于 Odoo 项目的根目录，或者 Docker 容器中挂载的目录。

   使用 `nano` 或 `vim` 编辑配置文件：

   ```bash
   nano /path/to/your/odoo.conf
   ```

2. 找到 `admin_passwd` 字段，修改为你想要的密码：

   ```ini
   admin_passwd = new_password_here
   ```

3. 保存文件并退出编辑器。

##### 1.2 使用 SQL 更改 Odoo 的管理员密码

1. 通过 Docker 容器进入 PostgreSQL 数据库：

   ```bash
   docker exec -it pg170 psql -U proot -d odoo
   ```

2. 执行以下 SQL 查询来更新管理员密码。替换 `new_password_here` 为你想设置的密码：

   ```sql
   UPDATE res_users SET password = 'new_password_here' WHERE login = 'admin';
   
   UPDATE res_users SET password = 'Qd#969kyghb!k&chFdv5axsuH+wq7' WHERE login = 'admin';
   ```

3. 退出 PostgreSQL：

   ```sql
   \q
   ```

#### 2. 修改 PostgreSQL 用户（`proot`）的密码

1. 进入 PostgreSQL 容器并使用管理员权限登录：

   ```bash
   docker exec -it pg170 psql -U proot
   ```

2. 修改 `proot` 用户的密码（替换 `new_password_here` 为你想要的密码）：

   ```sql
   ALTER USER proot WITH PASSWORD 'new_password_here';
   
   ALTER USER proot WITH PASSWORD 'Qd#969kyghb!k&chFdv5axsuH+wq7';
   ```

3. 确保数据库配置文件中的新密码与所设置的密码一致。更新 Odoo 配置文件 `odoo.conf` 中的 `db_password`：

   ```ini
   db_password = new_password_here
   ```

4. 退出 PostgreSQL：

   ```sql
   \q
   ```

#### 3. 确保数据库和 Odoo 配置文件同步

确保在 `odoo.conf` 配置文件中，`db_password` 字段和 PostgreSQL 中的 `proot` 用户密码一致：

```ini
db_host = 127.0.0.1
db_port = 5432
db_user = proot
db_password = new_password_here  # 修改为新密码
```

#### 4. 重启 Odoo 服务

修改完密码后，需要重启 Odoo 服务，使配置生效。

如果你在 Docker 中运行 Odoo：

```bash
docker restart pg170   # 重启 PostgreSQL 容器（如果有更改数据库设置）
docker restart odoo_app # 重启 Odoo 容器
```

或者，如果你直接在服务器上运行 Odoo：

```bash
sudo systemctl restart odoo
```

#### 5. 检查 Odoo 是否正常连接 PostgreSQL

访问 Odoo UI，尝试登录并检查是否能够使用新的密码访问系统。你可以访问 Odoo 的 `http://localhost:8069` 或对应的公网地址，确保数据库连接和管理员密码都正确。

---

### 总结：

* **修改 Odoo 管理员密码**：直接修改 `odoo.conf` 或使用 SQL 更新数据库中的管理员密码。
* **修改 PostgreSQL 用户密码**：通过 SQL 命令修改 `proot` 用户密码，并确保 `odoo.conf` 中同步更新。
* **重启 Odoo 和 PostgreSQL** 服务，确保更改生效。



*********************************************************************************************************************************************************
# unbuntu20下的odoo系统，设置为systemctl自动启动，数据库是docker自动启动，现在发现odoo服务启动时，数据库系统还没有启动起来，
你说的是“开机自启时 Odoo 抢先启动，而 Docker 里的 Postgres 还没 ready，导致 Odoo 启动失败”。用 **systemd 的 ExecStartPre 等待 DB 就绪** 是最稳的做法。给你三套可选方案，首推方案 A。

---

## 方案 A：在 odoo.service 里用 `pg_isready` 等待端口就绪（推荐）

1. 在宿主机装客户端检测工具：

```bash
sudo apt-get update
sudo apt-get install -y postgresql-client
```

2. 修改 `/etc/systemd/system/odoo.service`（关键是 `After/Wants` + `ExecStartPre`）：

```ini
[Unit]
Description=Odoo
After=network-online.target docker.service
Wants=network-online.target docker.service

[Service]
Type=simple
User=bill
Group=bill
WorkingDirectory=/data/odoo.github.rainth888

# 按你实际路径写
ExecStart=/data/odoo.github.rainth888/.venv/bin/python /data/odoo.github.rainth888/odoo-bin -c /data/odoo.github.rainth888/odoo.conf

# —— 等待数据库就绪（最多 60 秒）——
Environment="DB_HOST=127.0.0.1" "DB_PORT=5432"
ExecStartPre=/bin/sh -c 'for i in $(seq 1 60); do \
  /usr/bin/pg_isready -h ${DB_HOST} -p ${DB_PORT} >/dev/null 2>&1 && exit 0; \
  echo "[wait-db] postgres not ready, retry $i/60"; sleep 1; done; exit 1'

# 可选：顺手把容器启动起来（若用 docker 重启策略也可省略）
ExecStartPre=/usr/bin/docker start pg170 >/dev/null 2>&1 || true

Restart=always
RestartSec=5
TimeoutStartSec=70   # 给等待脚本一些时间

[Install]
WantedBy=multi-user.target
```

3. 使配置生效并测试：

```bash
sudo systemctl daemon-reload
sudo systemctl restart odoo
sudo systemctl status odoo -n 50
```

> 说明
>
> * `After=… docker.service` 只保证 **Docker 守护进程**已起，不代表容器就绪；真正的“ready”靠 `ExecStartPre` 的 `pg_isready` 来兜底。
> * `DB_HOST=127.0.0.1` 前提是你把容器 5432 映射到宿主 5432（`-p 5432:5432`）。如果你用了别的端口，改成对应端口。
> * `pg_isready` 只测“是否接受连接”，**无需用户/密码**，非常适合做 readiness。

---

## 方案 B：不想装 `pg_isready`？用 `nc`/`bash` 端口探测

把 `ExecStartPre` 换成下面任一条（先装 `netcat`）：

```bash
sudo apt-get install -y netcat
```

**版本 1（nc）：**

```ini
ExecStartPre=/bin/sh -c 'for i in $(seq 1 60); do \
  nc -z 127.0.0.1 5432 && exit 0; \
  echo "[wait-db] port closed, retry $i/60"; sleep 1; done; exit 1'
```

**版本 2（/dev/tcp）：**

```ini
ExecStartPre=/bin/sh -c 'for i in $(seq 1 60); do \
  (echo > /dev/tcp/127.0.0.1/5432) >/dev/null 2>&1 && exit 0; \
  echo "[wait-db] port closed, retry $i/60"; sleep 1; done; exit 1'
```

---

## 方案 C：把 DB 与 Odoo 都用 docker-compose 管（健康检查 + 依赖）

如果你愿意把 Odoo 也容器化，`docker compose` 的 **healthcheck + depends\_on: condition: service\_healthy** 能天然保证启动顺序。例如：

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: proot
      POSTGRES_PASSWORD: proot
      POSTGRES_DB: odoo
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U proot -d odoo"]
      interval: 5s
      timeout: 3s
      retries: 30
    ports:
      - "5432:5432"
    volumes:
      - ./pgdata:/var/lib/postgresql/data

  odoo:
    image: odoo:18
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8069:8069"
    volumes:
      - ./odoo.conf:/etc/odoo/odoo.conf
      - ./addons:/mnt/extra-addons
```

开机自启可用一个 systemd 单元去执行 `docker compose up -d`，就不需要自己写 `ExecStartPre` 轮询了。

---

## 其他加固建议

* **Odoo 连接 DB 时用 127.0.0.1/固定端口**（避免使用 `172.17.x.x` 这类 Docker 内网 IP，会变化）。
* **Postgres 容器加重启策略**：`--restart unless-stopped`（或 compose 里 `restart: unless-stopped`）。
* **Odoo 服务 `Restart=always`**：即使 DB 短时重启，Odoo 也能自动拉起。
* **权限/用户**：避免用 `root` 跑 Odoo，`User=bill` 并确保目录归属 `bill:bill`。
* **日志定位**：`journalctl -u odoo -b -n 100 -f` 看 Odoo；`docker logs -f pg170` 看 DB 容器。

---

按方案 A 改完，你再重启机器（或模拟 DB 慢起）测试一遍：

1. `sudo systemctl stop odoo`
2. `docker stop pg170 && sleep 3 && docker start pg170`
3. `sudo systemctl start odoo`
   看 `status`/日志里会打印 “\[wait-db] … retry …”，直到 “accepting connections” 再正式启动 Odoo。



# *********************************************************************************************************************************************************

一次性指令（同时留下“监控脚本”，第二天可复查）

1. 停掉旧进程  
```bash
pkill -f odoo-bin
```

2. 立即建一个「监控脚本」记录数据库列表  
```bash
cat > /data/odoo-watch.sh <<'EOF'
#!/bin/bash
ts=$(date '+%F %T')
echo "[$ts] Database list:" >> /data/pg-watch.log
docker exec -it pg170 psql -U proot -c '\l' >> /data/pg-watch.log
EOF
chmod +x /data/odoo-watch.sh
```
```bash
cat > odoo-watch.sh <<'EOF'
#!/bin/bash
PG_PASS='Qd#969kyghb!k&chFdv5axsuH+wq7'
ts=$(date '+%F %T')
echo "[$ts] Database list:" >> pg-watch.log
docker exec -e PGPASSWORD="$PG_PASS" pg170 \
  psql -h 127.0.0.1 -U proot -d odoo -c '\l' >> pg-watch.log 2>&1
EOF
chmod +x odoo-watch.sh
```

3. **初始化**（带 `--stop-after-init` 让它跑完自动停，方便你检查）  
```bash
cd /data/odoo.github.rainth888
python odoo-bin \
  --addons-path=addons \
  -d odoo \
  --db_host=127.0.0.1 \
  --db_port=5432 \
  --db_user=proot \
  --db_password='Q*************H+wq7' \
  -i base \
  --stop-after-init
```

4. 初始化完成 **立即** 看库  
```bash
/data/odoo-watch.sh        # 第一次记录
docker exec -it pg170 psql -U proot -c '\l'
```

5. 正常启动（以后用）  
```bash
python odoo-bin \
  --addons-path=addons \
  -d odoo \
  --db_host=127.0.0.1 --db_port=5432 \
  --db_user=proot --db_password='Q*************H+wq7'
```

6. 隔夜检查  
```bash
/data/odoo-watch.sh        # 第二次记录
diff /data/pg-watch.log    # 对比两天库列表
```

只要 `/data/pg17-data` 目录不被删除或重新 `docker run` 了同名容器，库就不会消失；日志对比即可一眼看出问题。

# *********************************************************************************************************************************************************

好的，你的想法是对的：如果已经没有历史数据可恢复，那就直接用 Odoo 重新初始化一个数据库。但这一次一定要保证数据库不会再“神秘消失”。我给你分三步来操作：

---

## 一、重新初始化 Odoo 数据库

进入 Odoo 代码目录后执行（假设容器里 PostgreSQL 正常运行，用户 `proot` 存在）：

```bash
python3 odoo-bin \
  --addons-path=addons \
  -d odoo \
  --db_host=127.0.0.1 \
  --db_port=5432 \
  --db_user=proot \
  --db_password='你的密码' \
  -i base
```

* `-d odoo` 表示数据库名叫 `odoo`，如果不存在会创建。
* `-i base` 会安装最基础的 Odoo 模块。
* 成功后，你用浏览器访问 Odoo 就能进入初始化好的系统。

---

## 二、防止再次丢库的关键措施

你的环境里最危险的点是：**Postgres 5432 端口对公网开放**。如果不收口，即使这次重新初始化成功，也可能再次被 DROP。解决办法：

1. **收口端口**

   * 最好改为仅监听本地：

     ```yaml
     # docker-compose.yml 示例
     ports:
       - "127.0.0.1:5432:5432"
     ```
   * 或者用防火墙限制，只允许内网/跳板机：

     ```bash
     sudo ufw allow from <内网IP段> to any port 5432 proto tcp
     sudo ufw deny 5432/tcp
     ```

2. **限制用户权限**

   * 不要用超级用户（`proot` 带 SUPERUSER 权限风险大）。
   * 创建一个专门给 Odoo 用的数据库用户，只赋予该数据库的权限：

     ```sql
     CREATE USER odoo_user WITH PASSWORD '安全密码';
     CREATE DATABASE odoo OWNER odoo_user;
     GRANT ALL PRIVILEGES ON DATABASE odoo TO odoo_user;
     ```
   * 然后 Odoo 连接用 `odoo_user` 而不是 `proot`。

3. **配置 PostgreSQL 访问规则**（容器内 `/var/lib/postgresql/data/pg_hba.conf`）
   只允许本地/指定 IP 连接，并且用安全认证：

   ```conf
   host    odoo    odoo_user    127.0.0.1/32     scram-sha-256
   host    all     all          0.0.0.0/0        reject
   ```

4. **启用日志与审计**
   在 `postgresql.conf` 打开：

   ```conf
   logging_collector = on
   log_statement = 'ddl'
   ```

   这样以后谁执行了 `DROP`/`CREATE` 都能追踪。

5. **备份机制**
   加个每日备份脚本，至少保证就算被删库也能恢复：

   ```bash
   pg_dump -h 127.0.0.1 -U odoo_user -d odoo -F c -f /data/pg-backup/odoo_$(date +%F).dump
   ```

---

## 三、观察验证是否还会“消失”

1. 先执行初始化，把 Odoo 用起来。
2. 观察 `/data/pg17-data` 的体量（用 `du -sh`），随着 Odoo 创建表会变大。
3. 第二天如果发现“库没了”，就立刻查 **容器日志** 和 **Postgres 日志**，判断是 DROP 还是 initdb。
4. 如果以上防护措施到位，基本不可能再出现无故消失的情况。

---

👉 建议：你这次初始化时，用一个\*\*新建的业务用户（非 superuser）\*\*来给 Odoo 连接，这样即使外部有人扫到密码，也没法 DROP 掉整个库。

要不要我帮你写一个 **完整的 docker-compose.yml 示例**（包含 Postgres + Odoo，带内网网络、用户权限配置、持久化挂载、端口收口），你可以直接替换使用？



# *********************************************************************************************************************************************************

# 安装wkhtmltopdf

这是 Odoo 在找不到 **wkhtmltopdf / wkhtmltoimage** 可执行文件时报的标准提示。要生成 PDF/图片报表，你需要在**运行 Odoo 的这台机器**上安装 wkhtmltopdf（与数据库是否在 Docker 无关）。

下面给你一套在 **Ubuntu 20.04（Focal）** 上的靠谱做法，并附上常见坑位检查。

---

## 一步到位安装（Ubuntu 20.04）

### 方式 A：安装官方静态包（包含 wkhtmltopdf + wkhtmltoimage，带 patched Qt，最稳）

> 静态包无需 X 服务器，适合服务器/WSL/容器内使用。

```bash
# 先清掉可能的旧 apt 版本（可选）
sudo apt-get remove -y wkhtmltopdf || true

sudo apt-get update
# 一些字体/渲染依赖（有些包可能已内置，但装上更保险）
sudo apt-get install -y fontconfig libxrender1 libxext6 xfonts-base xfonts-75dpi

# 到 wkhtmltopdf Releases 下载 Ubuntu 20.04 对应的 .deb（名称通常含 “focal_amd64.deb”）
# 例：wkhtmltox_0.12.6-1.focal_amd64.deb
# 假设已下载到 /tmp/wk.deb
sudo apt-get install -y /tmp/wk.deb
# 或者：sudo dpkg -i /tmp/wk.deb && sudo apt-get -f install -y
```

> 注：我不能直接给你外链，去官方 GitHub Releases 选 **focal\_amd64** 的 `.deb` 即可（0.12.5 或 0.12.6 均可；Odoo 16/17/18 通常 0.12.6 更合适）。

### 方式 B：用 apt 直接装（更省事，但个别功能/字体兼容不如静态包）

```bash
sudo apt-get update
sudo apt-get install -y wkhtmltopdf
```

---

## 验证安装是否成功

```bash
wkhtmltopdf --version
wkhtmltoimage --version
which wkhtmltopdf    # 看路径，一般是 /usr/local/bin 或 /usr/bin
```

安装结果：
```
root@yisu-ubuntu20:~# wkhtmltopdf --version
wkhtmltopdf 0.12.5
root@yisu-ubuntu20:~# wkhtmltoimage --version
wkhtmltoimage 0.12.5
root@yisu-ubuntu20:~# which wkhtmltopdf
/usr/bin/wkhtmltopdf
root@yisu-ubuntu20:~#

```

如果命令可用，重启 Odoo 即可；日志里关于 wkhtmltopdf 的提示会消失。

---

## 告诉 Odoo 可执行文件的路径（可选）

通常 Odoo 会从 `PATH` 里自动找到；若仍提示缺失，可在 **odoo.conf** 里加一行指向实际路径：

```ini
[options]
wkhtmltopdf = /usr/local/bin/wkhtmltopdf   ; 或 /usr/bin/wkhtmltopdf
```

改完重启 Odoo：

```bash
sudo systemctl restart odoo   # 如果你用 systemd 管理
# 或者手工重启你现在的进程
```

---

## 报表打不开 / 空白 的常见原因与修复

1. **服务内回环访问失败**（wkhtmltopdf 渲染时需要回连 Odoo 拉静态资源）

   * 在 Odoo 系统参数里设置：

     * `web.base.url`：对外访问的完整 URL（例如 `http://103.100.211.232:8069`，若有反代/HTTPS则写 `https://your.domain`）。
     * `report.url`：wkhtmltopdf 渲染时**用于回连**的内部地址（如果 Odoo 在同机，常设为 `http://127.0.0.1:8069`）。
   * 位置：设置 → 技术 → 参数 → 系统参数。

2. **中文/特殊字体缺失** → PDF 乱码/方块
   安装常用中文字体：

   ```bash
   sudo apt-get install -y fonts-noto-cjk fonts-noto fonts-dejavu ttf-wqy-zenhei
   ```

   安装后重启 Odoo，再试导出。

3. **防火墙/SELinux/容器网络**

   * 确保 Odoo 进程所在环境能访问到 `report.url`。
   * 如果 Odoo 在容器里，`report.url` 推荐指向容器可达的地址（如 `http://odoo:8069` 或宿主 127.0.0.1:映射端口，按你的网络拓扑设）。

4. **运行在 WSL**

   * 也要在 **WSL Linux 环境内** 安装 wkhtmltopdf（不是在 Windows）。
   * 路径、可执行权限、字体同上。

---

## 最后小抄

* 安装成功却仍报缺失 → 指定 `wkhtmltopdf` 路径到 `odoo.conf`。
* 报表空白/资源 404 → 设好 `report.url` 和 `web.base.url`，并保证回环可达。
* 中文不显示 → 安装 `fonts-noto-cjk` / `wqy`。
* Docker 化部署 → 把 wkhtmltopdf 安装写进 Dockerfile（`wkhtmltox` 静态包最佳），或单独提供一个包含它的镜像层。

如果你把当前 **`wkhtmltopdf --version` 输出**、**`which wkhtmltopdf` 路径**、以及你的 **`odoo.conf`** 贴出来，我可以帮你检查是否已经就绪，并给出针对你环境的一条龙修正。

这是 Odoo 在 **WSL2** 里最常见的“**看得见可执行文件，却报找不到**”的坑：  
Odoo 跑在 **Windows 浏览器** 里，但 wkhtmltopdf 装在 **Linux 子系统**，两边不在同一“世界”。  
解决思路：**让 Odoo 调用的其实是 Windows 版的 wkhtmltopdf**。

------------------------------------------------
一步到位的做法（推荐）

1. 在 **Windows 11** 里再装一份  
   下载 64-bit EXE（https://wkhtmltopdf.org/downloads.html）。  
   安装到默认路径 `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`。

2. 启动 Odoo 时把路径指给系统  
   打开 **PowerShell / CMD**（**不要**在 WSL 终端里）：

   ```powershell
   setx WKHTMLTOPDF_CMD "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
   setx WKHTMLTOPDF_ARGS "--enable-local-file-access"
   ```

   然后 **重启 Odoo 服务**（或关掉再开）。

3. 验证  
   进 Odoo →「设置 → 技术 → 参数 → 系统参数」  
   如果看到 `wkhtmltopdf_path` 已经指向 Windows 路径，刷新即可；  
   若没有，手动加一条：  
   ```
   key  : wkhtmltopdf_path
   value: C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
   ```

4. 再次打印报表  
   Odoo 会调用 Windows 版 wkhtmltopdf，问题消失。

------------------------------------------------
备用方案（只在 WSL 里跑 Odoo 时才用）

若你坚持让 Odoo 跑在 WSL 里，需要：

- 给 wkhtmltopdf 装 **缺失的 Qt 依赖**  
  ```bash
  sudo apt update
  sudo apt install -y libxrender1 libfontconfig1 libxext6 libjpeg-turbo8
  ```
- 在 Odoo 配置里把路径写成绝对 Linux 路径  
  ```
  wkhtmltopdf_path = /usr/bin/wkhtmltopdf
  wkhtmltopdf_args = --enable-local-file-access
  ```
- 然后重启 Odoo。  
  但 Windows 浏览器仍可能因 **路径转换/字体** 导致乱码，所以 **方案一更稳**。

------------------------------------------------
一句话总结  
WSL2 里装的 wkhtmltopdf **只能给 WSL 里的进程用**。  
Odoo 在 Windows 端运行 → 给它一份 **Windows 版 wkhtmltopdf** 并指对路径即可。

*********************************************************************************************************************************************************

你已经在 WSL2 里装好了 `wkhtmltopdf`，但 Odoo 仍提示“找不到”。这通常不是“没安装”，而是**Odoo 进程运行的环境找不到可执行文件**（PATH、运行用户、服务方式不同），或者**Odoo 配置没指到具体路径**。按下面顺序排查，基本必解：

---

## 1) 确认“谁”在跑 Odoo，以及它能否看到 wkhtmltopdf

### 如果你是手工前台跑（同一个 shell/venv）

在**同一个终端**里确认：

```bash
which wkhtmltopdf
wkhtmltopdf --version
# 你贴的结果是 /usr/bin/wkhtmltopdf 与 0.12.5，OK
```

### 如果你用 systemd 自启（`systemctl start odoo`）

systemd 的环境和你当前 shell 不一定一样。显式测一把 **服务用户**能否找到命令（假设 User=bill）：

```bash
sudo -u bill -H bash -lc 'echo $PATH; which wkhtmltopdf; wkhtmltopdf --version'
```

* 如果这里找不到/报错，说明 Odoo 进程确实“看不到”它 → 走第 2 步。

---

## 2) 最稳的方式：在 `odoo.conf` 指定绝对路径

直接把路径写死，绕过 PATH 差异：

`/data/odoo.github.rainth888/odoo.conf`

```ini
[options]
wkhtmltopdf  = /usr/bin/wkhtmltopdf
wkhtmltoimage = /usr/bin/wkhtmltoimage
; （顺手建议）
report.url = http://127.0.0.1:8069
web.base.url = http://<你的访问域名或IP>:8069
```

改完**重启 Odoo**：

```bash
# 前台跑就 Ctrl+C 再重启
# systemd 跑：
sudo systemctl daemon-reload
sudo systemctl restart odoo
```

> `report.url` 让 wkhtmltopdf 渲染时回连 Odoo 走 127.0.0.1，更稳定。

---

## 3) 若还是提示：给 systemd 显式设置 PATH（仅自启服务时需要）

编辑 `/etc/systemd/system/odoo.service`，在 `[Service]` 段补一行：

```ini
[Service]
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

然后：

```bash
sudo systemctl daemon-reload
sudo systemctl restart odoo
```

---

## 4) 在当前用户能用，但服务里仍失败？做一次“直接渲染”自测

用**同一个用户**直接跑 wkhtmltopdf，把登录页转成 PDF，看是否可用/是否需要 X：

```bash
wkhtmltopdf http://127.0.0.1:8069/web/login /tmp/odoo_login.pdf
```

* 能生成，说明渲染可行；
* 如果报 `QXcbConnection` 等 X 相关错误，说明你装的是 apt 里的“需要 X”的构建，建议换 **官方静态包（patched Qt）**：

  * 下载 `wkhtmltox_0.12.6-1.focal_amd64.deb`（或 0.12.5 的 focal 版）并安装：

    ```bash
    sudo apt remove -y wkhtmltopdf || true
    sudo apt update && sudo apt install -y fontconfig xfonts-base xfonts-75dpi libxrender1 libxext6
    sudo apt install -y /path/to/wkhtmltox_0.12.6-1.focal_amd64.deb
    which wkhtmltopdf; wkhtmltopdf --version
    ```
  * 然后回到第 2 步在 `odoo.conf` 指路。

---

## 5) Odoo 里还有两处容易忽略的设置

* **系统参数**（设置 → 技术 → 参数 → 系统参数）：

  * `report.url` 设为 `http://127.0.0.1:8069`
  * `web.base.url` 设为你的外网或内网可访问地址
* **字体**（中文/特殊字符乱码）：

  ```bash
  sudo apt install -y fonts-noto-cjk fonts-dejavu ttf-wqy-zenhei
  ```

---

## 6) 特殊拓扑提醒

* **如果 Odoo 在 Docker 里运行**：必须把 wkhtmltopdf 装进 **Odoo 容器**（宿主机安装不生效），或自建镜像在 Dockerfile 里安装 `wkhtmltox`，并在容器内指定路径。
* **WSL2 场景**：你现在是在 WSL 内跑 Odoo → 就在 WSL 内安装 wkhtmltopdf（你已做），并按上面方法在 `odoo.conf` 指定绝对路径即可。

---

### 速查清单（最常见两步就好用）

1. `odoo.conf` 明确：

```ini
wkhtmltopdf  = /usr/bin/wkhtmltopdf
wkhtmltoimage = /usr/bin/wkhtmltoimage
report.url = http://127.0.0.1:8069
```

2. 重启 Odoo（或 systemd 并设置 PATH）。

做完这两步，标签/报表打印的“找不到 wkhtmltopdf”提示就会消失。若还有报错，把 **`sudo -u <运行用户> which wkhtmltopdf` 的输出**和你的 **`odoo.conf`** 发我，我帮你对位看看是哪一步没有生效。


# *********************************************************************************************************************************************************

# 把“订单”打印成 票据打印机专用格式

在 **Odoo 18** 里，如果你要把“订单”打印成 **票据打印机专用格式**，流程大致分 3 部分：

---

## 一、理解 Odoo 打印机制

* Odoo 的打印（比如“报价单”、“订单”、“发票”）是基于 **QWeb 报表模板**生成的 PDF。
* 这些模板是用 **XML + QWeb 指令**写的，可以控制内容、字段、排版。
* 默认的报表格式适合 A4 打印，不适合票据打印机，所以你需要 **自定义报表模板**。

---

## 二、操作步骤

### 1. 开启开发者模式

* 进入 **设置 → 激活开发者模式**。
* 这样可以在“技术”菜单里编辑报表。

### 2. 找到订单的报表

1. 进入 **设置 → 技术 → 报表 → 报表**。
2. 搜索 `sale.order`，你会看到类似 **Quotation / Order** 的报表定义。

   * 模型：`sale.order`
   * 报表类型：`qweb-pdf`
   * 模板：指向一个 QWeb 模板（比如 `sale.report_saleorder_document`）。

### 3. 复制并自定义模板

1. 进入 **设置 → 技术 → 用户界面 → 视图**。
2. 搜索 `report_saleorder_document`（就是订单打印用的 QWeb 模板）。
3. 复制一份（继承方式更好，避免覆盖官方模板）。

   * 新模板里你可以用 QWeb 标签和 HTML/CSS 调整格式：

     * 去掉多余表格线条
     * 控制字体大小
     * 设置票据宽度（比如 80mm 或 58mm）

例如：

```xml
<t t-name="custom.report_saleorder_ticket">
  <t t-call="web.external_layout">
    <div class="page" style="width:80mm; font-size:12px;">
      <h3 style="text-align:center;">订单</h3>
      <p>客户：<span t-field="o.partner_id.name"/></p>
      <p>订单号：<span t-field="o.name"/></p>
      <table style="width:100%;">
        <tr>
          <th>商品</th><th>数量</th><th>价格</th>
        </tr>
        <tr t-foreach="o.order_line" t-as="line">
          <td><span t-field="line.product_id.name"/></td>
          <td><span t-field="line.product_uom_qty"/></td>
          <td><span t-field="line.price_total"/></td>
        </tr>
      </table>
      <p style="text-align:right;">合计：<span t-field="o.amount_total"/></p>
    </div>
  </t>
</t>
```

### 4. 注册报表动作

* 在 **设置 → 技术 → 报表**，新建一个报表，绑定：

  * 模型：`sale.order`
  * 报表类型：`qweb-pdf`
  * 模板：选择你刚才新建的 `custom.report_saleorder_ticket`

这样，订单上就会出现一个新的打印按钮（比如“打印票据”）。

---

## 三、让票据打印机打印

1. 票据打印机一般是 **热敏打印机**，支持 58mm 或 80mm 宽度。
2. 你的 QWeb 模板里设置好宽度，比如 `style="width:80mm;"`。
3. 打印方式：

   * 默认是生成 PDF，你可以直接在浏览器里选择 **票据打印机**。
   * 如果要自动打印，可以安装 Odoo 的 **IoT Box** 或者配合 **cups 打印服务**做自动打印。

---

## 四、推荐开发流程

1. 先在测试环境里复制默认模板，改成简化版本。
2. 调整 CSS，直到在票据打印机里能正常显示。
3. 再上线使用。

---

✅ **总结**

* 在 Odoo 18 里，打印订单走的是 QWeb 模板。
* 你需要复制/继承 `sale.order` 的报表模板，自定义成票据格式（80mm/58mm 宽）。
* 注册一个新报表动作，让订单界面有“打印票据”按钮。
* 最终通过票据打印机打印。

---

要不要我帮你写一个 **完整的 Odoo 自定义模块骨架**（含 `__manifest__.py`、报表 XML、模板 XML），你可以直接安装到 Odoo，就能生成一个“票据打印版订单”？

太棒的需求！下面给你一份**可直接安装的 Odoo 18 自定义模块骨架**（“小票样式订单打印”），满足你贴的票据格式与排版。安装后，进入销售订单即可点击“打印小票”。

---

# 模块名称

`imon_receipt`

# 目录结构

```
imon_receipt/
├─ __init__.py
├─ __manifest__.py
├─ models/
│  └─ sale_order.py
├─ report/
│  ├─ receipt_report.xml      # 定义报表动作
│  └─ receipt_template.xml    # QWeb小票模板
└─ views/
   └─ sale_order_views.xml    # 在订单页面加入按钮/字段（可选）
```

---

## 1) `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    "name": "IMON Receipt - Ticket Print",
    "summary": "Jewelry IMON 小票格式销售订单打印",
    "version": "1.0.0",
    "category": "Accounting/Reporting",
    "author": "Your Team",
    "depends": ["sale", "account"],  # 使用 sale.order、税、金额等
    "data": [
        "report/receipt_template.xml",
        "report/receipt_report.xml",
        "views/sale_order_views.xml",
    ],
    "assets": {},
    "license": "LGPL-3",
    "application": False,
    "installable": True,
}
```

---

## 2) `__init__.py`

```python
# -*- coding: utf-8 -*-
from . import models
```

---

## 3) `models/sale_order.py`

> 给 sale.order 增加一些字段，便于直接填入“收据号 / 传票号 / 负责人 / 现金支付 / 找零 / 营业编号”等。星期文本也一并计算，方便模板展示。

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime

WEEKDAY_MAP = {
    0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"
}

class SaleOrder(models.Model):
    _inherit = "sale.order"

    imon_business_no = fields.Char(string="营业编号", help="例：T2010701001070")
    imon_receipt_no = fields.Char(string="收据号")
    imon_slip_no = fields.Char(string="传票号")
    imon_responsible = fields.Char(string="负责人", help="可直接录入，如 YOH")
    imon_cash_paid = fields.Monetary(string="现金支付")
    imon_change = fields.Monetary(string="找零")
    imon_items_count = fields.Integer(string="合计件数", compute="_compute_imon_items_count", store=False)
    imon_weekday_text = fields.Char(string="星期文本", compute="_compute_imon_weekday_text", store=False)

    @api.depends("order_line.product_uom_qty")
    def _compute_imon_items_count(self):
        for order in self:
            order.imon_items_count = int(sum(order.order_line.mapped("product_uom_qty")))

    @api.depends("date_order")
    def _compute_imon_weekday_text(self):
        for order in self:
            dt = fields.Datetime.context_timestamp(order, order.date_order) if order.date_order else datetime.datetime.now()
            order.imon_weekday_text = WEEKDAY_MAP.get(dt.weekday(), "")

```

---

## 4) `report/receipt_report.xml`

> 定义一个新的报表动作，在销售订单页出现“打印小票”菜单项。类型使用 qweb-pdf（票据机打印 PDF 也可；若需直接ESC/POS打印需另行扩展）。

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <report
      id="action_report_imon_receipt"
      model="sale.order"
      string="打印小票"
      report_type="qweb-pdf"
      name="imon_receipt.report_imon_receipt_ticket"
      file="imon_receipt.report_imon_receipt_ticket"
      print_report_name="'Receipt - %s' % (object.name)"
  />
</odoo>
```

---

## 5) `report/receipt_template.xml`

> QWeb 模板（80mm 宽热敏小票），直出你给的版式。注意中文/日文字体由系统打印端控制；wkhtmltopdf 默认字体可满足大部分场景，若需要更漂亮字体可在打印机/系统层安装。

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <template id="report_imon_receipt_ticket">
    <t t-call="web.external_layout">
      <div class="page"
           style="width:80mm; padding:2mm 3mm; font-size:12px; line-height:1.5; -webkit-print-color-adjust:exact;">

        <!-- 抬头 -->
        <div style="text-align:center; font-weight:700; font-size:15px;">
          Jewelry IMON（井門珠宝）
        </div>
        <div style="text-align:center; margin-top:2px;">
          电话：03-5826-8818
        </div>
        <div style="text-align:center;">
          营业编号：<t t-esc="o.imon_business_no or ''"/>
        </div>
        <div style="text-align:center;">
          地址：东京都台东区上野5-26-16
        </div>

        <div style="text-align:center; margin:6px 0; font-weight:700;">
          ★黄金、铂金高价收购★<br/>
          ★免费估价、鉴定★
        </div>

        <div style="text-align:center; font-weight:700; border:1px solid #000; display:inline-block; padding:1px 4px;">
          免税 TAX FREE
        </div>

        <hr style="border:0; border-top:1px dashed #000; margin:8px 0"/>

        <!-- 头部信息 -->
        <div>
          <t t-set="dt" t-value="o.date_order and o.date_order.astimezone(o.env.user.tz and pytz.timezone(o.env.user.tz) or None) if hasattr(o.date_order,'astimezone') else o.date_order"/>
          <t t-set="locdt" t-value="o.date_order and o.date_order or o.create_date"/>
          <t t-raw="0"/>
          <div>
            日期：
            <t t-esc="format_datetime(o, o.date_order or o.create_date, tz=o.env.user.tz, dt_format='yyyy年MM月dd日（')"/>
            <t t-esc="o.imon_weekday_text or ''"/>
            <t t-esc="format_datetime(o, o.date_order or o.create_date, tz=o.env.user.tz, dt_format='）HH:mm')"/>
          </div>
          <div>编号：<t t-esc="o.name"/></div>
          <div>收据号：<t t-esc="o.imon_receipt_no or ''"/></div>
          <div>传票号：<t t-esc="o.imon_slip_no or ''"/></div>
          <div>负责人：<t t-esc="o.imon_responsible or (o.user_id and o.user_id.name) or ''"/></div>
        </div>

        <hr style="border:0; border-top:1px dashed #000; margin:8px 0"/>

        <!-- 商品明细 -->
        <div style="font-weight:700; margin-bottom:4px;">商品明细</div>
        <t t-foreach="o.order_line" t-as="line">
          <div style="display:flex; justify-content:space-between;">
            <div style="width:58mm; word-break:break-all;">
              •<t t-esc="line.product_id.display_name"/>
              ×<t t-esc="int(line.product_uom_qty) if float(line.product_uom_qty).is_integer() else line.product_uom_qty"/>
              件
            </div>
            <div>
              <t t-esc="formatLang(line.price_total, currency_obj=o.currency_id)"/>
            </div>
          </div>
        </t>

        <hr style="border:0; border-top:1px dashed #000; margin:8px 6px"/>

        <!-- 合计 -->
        <div style="display:flex; justify-content:space-between; font-weight:700;">
          <div>合计（TOTAL）：<t t-esc="o.imon_items_count"/>件</div>
          <div><t t-esc="formatLang(o.amount_total, currency_obj=o.currency_id)"/></div>
        </div>
        <div style="text-align:right; margin-top:3px;">
          （含消费税TAX <t t-esc="int(round((o.amount_total - o.amount_untaxed) and (o.amount_total - o.amount_untaxed)/o.amount_untaxed*100 or 0))"/>%）
        </div>

        <hr style="border:0; border-top:1px dashed #000; margin:8px 6px"/>

        <!-- 付款 -->
        <div style="font-weight:700; margin-bottom:4px;">付款</div>
        <div style="display:flex; justify-content:space-between;">
          <div>•现金支付：</div>
          <div><t t-esc="formatLang(o.imon_cash_paid or 0.0, currency_obj=o.currency_id)"/></div>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <div>•找零：</div>
          <div><t t-esc="formatLang(o.imon_change or 0.0, currency_obj=o.currency_id)"/></div>
        </div>

      </div>
    </t>
  </template>
</odoo>
```

> 说明：
>
> * 宽度设为 `80mm`，适配80mm票据机；若58mm，改为 `width:58mm`。
> * 日期使用 `format_datetime`（Odoo 18 提供）+ 计算字段 `imon_weekday_text` 输出中文星期。
> * 金额使用 `formatLang`，随订单币种显示。
> * 明细行用 `line.price_total`（含税/不含税可按需调整成 `price_subtotal`）。
> * 顶部“免税 TAX FREE”等完全按你样式。

---

## 6) `views/sale_order_views.xml`

> 在销售订单表单上露出自定义字段，方便填“营业编号/收据号/传票号/负责人/现金/找零”，并在打印下拉里显示“打印小票”。

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <record id="view_order_form_inherit_imon" model="ir.ui.view">
    <field name="name">sale.order.form.imon.receipt</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
      <xpath expr="//sheet/notebook/page[1]" position="after">
        <group string="IMON 收据信息">
          <field name="imon_business_no"/>
          <field name="imon_receipt_no"/>
          <field name="imon_slip_no"/>
          <field name="imon_responsible"/>
          <field name="imon_cash_paid"/>
          <field name="imon_change"/>
          <field name="imon_items_count" readonly="1"/>
        </group>
      </xpath>
      <!-- 在 打印 下拉里显示“打印小票”（新版通常自动出现report按钮；此处确保显示） -->
      <xpath expr="//header" position="inside">
        <button name="%(imon_receipt.action_report_imon_receipt)d"
                type="action" string="打印小票" class="btn-secondary"
                context="{'discard_logo_check': True}"/>
      </xpath>
    </field>
  </record>
</odoo>
```

---

# 使用步骤

1. 把上面的目录与文件放到 Odoo 的自定义模块目录（如 `/opt/odoo/custom_addons/imon_receipt`）。
2. **更新应用列表**：设置 → 应用 → 更新应用列表。
3. 搜索并安装 **IMON Receipt - Ticket Print**。
4. 进入 **销售 → 报价单/订单**，打开一张订单：

   * 填写：营业编号、收据号、传票号、负责人、现金支付、找零。
   * 点击顶部的 **打印小票**。
5. 选择你的 **票据打印机**（80mm/58mm），打印即可。

---

# 打印与显示小贴士

* 建议安装 `wkhtmltopdf`（Odoo 日志也提示缺少），否则 PDF 打印可能效果不稳定。
* 如果你希望**直接无 PDF 弹窗**在门店自动打印，需要配 **Odoo IoT Box** 或在内网配置 CUPS 打印服务与自定义自动打印模块（后续我可以给你再做一个“直打版”）。
* 需要 58mm → 把模板 `width:80mm;` 改为 `width:58mm;`，适当调小字体。
* 若需把“商品显示”改为你展示的**精确名称**（如“PT喜平手链 / K18喜平手链”），在产品名或订单行描述填写即可，模板取 `line.product_id.display_name` 或 `line.name`。（`line.name`更自由）

---

如果你愿意，我可以把这套代码**打成一个zip**给你直接安装，或者根据你们的**LOGO、公司抬头、税号位置**微调一版，做到“开箱即用”。


*********************************************************************************************************************************************************



*********************************************************************************************************************************************************



*********************************************************************************************************************************************************



*********************************************************************************************************************************************************



*********************************************************************************************************************************************************

REPO_URL="https://rainth888:thun700522@github.com/rainth888/odoo.git"
WORK_DIR="/data/odoo.github.rainth888"
BRANCH="Branch_18.0.chowtaiking"

git clone --branch "$BRANCH" --single-branch "$REPO_URL" .

*********************************************************************************************************************************************************



*********************************************************************************************************************************************************





