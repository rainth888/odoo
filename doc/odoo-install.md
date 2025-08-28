

# python3.11安装


*********************************************************************************************************************************************************

你现在遇到的 **“Unable to locate package python3.11”** 基本可以确定是 **Ubuntu 版本太旧**（WSL2 默认装的是 Ubuntu 18.04，而 **deadsnakes PPA 对 18.04 的 Python 3.11 包已经停止维护**）。  
解决思路有两条，推荐按先后顺序尝试。

------------------------------------------------
路线 1：就地升级到 Ubuntu 20.04 / 22.04（**最快最干净**，10 分钟）

1. 备份（可选但建议）
   ```bash
   sudo apt install -y etckeeper   # 会自动把 /etc 备份到 git
   ```

2. 升级到 20.04  
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo do-release-upgrade       # 一路 y / 回车
   ```
   结束后会重启 WSL2（`wsl --shutdown` 再重新进入）。  
   如果想一步到位到 22.04，可以再执行一次 `sudo do-release-upgrade -d`。

3. 升级完成后再加 PPA & 安装 3.11  
   ```bash
   sudo apt install -y software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt update
   sudo apt install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils
   ```

4. 验证  
   ```bash
   python3.11 --version   # Python 3.11.x
   ```

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


需要，但只需 **一条命令** 就能给刚编译好的 3.11 装上专属 pip，且不会影响系统自带 3.6：

```bash
# 用 3.11 自带的 ensurepip 装（最简）
/usr/local/bin/python3.11 -m ensurepip --upgrade
```

或传统方案（二选一即可）：

```bash
# 方案 2：官方 get-pip.py
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo /usr/local/bin/python3.11
```

验证：

```bash
/usr/local/bin/python3.11 -m pip --version
# 输出示例：pip 24.2 from /usr/local/lib/python3.11/site-packages/pip (python 3.11)
```

以后用 `py311 -m pip install xxx` 或进入虚拟环境后直接用 `pip install xxx`，都不会跟系统 3.6 冲突。


*********************************************************************************************************************************************************
# py311进入虚拟环境

针对odoo系统路径/d/_projects/odoo.github.rainth888，要进行pip编译，那么py311如何进入虚拟环境

下面给你几种常见场景下，用 **Python 3.11（py311）创建并进入虚拟环境** 的最简步骤。你要操作的 Odoo 目录是
`D:\_projects\odoo.github.rainth888`（WSL 下路径为 `/mnt/d/_projects/odoo.github.rainth888`）。

---

## A. 在 **WSL2（Ubuntu/Debian）** 里操作

> 建议：在 WSL 的 Linux 文件系统里建 venv（速度更快），代码目录仍可在 `/mnt/d/...`。

1. 安装 Python3.11 及 venv 组件（若未安装）

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv
```

2. 进入项目目录并创建虚拟环境

```bash
cd /mnt/d/_projects/odoo.github.rainth888
python3.11 -m venv .venv


```

3. \*\*进入（激活）\*\*虚拟环境

```bash
source .venv/bin/activate
# 验证
python -V     # Python 3.11.x
pip -V
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



4. 安装依赖 / 编译（pip 装包）

```bash
python -m pip install --upgrade pip wheel setuptools
# 如果项目有 requirements.txt：
pip install -r requirements.txt
# 国内可加镜像，例如：
# pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
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

---

## B. 在 **Windows PowerShell** 里操作（不进 WSL）

> 需要已安装 Windows 版 Python 3.11（带 *Python Launcher* 更方便）。

1. 创建虚拟环境（项目根目录执行）

```powershell
cd D:\_projects\odoo.github.rainth888
py -3.11 -m venv .venv
```

2. \*\*进入（激活）\*\*虚拟环境

```powershell
.\.venv\Scripts\Activate.ps1
# 若被执行策略拦截，可临时放开：
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

（CMD 用法：`.\.venv\Scripts\activate.bat`；Git Bash：`source .venv/Scripts/activate`）

3. 安装依赖

```powershell
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

4. 退出

