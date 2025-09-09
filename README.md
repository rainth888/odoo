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
