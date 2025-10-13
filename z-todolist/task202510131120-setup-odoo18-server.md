# task202510131120-setup-odoo18-server

## Original Request
我新申请了一个云服务器，ubuntu22.4，两个存储盘分别都是80G。要准备安装生产环境的odoo18系统，从零开始装，数据库需要使用docker来装。需要帮我写一个完整的，详细的过程，包括但不限于：加载硬盘，合理分配两个硬盘的应用存储，安装数据库、odoo18（我有github库代码，Branch_18.0.chowtaiking分支）使用nginx配置外网访问，外网域名jpp.chwwdk.com。将整体业务流程写入z-todolist。

## Improved English Phrasing
Set up a production Odoo 18 environment on a fresh Ubuntu 22.04 server that has two 80 GB disks. Provision storage properly, mount the extra disk, deploy PostgreSQL in Docker, install Odoo 18 from the GitHub branch `Branch_18.0.chowtaiking`, expose it to the public via Nginx with the domain `jpp.chwwdk.com`, and document the full process inside `z-todolist`.

## Technical Analysis
- **Infrastructure**: Ubuntu 22.04 with two NVMe disks (`/dev/nvme0n1` already holding the OS, `/dev/nvme1n1` expected to be free). Need to partition, format, and mount the extra disk for application data.
- **Storage layout**: Keep the system disk for OS + application code. Dedicate the second disk to persistent data (PostgreSQL volume, Odoo filestore, backups). Ensure mounts persist via `/etc/fstab`.
- **Database**: PostgreSQL must run in Docker. Docker Compose simplifies lifecycle management and allows explicit volume and network definitions.
- **Odoo application**: Deploy Odoo 18 from the provided GitHub branch, managed by a dedicated `odoo` system user, with Python virtual environment and dependencies installed. Configure `odoo.conf` accordingly.
- **Services**: Create systemd units for both Odoo and (optionally) the Docker Compose stack to start on boot. Ensure network communication with the Dockerized PostgreSQL.
- **Reverse proxy**: Configure Nginx to proxy `jpp.chwwdk.com` to the Odoo backend on port 8069, handle timeouts, gzip, headers, and optionally TLS (Let's Encrypt).
- **Operational docs**: Provide command-by-command instructions, verification steps, and ongoing maintenance tips.

## Steps
1. **Record task & plan**
   - 更新 `_todolis.md` 并创建本任务文件，准备详细部署方案。

2. **准备磁盘与挂载点**
   - 查看磁盘：
     ```bash
     lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT
     sudo fdisk -l
     ```
   - 如果 `/dev/nvme1n1` 未分区，创建 GPT 分区并格式化：
     ```bash
     sudo parted /dev/nvme1n1 --script mklabel gpt
     sudo parted /dev/nvme1n1 --script mkpart primary ext4 0% 100%
     sudo mkfs.ext4 -L odoo-data /dev/nvme1n1p1
     ```
   - 挂载到 `/srv/odoo-data` 并创建目录：
     ```bash
     sudo mkdir -p /srv/odoo-data
     sudo mount /dev/nvme1n1p1 /srv/odoo-data
     sudo mkdir -p /srv/odoo-data/{postgres,filestore,backups,docker}
     sudo chown root:root /srv/odoo-data
     sudo chmod 750 /srv/odoo-data
     ```
   - 写入 `/etc/fstab` 以便开机自动挂载：
     ```bash
     sudo blkid /dev/nvme1n1p1
     # 假设 UUID=XXXXXXXX
     echo 'UUID=XXXXXXXX /srv/odoo-data ext4 defaults 0 2' | sudo tee -a /etc/fstab
     sudo mount -a
     df -h | grep odoo-data
     ```

3. **安装基础软件与 Odoo 用户**
   - 更新系统并安装依赖：
     ```bash
     sudo apt update && sudo apt upgrade -y
     sudo apt install -y git python3-venv python3-pip build-essential libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libjpeg-dev libpng-dev libevent-dev \
       libffi-dev libssl-dev wkhtmltopdf curl gnupg lsb-release unzip logrotate
     ```
   - 创建 `odoo` 系统用户与目录：
     ```bash
     sudo adduser --system --home /opt/odoo --group odoo
     sudo mkdir -p /opt/odoo/{etc,logs,src}
     sudo chown -R odoo:odoo /opt/odoo
     sudo chown -R odoo:odoo /srv/odoo-data/{filestore,backups}
     sudo chown -R 999:999 /srv/odoo-data/postgres  # 999 是 postgres 容器用户
     ```

4. **安装 Docker 与 Compose**
   - 安装并配置 Docker：
     ```bash
     sudo apt install -y docker.io docker-compose-plugin
     sudo systemctl enable --now docker
     sudo usermod -aG docker odoo
     sudo usermod -aG docker $USER  # 方便当前管理员操作
     newgrp docker
     docker info
     ```

5. **通过 Docker Compose 部署 PostgreSQL**
   - 准备 Compose 文件：
     ```bash
     sudo -u odoo mkdir -p /opt/odoo/docker
     sudo tee /opt/odoo/docker/docker-compose.yml <<'YAML'
     version: '3.9'
     services:
       postgres:
         image: postgres:16
         container_name: odoo-postgres
         restart: unless-stopped
         environment:
           POSTGRES_DB: odoo
           POSTGRES_USER: odoo
           POSTGRES_PASSWORD: ReplaceWithStrongPassword
         volumes:
           - /srv/odoo-data/postgres:/var/lib/postgresql/data
         networks:
           - odoo-net
         ports:
           - "5432:5432"
     networks:
       odoo-net:
         name: odoo-net
     YAML
     sudo chown odoo:odoo /opt/odoo/docker/docker-compose.yml
     ```
   - 启动数据库并检查：
     ```bash
     sudo -u odoo docker compose -f /opt/odoo/docker/docker-compose.yml up -d
     docker ps --format 'table {{.Names}}	{{.Status}}	{{.Ports}}'
     docker logs -f odoo-postgres
     ```

6. **拉取 Odoo 代码并配置 Python 环境**
   - 克隆仓库并切换分支：
     ```bash
     sudo -u odoo git clone https://github.com/<your-org>/<repo>.git /opt/odoo/src/odoo18
     sudo -u odoo git -C /opt/odoo/src/odoo18 checkout Branch_18.0.chowtaiking
     ```
   - 创建虚拟环境并安装依赖：
     ```bash
     sudo -u odoo python3 -m venv /opt/odoo/venv
     sudo -u odoo /opt/odoo/venv/bin/pip install --upgrade pip wheel setuptools
     sudo -u odoo /opt/odoo/venv/bin/pip install -r /opt/odoo/src/odoo18/requirements.txt
     ```
   - 若有自定义模块，可放在 `/opt/odoo/src/odoo18/addons_custom` 并确认权限。

7. **编写 Odoo 配置文件**
   - 新建 `/opt/odoo/etc/odoo.conf`：
     ```bash
     sudo tee /opt/odoo/etc/odoo.conf <<'CONF'
     [options]
     admin_passwd = ChangeThisMasterPassword
     db_host = 127.0.0.1
     db_port = 5432
     db_user = odoo
     db_password = ReplaceWithStrongPassword
     addons_path = /opt/odoo/src/odoo18/odoo/addons,/opt/odoo/src/odoo18/addons,/opt/odoo/src/odoo18/addons_custom
     data_dir = /srv/odoo-data/filestore
     logfile = /opt/odoo/logs/odoo.log
     proxy_mode = True
     limit_memory_hard = 2684354560
     limit_memory_soft = 2147483648
     limit_time_cpu = 120
     limit_time_real = 240
     workers = 4
     xmlrpc_port = 8069
     longpolling_port = 8072
     CONF
     sudo chown odoo:odoo /opt/odoo/etc/odoo.conf
     sudo chmod 640 /opt/odoo/etc/odoo.conf
     ```

8. **创建 systemd 服务**
   - 编写 `/etc/systemd/system/odoo.service`：
     ```bash
     sudo tee /etc/systemd/system/odoo.service <<'SERVICE'
     [Unit]
     Description=Odoo 18 Application Service
     After=network.target docker.service
     Requires=docker.service

     [Service]
     Type=simple
     User=odoo
     Group=odoo
     ExecStart=/opt/odoo/venv/bin/python /opt/odoo/src/odoo18/odoo-bin -c /opt/odoo/etc/odoo.conf
     ExecReload=/bin/kill -HUP $MAINPID
     KillMode=mixed
     Restart=on-failure
     RestartSec=5s
     WorkingDirectory=/opt/odoo/src/odoo18

     [Install]
     WantedBy=multi-user.target
     SERVICE
     sudo systemctl daemon-reload
     sudo systemctl enable --now odoo.service
     sudo journalctl -u odoo -f
     ```

9. **验证 PostgreSQL 连接**
   - 使用 `psql` 确认 Odoo 可以连接数据库：
     ```bash
     docker exec -it odoo-postgres psql -U odoo -d odoo -c '\l'
     sudo -u odoo /opt/odoo/venv/bin/python /opt/odoo/src/odoo18/odoo-bin shell -c /opt/odoo/etc/odoo.conf -d odoo --stop-after-init
     ```
   - 若尚未创建数据库，可先执行 `CREATE DATABASE` 或让 Odoo 后台安装时创建。

10. **配置 Nginx 反向代理**
    - 安装 Nginx 并创建站点配置：
      ```bash
      sudo apt install -y nginx
      sudo tee /etc/nginx/sites-available/jpp.chwwdk.com <<'NGINX'
      server {
          listen 80;
          server_name jpp.chwwdk.com;

          access_log /var/log/nginx/jpp.chwwdk.com.access.log;
          error_log  /var/log/nginx/jpp.chwwdk.com.error.log;

          proxy_read_timeout 720s;
          proxy_connect_timeout 720s;
          proxy_send_timeout 720s;

          gzip on;
          gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript;

          location / {
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
              proxy_set_header X-Forwarded-Host $host;
              proxy_set_header X-Forwarded-Port $server_port;
              proxy_redirect off;
              proxy_buffering off;
              proxy_pass http://127.0.0.1:8069;
          }

          location /longpolling {
              proxy_pass http://127.0.0.1:8072;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
          }
      }
      NGINX
      sudo ln -s /etc/nginx/sites-available/jpp.chwwdk.com /etc/nginx/sites-enabled/
      sudo nginx -t
      sudo systemctl reload nginx
      ```
    - 若需 HTTPS，使用 Certbot 获取证书：
      ```bash
      sudo snap install core; sudo snap refresh core
      sudo snap install --classic certbot
      sudo ln -s /snap/bin/certbot /usr/bin/certbot
      sudo certbot --nginx -d jpp.chwwdk.com
      sudo systemctl reload nginx
      ```

11. **最终检查与运维建议**
    - 测试服务：
      ```bash
      curl -I http://127.0.0.1:8069
      curl -I https://jpp.chwwdk.com  # 启用 HTTPS 后
      sudo systemctl status odoo
      docker ps
      ```
    - 初始化数据库、创建管理员账号，并确认附件存储到 `/srv/odoo-data/filestore`。
    - 设置备份脚本（例如 `/usr/local/bin/odoo-backup.sh` 使用 `pg_dump` + `tar` 归档 filestore），并配置 cron。
    - 使用 `ufw` 或云厂商安全组开放 22/80/443 端口，限制其他访问。

## Files Changed
- `z-todolist/_todolis.md`
- `z-todolist/task202510131120-setup-odoo18-server.md`

## Apply / Verify
1. 按照磁盘命令 (`lsblk`, `parted`, `mkfs.ext4`, `mount`) 将第二块磁盘挂载至 `/srv/odoo-data`，通过 `df -h` 验证容量。
2. 在 `/opt/odoo/docker` 下运行 `docker compose up -d`，用 `docker ps` 确认 PostgreSQL 容器状态为 `Up`。
3. 启动 `odoo.service`，通过 `journalctl -u odoo -f` 观察日志直到监听端口 8069。
4. 使用 `curl -I http://jpp.chwwdk.com`（或 `https://`）验证 Nginx 反向代理是否工作。
5. 登录前端创建生产数据库，确认附件写入 `/srv/odoo-data/filestore`，并执行一次备份测试。

## Next
- 设计自动备份策略（`pg_dump` + filestore rsync）存放至 `/srv/odoo-data/backups` 或异地存储。
- 启用 UFW 并仅开放必要端口，结合云端安全组增强防护。
- 部署监控和日志轮转（`logrotate` 针对 `/opt/odoo/logs/odoo.log`），以及系统资源告警。

## Detailed Technical Analysis Process
1. 评估服务器硬件结构并决定根磁盘与数据磁盘的职责分工，避免应用与数据混用导致迁移困难。
2. 选择 ext4 格式和 `/srv/odoo-data` 挂载点，规划 PostgreSQL、Odoo filestore、备份与 Docker 工作目录的权限与归属。
3. 确定使用 Docker Compose 管理单个 PostgreSQL 容器，方便将来升级与重启，并通过挂载目录确保数据持久化。
4. 分析 Odoo 18 的依赖项，准备 Python 虚拟环境、系统库、wkhtmltopdf 等打印组件，确保生产环境稳定。
5. 设计 `odoo.conf` 参数，启用 `proxy_mode` 与合理的 `workers`、资源限制，兼容 Nginx 代理与长轮询需求。
6. 编写 systemd 服务脚本，使 Odoo 在系统启动时自动拉起并在失败后自动重启，满足生产可靠性。
7. 提供 Nginx 反向代理配置，涵盖静态压缩、长轮询路径、头部透传及 HTTPS 部署步骤，确保对外访问安全稳定。
8. 补充验证、备份、防火墙与监控建议，保证上线后的可观测性与灾备能力。

## Work Summary / 变更说明
- 记录并分析了在 Ubuntu 22.04 服务器上部署生产 Odoo 18（PostgreSQL Docker、Nginx 反向代理、双磁盘存储规划）的完整实施方案。
- 输出了包含分区、挂载、服务部署、配置文件、验证步骤与后续运维建议的命令级流程文档。