```powershell
deactivate
```

---

## C. 性能优化建议（可选）

* WSL2 在 `/mnt/d` 上 I/O 略慢。可在 WSL **家目录**建 venv，例如：

  ```bash
  python3.11 -m venv ~/venvs/odoo311
  source ~/venvs/odoo311/bin/activate
  # 然后针对挂载的代码目录安装
  pip install -e /mnt/d/_projects/odoo.github.rainth888
  ```
* VS Code：在工作区选择 Python 解释器为 **项目根/.venv**（或 `~/venvs/odoo311`）。

---

## D. 常见问题

* `python3.11: command not found` → 先 `sudo apt install python3.11 python3.11-venv`。
* `Activate.ps1 被阻止` → PowerShell 临时执行：`Set-ExecutionPolicy -Scope Process Bypass`。
* 需代理安装依赖：沿用你之前的 WSL 代理环境变量（`http_proxy/https_proxy`），或为 pip 指定镜像源。

> 总结：**创建** `python3.11 -m venv .venv`（或 `py -3.11 -m venv .venv`），**进入** `source .venv/bin/activate`（WSL）或 `.\.venv\Scripts\Activate.ps1`（PowerShell），然后 `pip install -r requirements.txt` 即可。

*********************************************************************************************************************************************************

安装下面这个扩展包，怎么在py311下执行：
sudo apt install python3-pip libldap2-dev libpq-dev libsasl2-dev

你这台机器里已经有 **Python 3.11**（`python3.11` 可以启动），所以 `apt` 再去装 `python3.11 / python3.11-venv` 才会提示“找不到该包”（你的 3.11 多半是源码安装/pyenv，不是 APT 管理的版本）。
结论：**不用 apt 装 3.11**，直接装系统级依赖，然后用现有的 `python3.11` 建虚拟环境即可。

按下面做就行（WSL2 里执行）：

---

## 1) 装系统级依赖（给 C 扩展编译用）

```bash
sudo apt update
sudo apt install -y \
  build-essential libldap2-dev libpq-dev libsasl2-dev \
  libssl-dev libffi-dev pkg-config
# 验证 pg 客户端头/工具是否就绪
pg_config --version
```

> 这些库用于编译 `python-ldap`（需要 `libldap2-dev`/`libsasl2-dev`）和 `psycopg2`（需要 `libpq-dev`）。
> `python3-pip` 可装可不装；虚拟环境里自带 pip。

---

## 2) 在项目目录创建并进入 **py311** 虚拟环境

```bash
cd /mnt/e/_projects/odoo.github.rainth888   # 你的路径在 WSL 下是 /mnt/e/...
python3.11 -m venv .venv
source .venv/bin/activate

# 如提示没有 pip，则：
python -m ensurepip --upgrade

python -V      # 应显示 Python 3.11.x
pip -V
```

---

## 3) 升级打包工具并安装依赖（pip 编译）

```bash
python -m pip install --upgrade pip setuptools wheel

# 如果你有 requirements.txt：
pip install -r requirements.txt

# 或单独安装常见包（示例）：
pip install psycopg2            # 用 libpq-dev 编译（推荐）
# 或开发调试时临时：
# pip install psycopg2-binary

pip install python-ldap         # 需要 libldap2-dev / libsasl2-dev
```

快速验证：

```bash
python -c "import psycopg2,ldap,sys; print(sys.version); print(psycopg2.__version__)"
```

---

## 4) 常见问题排查

* `fatal error: sasl.h: No such file or directory` → 安装 `libsasl2-dev`。
* `pg_config not found` → 安装 `libpq-dev`（已在第 1 步）。
* `No module named ensurepip` → 你的 3.11 是最小化编译，先 `sudo apt install python3-venv`（针对系统 Python），或重新编译启用 ensurepip；临时也可用 `get-pip.py`。
* `/mnt/e` 上 I/O 慢 → 可把 venv 建在 WSL 的 Linux 磁盘（如 `~/venvs/odoo311`），再对 `/mnt/e/...` 安装：

  ```bash
  python3.11 -m venv ~/venvs/odoo311
  source ~/venvs/odoo311/bin/activate
  pip install -e /mnt/e/_projects/odoo.github.rainth888
  ```

---

## 可选：一定要用 APT 安装 3.11？

* **Ubuntu 20.04/22.04** 可用 **deadsnakes** PPA：`sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt install python3.11 python3.11-venv`
* **Debian 老版本**可用 backports。
  不过你当前已能用 `python3.11`，**没必要再装 apt 版**。

---

接下来你就可以在这个 `.venv` 里执行 Odoo 的 pip 安装/编译了。需要的话我可以帮你把项目的 `requirements.txt`（或 Odoo 指定依赖）整理成国内镜像的一键安装命令。



*********************************************************************************************************************************************************
python3 odoo-bin --addons-path=addons -d pdemo
py311 odoo-bin --addons-path=addons -d pdemo


创建数据库odoo

# 连接到 PostgreSQL 容器
docker exec -it pg170 psql -U postgres

# 在 PostgreSQL 中执行以下命令：
CREATE USER proot WITH PASSWORD 'proot';
CREATE DATABASE odoo OWNER proot;
GRANT ALL PRIVILEGES ON DATABASE odoo TO proot;
\q

# 使用新创建的数据库运行 Odoo
python odoo-bin --addons-path=addons -d odoo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot
python odoo-bin --addons-path=addons -d odoo --db_host=pg170 --db_port=5432 --db_user=proot --db_password=proot -i base

# 假设容器 IP 是 172.17.0.2（请根据实际 IP 调整）
python odoo-bin --addons-path=addons -d odoo --db_host=172.17.0.2 --db_port=5432 --db_user=proot --db_password=proot -i base

*********************************************************************************************************************************************************

# 模块安装

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

你这次报错的根因有三点：

1. `CREATE DATABASE` 不能在 `DO $$ ... $$;` 里执行（它相当于函数/事务块内执行，PG 会拒绝）。
2. 你的 heredoc 中间有复制粘贴残留（`IF NOT EXISTS (SELECT FROM pg>`、`GES ON DATABASE >` 等），把 SQL 打断了。
3. 你在 `\c pdemo` 切库之前，`pdemo` 还没成功创建，自然会报 “database does not exist”。

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



# 太棒了！从你贴的结果看，一切都成功了：

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

---

有需要我把这些命令打包成一个“菜单脚本”（一键：初始化/自测/远程开关/备份恢复）吗？你直接运行、选项式操作就行。


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





*********************************************************************************************************************************************************





*********************************************************************************************************************************************************

下面给你 **WSL2 下安装 PostgreSQL 17.0** 的三种做法。差异在于你是否“必须精确就是 17.0”。如果不一定非 17.0，小版本用最新最安全的 **17.x** 更合适（方案 A）。若**严格要求 17.0**，用 **源码编译**（方案 B）或 **Docker 指定镜像标签**（方案 C）。

---

## ✅ 方案 A：APT 安装（得到 17 系列最新小版本，最省心）

> 适用于 WSL2 的 Ubuntu/Debian。包名是 `postgresql-17`，安装的是 **17.x 的最新补丁版**（不是 17.0 原始版，但更安全）。

```bash
# 1) 加官方 PGDG APT 源
sudo apt update
sudo apt install -y wget gnupg lsb-release
wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc \
 | sudo gpg --dearmor -o /usr/share/keyrings/pgdg.gpg
echo "deb [signed-by=/usr/share/keyrings/pgdg.gpg] http://apt.postgresql.org/pub/repos/apt/ \
$(lsb_release -cs)-pgdg main" \
 | sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt update

# 2) 安装 17 系列
sudo apt install -y postgresql-17 postgresql-client-17
```

**启动方式（按你是否开启了 systemd 选择）**

* 若 WSL2 已启用 systemd：

  ```bash
  sudo systemctl enable --now postgresql
  sudo systemctl status postgresql
  ```
* 未启用 systemd：

  ```bash
  sudo pg_ctlcluster 17 main start
  sudo pg_lsclusters
  ```

**验证：**

```bash
sudo -u postgres psql -c "SELECT version();"
```

**配置文件（默认路径）：**
`/etc/postgresql/17/main/postgresql.conf`、`pg_hba.conf`
**数据目录：** `/var/lib/postgresql/17/main`

> 允许从 Windows 连接 WSL：在 `postgresql.conf` 设 `listen_addresses='*'`；在 `pg_hba.conf` 增加你的子网白名单（如 `host all all 172.19.0.0/16 md5`），然后重启。

---

## 🎯 方案 B：源码编译“精确 17.0”（严格版本要求时用）

> 17.0 是最初发布的小版本，**不含后续安全补丁**。建议仅用于复现/兼容性测试。

```bash
# 1) 依赖
sudo apt update
sudo apt install -y build-essential libreadline-dev zlib1g-dev \
  flex bison libssl-dev libxml2-dev libxslt1-dev libicu-dev \
  tcl-dev libperl-dev libpython3-dev pkg-config

# 2) 下载并编译 v17.0
cd /tmp
wget https://ftp.postgresql.org/pub/source/v17.0/postgresql-17.0.tar.gz
tar xf postgresql-17.0.tar.gz
cd postgresql-17.0
./configure --prefix=/usr/local/pgsql-17.0 \
  --with-openssl --with-libxml --with-libxslt --with-icu
make -j"$(nproc)"
sudo make install

# 3) 初始化与启动
sudo useradd -r -s /bin/false postgres 2>/dev/null || true
sudo mkdir -p /usr/local/pgsql-17.0/data
sudo chown -R postgres:postgres /usr/local/pgsql-17.0

sudo -u postgres /usr/local/pgsql-17.0/bin/initdb -D /usr/local/pgsql-17.0/data
sudo -u postgres /usr/local/pgsql-17.0/bin/pg_ctl \
  -D /usr/local/pgsql-17.0/data -l /usr/local/pgsql-17.0/logfile start

# 4) 验证
/usr/local/pgsql-17.0/bin/psql -U postgres -c "SELECT version();"

# (可选) 加 PATH
echo 'export PATH=/usr/local/pgsql-17.0/bin:$PATH' >> ~/.bashrc && source ~/.bashrc
```

> 关闭：`sudo -u postgres /usr/local/pgsql-17.0/bin/pg_ctl -D /usr/local/pgsql-17.0/data stop`

---

## 🚀 方案 C：Docker（快速、可显式标签 17.0）

> 需要 Docker（可用 Docker Desktop + WSL2 集成）。**精确 17.0** 时，直接用镜像标签。

```bash
docker rm -f pg170 2>/dev/null

docker run -d --name pg170 \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v $HOME/pg17-data:/var/lib/postgresql/data \
  postgres:17.0



# 验证
docker exec -it pg170 psql -U postgres -c "SELECT version();"
```

> 如果拉取不到 `17.0` 标签，可用 `postgres:17`（拿到最新 17.x）。一定要锁定 17.0，可改用**镜像 digest**或找存档镜像。

---

## WSL2 常见注意点

* **systemd**：要用 `systemctl` 管服务，先在 `/etc/wsl.conf` 启用：

  ```ini
  [boot]
  systemd=true
  ```

  然后在 PowerShell：`wsl --shutdown` 再进来。
* **从 Windows 连接**：Win11 一般可直接 `localhost:5432`；若不行，查 WSL IP（`ip addr`）或确认 `listen_addresses` 与 `pg_hba.conf`。
* **端口冲突**：若 5432 被占，改 `postgresql.conf` 里的 `port`，或停掉其他实例。
* **代理环境**：在有代理时，`apt`/`wget`/`docker` 需要代理配置；TLS 证书请导入到 WSL（`update-ca-certificates`）。

---

## 该用哪种？

* **开发/生产建议**：方案 A（17.x 最新补丁，安全）
* **必须严格 17.0**：方案 B（源码）或方案 C（Docker 指定标签）

如果你告诉我当前发行版（`cat /etc/os-release`）和是否已启用 systemd，我可以把对应方案整理成**一键脚本**适配你的环境。


*********************************************************************************************************************************************************
# docker 引擎安装 

你的报错：

```
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

说明**WSL2 里没有在运行的 Docker 守护进程（dockerd）**，`docker` 只是客户端。要么用 **Docker Desktop（推荐）** 把引擎跑在 Windows 并对接 WSL，要么在 **WSL 发行版内安装原生 Docker Engine** 并启动它。二选一即可。



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
### 停止 或者终止postgresql10
```
bill@leiyu-pc:~$ sudo ss -ltnp | grep :5432
LISTEN   0         224                127.0.0.1:5432            0.0.0.0:*        users:(("postgres",pid=401,fd=7))      
bill@leiyu-pc:~$ sudo pg_lsclusters
Ver Cluster Port Status Owner    Data directory              Log file
10  main    5432 online postgres /var/lib/postgresql/10/main /var/log/postgresql/postgresql-10-main.log
bill@leiyu-pc:~$
bill@leiyu-pc:~$
bill@leiyu-pc:~$ sudo pg_ctlcluster 10 main stop
bill@leiyu-pc:~$ sudo sed -i 's/^auto/manual/' /etc/postgresql/10/main/start.conf
bill@leiyu-pc:~$
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

> 你命令里有一行误打的 `e POSTGRES_PASSWORD=postgres \`，下次去掉就行；真正生效的是后面的 `-e POSTGRES_PASSWORD=postgres`。

---

## 5) 备份 / 恢复（从宿主机直接做）

```bash
# 逻辑备份（自带压缩格式）
docker exec pg170 pg_dump -U postgres -Fc appdb > ~/appdb_$(date +%F).dump

# 恢复到空库（确保先 CREATE DATABASE）
docker exec -i pg170 pg_restore -U postgres -d appdb < ~/appdb_2025-08-26.dump

# 全库备份（含角色/库定义）
docker exec pg170 pg_dumpall -U postgres > ~/pg_all_$(date +%F).sql
```

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




*********************************************************************************************************************************************************
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





*********************************************************************************************************************************************************





*********************************************************************************************************************************************************





*********************************************************************************************************************************************************




# 安装 db postgresql
```
bill@leiyu-pc:~$ sudo apt update
[sudo] password for bill:
Hit:1 http://archive.ubuntu.com/ubuntu bionic InRelease
Get:2 http://security.ubuntu.com/ubuntu bionic-security InRelease [102 kB]
Get:3 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [102 kB]
Get:4 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [102 kB]
Fetched 305 kB in 14s (22.5 kB/s)
Reading package lists... Done
Building dependency tree
Reading state information... Done
16 packages can be upgraded. Run 'apt list --upgradable' to see them.

bill@leiyu-pc:~$ sudo apt install postgresql
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  libpq5 postgresql-10 postgresql-client-10 postgresql-client-common postgresql-common ssl-cert sysstat
Suggested packages:
  postgresql-doc locales-all postgresql-doc-10 libjson-perl openssl-blacklist isag
The following NEW packages will be installed:
  libpq5 postgresql postgresql-10 postgresql-client-10 postgresql-client-common postgresql-common ssl-cert sysstat
0 upgraded, 8 newly installed, 0 to remove and 16 not upgraded.
Need to get 5337 kB of archives.
After this operation, 20.9 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 libpq5 amd64 10.23-0ubuntu0.18.04.2 [107 kB]
Get:2 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 postgresql-client-common all 190ubuntu0.1 [29.6 kB]
Get:3 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 postgresql-client-10 amd64 10.23-0ubuntu0.18.04.2 [943 kB]
Get:4 http://archive.ubuntu.com/ubuntu bionic/main amd64 ssl-cert all 1.0.39 [17.0 kB]
Get:5 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 postgresql-common all 190ubuntu0.1 [157 kB]
Get:6 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 postgresql-10 amd64 10.23-0ubuntu0.18.04.2 [3781 kB]
Get:7 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 postgresql all 10+190ubuntu0.1 [5884 B]
Get:8 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 sysstat amd64 11.6.1-1ubuntu0.2 [295 kB]
Fetched 5337 kB in 23s (235 kB/s)
Preconfiguring packages ...
Selecting previously unselected package libpq5:amd64.
(Reading database ... 50863 files and directories currently installed.)
Preparing to unpack .../0-libpq5_10.23-0ubuntu0.18.04.2_amd64.deb ...
Unpacking libpq5:amd64 (10.23-0ubuntu0.18.04.2) ...
Selecting previously unselected package postgresql-client-common.
Preparing to unpack .../1-postgresql-client-common_190ubuntu0.1_all.deb ...
Unpacking postgresql-client-common (190ubuntu0.1) ...
Selecting previously unselected package postgresql-client-10.
Preparing to unpack .../2-postgresql-client-10_10.23-0ubuntu0.18.04.2_amd64.deb ...
Unpacking postgresql-client-10 (10.23-0ubuntu0.18.04.2) ...
Selecting previously unselected package ssl-cert.
Preparing to unpack .../3-ssl-cert_1.0.39_all.deb ...
Unpacking ssl-cert (1.0.39) ...
Selecting previously unselected package postgresql-common.
Preparing to unpack .../4-postgresql-common_190ubuntu0.1_all.deb ...
Adding 'diversion of /usr/bin/pg_config to /usr/bin/pg_config.libpq-dev by postgresql-common'
Unpacking postgresql-common (190ubuntu0.1) ...
Selecting previously unselected package postgresql-10.
Preparing to unpack .../5-postgresql-10_10.23-0ubuntu0.18.04.2_amd64.deb ...
Unpacking postgresql-10 (10.23-0ubuntu0.18.04.2) ...
Selecting previously unselected package postgresql.
Preparing to unpack .../6-postgresql_10+190ubuntu0.1_all.deb ...
Unpacking postgresql (10+190ubuntu0.1) ...
Selecting previously unselected package sysstat.
Preparing to unpack .../7-sysstat_11.6.1-1ubuntu0.2_amd64.deb ...
Unpacking sysstat (11.6.1-1ubuntu0.2) ...
Setting up sysstat (11.6.1-1ubuntu0.2) ...

Creating config file /etc/default/sysstat with new version
update-alternatives: using /usr/bin/sar.sysstat to provide /usr/bin/sar (sar) in auto mode
Created symlink /etc/systemd/system/multi-user.target.wants/sysstat.service → /lib/systemd/system/sysstat.service.
Setting up ssl-cert (1.0.39) ...
Setting up libpq5:amd64 (10.23-0ubuntu0.18.04.2) ...
Setting up postgresql-client-common (190ubuntu0.1) ...
Setting up postgresql-common (190ubuntu0.1) ...
Adding user postgres to group ssl-cert

Creating config file /etc/postgresql-common/createcluster.conf with new version
Building PostgreSQL dictionaries from installed myspell/hunspell packages...
Removing obsolete dictionary files:
Created symlink /etc/systemd/system/multi-user.target.wants/postgresql.service → /lib/systemd/system/postgresql.service.
Setting up postgresql-client-10 (10.23-0ubuntu0.18.04.2) ...
update-alternatives: using /usr/share/postgresql/10/man/man1/psql.1.gz to provide /usr/share/man/man1/psql.1.gz (psql.1.gz) in auto mode
Setting up postgresql-10 (10.23-0ubuntu0.18.04.2) ...
Creating new PostgreSQL cluster 10/main ...
/usr/lib/postgresql/10/bin/initdb -D /var/lib/postgresql/10/main --auth-local peer --auth-host md5
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.

The database cluster will be initialized with locale "C.UTF-8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

fixing permissions on existing directory /var/lib/postgresql/10/main ... ok
creating subdirectories ... ok
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default timezone ... Asia/Shanghai
selecting dynamic shared memory implementation ... posix
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok

Success. You can now start the database server using:

    /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l logfile start

Ver Cluster Port Status Owner    Data directory              Log file
10  main    5432 down   postgres /var/lib/postgresql/10/main /var/log/postgresql/postgresql-10-main.log
update-alternatives: using /usr/share/postgresql/10/man/man1/postmaster.1.gz to provide /usr/share/man/man1/postmaster.1.gz (postmaster.1.gz) in auto mode
Setting up postgresql (10+190ubuntu0.1) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
Processing triggers for ureadahead (0.100.0-21) ...
Processing triggers for libc-bin (2.27-3ubuntu1.6) ...
Processing triggers for systemd (237-3ubuntu10.57) ...
bill@leiyu-pc:~$

```
*********************************************************************************************************************************************************

PostgreSQL 不允许 **root** 启动，也不能让一个普通用户去写 **postgres** 的数据目录。  
正确做法：用 **postgres** 系统用户启动/管理实例。

1. 切到 postgres 用户  
   ```bash
   sudo -iu postgres
   ```

2. 启动（或注册成服务）  
   ```bash
   # 启动这一次
   /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l /tmp/pg.log start

   # 查看状态
   /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main status
   ```

3. 或者直接用 **systemd 服务**（推荐，WSL2 里也能用）  
   ```bash
   exit                       # 先回到 bill
   sudo systemctl start postgresql@10-main   # 立即启动
   sudo systemctl enable postgresql@10-main  # 开机自启
   ```

4. 验证  
   ```bash
   sudo -iu postgres psql -c "SELECT version();"
   # 能连进去就说明启动成功
   ```

问题根源  
- 你第一次用 `bill` 用户，没权限写 `/var/lib/postgresql/10/main/postmaster.pid` → “Permission denied”。  
- 第二次用 `sudo` 直接 root，PostgreSQL 拒绝 root 运行 → “cannot be run as root”。  

按上面的 **sudo -iu postgres** 或 **systemctl** 方式即可解决。

```
postgres@leiyu-pc:~$ # 启动这一次
in/pg_ctl -D /vapostgres@leiyu-pc:~$ /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l /tmp/pg.log start
/pg_ctl -D /var/lib/postgresql/10/main statuspg_ctl: another server might be running; trying to start server anyway
waiting for server to start.... stopped waiting
pg_ctl: could not start server
Examine the log output.
postgres@leiyu-pc:~$
postgres@leiyu-pc:~$ # 查看状态
postgres@leiyu-pc:~$ /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main status
pg_ctl: server is running (PID: 15003)
/usr/lib/postgresql/10/bin/postgres "-D" "/var/lib/postgresql/10/main" "-c" "config_file=/etc/postgresql/10/main/postgresql.conf"
postgres@leiyu-pc:~$

postgres@leiyu-pc:~$
postgres@leiyu-pc:~$ psql -c "SELECT version();"
                                                               version
--------------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 10.23 (Ubuntu 10.23-0ubuntu0.18.04.2) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0, 64-bit
(1 row)

postgres@leiyu-pc:~$

```

如何在wsl2下安装PostgreSQL版本为17.0 



*********************************************************************************************************************************************************

结论先行：**WinSCP 不能用来发起 TFTP 连接**。  
WinSCP 目前只支持 **SFTP、SCP、FTP(S)、WebDAV、Amazon S3** 等协议，在官方文档和界面里都没有 TFTP 选项。  
如果你的场景必须走 TFTP，请改用下列工具：

- **Tftpd64** / **3CDaemon**（Windows 图形界面，可做 TFTP 客户端/服务器）  
- **Windows 自带命令行 TFTP 客户端**（需勾选“启用或关闭 Windows 功能 → TFTP Client”）  
- **Linux/WSL 命令行**：`sudo apt install tftp-hpa` 后执行 `tftp <host>` 即可

一句话：想用图形界面传文件 → 继续用 WinSCP 的 SFTP/SCP；**必须 TFTP → 换 Tftpd64 或命令行 tftp**。

*********************************************************************************************************************************************************



*********************************************************************************************************************************************************



*********************************************************************************************************************************************************





