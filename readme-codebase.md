# Odoo 18 项目代码库架构与业务功能分析

本文基于当前代码仓库结构（Odoo 18 社区版源码 + 官方模块集）进行整体架构梳理与业务域模块盘点，帮助开发、实施与运维人员快速理解代码与功能的组织方式。

## 版本与总体概览

- 核心版本：Odoo 18（见 `odoo/release.py` 中 `version_info = (18, 0, 0, FINAL, 0, '')`）
- 主要组成：
  - 核心服务器框架（`odoo/`）
  - 官方模块集（`addons/`）
  - 基础内置模块与测试模块（`odoo/addons/`）
  - 命令入口与工具（`odoo-bin`、`setup/`、`odoo/cli/`）
  - 文档与说明（`doc/`、`README.md`、`SECURITY.md` 等）
  - 依赖清单（`requirements.txt`）与打包脚本（`setup.py`、`MANIFEST.in`）
  - 日志与示例配置（`logs/`、`debian/`、`setup/odoo-wsgi.example.py`）

## 分层与架构视图（高层）

从代码与运行时角度，可归纳为以下层次：

1) 数据层（PostgreSQL）
- 通过 `psycopg2` 驱动访问；连接管理与游标封装在 `odoo/sql_db.py`。
- Odoo ORM 层（`odoo/models.py`、`odoo/fields.py`、`odoo/api.py`）将业务对象映射到关系表。

2) 内核与服务层（Core + Services）
- 模块加载与注册表：`odoo/modules/`（`module.py`、`loading.py`、`registry.py`、`graph.py`）
- 服务器服务：`odoo/service/`（`server.py`、`db.py`、`model.py`、`security.py`、`common.py`）
- 配置与工具：`odoo/tools/`（缓存、国际化、时间与日期、图像、条码、JSON/CSV/XML 转换等）
- 配置解析：`odoo/tools/config.py`；日志级别：`odoo/loglevels.py`；异常：`odoo/exceptions.py`
- 兼容补丁：`odoo/_monkeypatches/`（第三方库行为修正）

3) 业务模型与逻辑层（ORM + Addons）
- ORM：`odoo/models.py`、字段：`odoo/fields.py`、API 装饰器：`odoo/api.py`
- 业务模块通过 `__manifest__.py` 声明依赖、数据、菜单、视图、访问控制；模型与业务逻辑位于 `addons/<module>/models/`。

4) 接口与控制器层（HTTP/RPC）
- HTTP 框架：`odoo/http.py`（路由、控制器、请求上下文）；WSGI 集成：`setup/odoo-wsgi.example.py`
- RPC（JSON-RPC/XML-RPC）经由 HTTP 层暴露；Web 客户端通过 `/web` 路由与后端交互。

5) 前端与视图层（Web/Website/JS）
- Web 客户端与基础组件：`addons/web/`、`addons/web_editor/`、`addons/web_tour/`、`addons/html_editor/`
- Website 站点与页面：`addons/website/` 及其生态（如 `website_blog`、`website_sale` 等）
- 资源打包与资产管理基于 Odoo 的 assets 机制（由 `web` 与内核工具协作处理）。

6) CLI 与运维工具
- 主入口：`odoo-bin`（等效 `python -m odoo`，见 `odoo/__main__.py`）
- CLI 命令：`odoo/cli/`（数据库、统计、部署等命令封装）
- Linux/Debian 相关脚本：`debian/`、`setup/`；Windows 安装脚本：`setup/win32/`

7) 升级与测试
- 升级框架：`odoo/upgrade/` 与示例升级脚本 `odoo/upgrade_code/`
- 测试框架：`odoo/tests/`，各模块也含有自身的测试（如 `addons/test_*`、`odoo/addons/test_*`）

## 关键目录与文件职责映射

- `odoo/`
  - `__init__.py`：内核初始化
  - `models.py`、`fields.py`、`api.py`：ORM/领域模型核心
  - `http.py`：HTTP 框架与控制器装饰器
  - `sql_db.py`：数据库连接与事务封装
  - `modules/`：模块加载、依赖解析、注册表与迁移
  - `service/`：服务器、数据库与安全服务（启动、管理、RPC）
  - `tools/`：通用工具与设施（缓存、i18n、时区、图像、条码、报表等）
  - `_monkeypatches/`：第三方库补丁（如 `lxml`、`urllib3` 等）
  - `release.py`：版本与产品元数据

- `addons/`（官方业务模块集，社区版）
  - 每个子目录为一个功能模块，包含 `__manifest__.py`、`models/`、`views/`、`security/`、`data/`、`report/`、`static/` 等。
  - 示例：`sale/`、`purchase/`、`stock/`、`account/`、`mrp/`、`hr/`、`point_of_sale/`、`website/`、`web/` 等。

- `odoo/addons/`
  - 内置基础模块与测试模块（例如 `base/`、大量 `test_*` 模块），补充核心测试与最小运行集。

- 其他：
  - `odoo-bin`：命令行启动器
  - `requirements.txt`：Python 依赖（按 Python 版本/平台精准钉死）
  - `setup/`、`debian/`：打包、安装与运维脚本
  - `doc/`：安装与配置文档（如 `doc/odoo-install.md`、`doc/odoo-configuration.md`）
  - `logs/`：日志输出目录（示例 `logs/odoo.log`）

## 模块生态与业务域功能一览（addons/）

以下按业务域对常见模块分组（仅列举本仓库中存在的代表性模块，非穷尽）：

- 基础与系统
  - `base`（位于 `odoo/addons/base`）：核心数据（公司/用户/权限/菜单/序列/附件/多语言等）
  - `mail`、`sms`、`bus`：消息、讨论、总线推送与短信能力
  - `auth_*`：认证（OAuth、LDAP、TOTP、密码策略、Passkey 等）
  - `iap*`：In-App 服务接入（例如丰富 CRM 线索等）

- Web 与网站
  - `web`、`web_editor`、`web_tour`、`html_editor`：Web 客户端、前端编辑与引导
  - `website`：网站与页面管理；生态含 `website_blog`、`website_crm`、`website_sale*`（电商）等

- CRM 与营销
  - `crm`、`crm_livechat`、`crm_mail_plugin`、`crm_sms`：线索与机会管理、对话与邮件插件整合
  - `mass_mailing*`、`marketing_card`：邮件与活动营销
  - `link_tracker`、`utm`：链接与渠道追踪

- 销售与电商
  - `sale`、`sale_management`、`sale_stock`、`sale_project`、`sale_timesheet`、`sale_margin` 等：报价、订单、发货与扩展
  - `website_sale*`：电商前台与扩展（对接库存、忠诚度、心愿单、比较等）

- 采购与供应
  - `purchase`、`purchase_stock`、`purchase_requisition*`：采购单、补货与招标/询价流程

- 库存与物流
  - `stock`、`stock_account`、`stock_delivery`、`stock_picking_batch`、`stock_landed_costs`、`delivery*`：多仓库、拣货、会计对接、运费商整合

- 生产制造（MRP）
  - `mrp`、`mrp_subcontracting*`、`mrp_landed_costs`、`mrp_repair`、`mrp_product_expiry`：BOM、工单、委外、维修、成本与保质期

- 财务会计
  - `account`、`account_payment`、`account_edi*`、`account_peppol`、`account_qr_code_*`、`account_tax_python`：总账、支付、电子发票、税务与二维码
  - 大量本地化 `l10n_*`：各国会计科目、税务与 EDI 对接（如 `l10n_fr`、`l10n_es_edi_sii`、`l10n_it_edi`、`l10n_in_*` 等）

- 人力资源与考勤
  - `hr`、`hr_attendance`、`hr_contract`、`hr_holidays`、`hr_recruitment`、`hr_expense`、`hr_skills`、`hr_timesheet` 等：员工、合同、请假、招聘、费用、技能、工时

- 项目与协作
  - `project` 及其衍生（`project_timesheet_holidays`、`project_purchase`、`project_sale_expense` 等）：任务、看板、项目成本联动

- POS 零售场景
  - `point_of_sale` 及扩展（`pos_*`、`hw_*`）：门店收银、硬件驱动、在线支付、餐饮增强等

- 设备与维护
  - `maintenance`、`fleet`：设备资产、维护工单与车队管理

- 质量与售后（部分）
  - `repair`：维修流程；与 MRP/库存对接

- 支付网关
  - `payment_*`：Stripe、Adyen、PayPal、Razorpay、Mollie、Worldline、Xendit、Mercado Pago 等

- 其他常用模块
  - `calendar`、`contacts`、`survey`、`documents`（未在本仓库发现）等

> 说明：上述分组基于本仓库实际目录枚举（`Get-ChildItem addons`），并结合 Odoo 标准模块生态进行归纳。企业版（Enterprise）特性与专属模块不在本文范围内。

## 运行与部署要点

- 运行入口
  - 开发/本地：`python odoo-bin -c <配置文件>` 或 `python -m odoo`
  - 配置文件包含数据库连接、addons 路径、日志等（参考 `doc/odoo-configuration.md`）

- Addons 路径
  - 默认包含 `addons/` 与 `odoo/addons/`，可通过配置项 `addons_path` 扩展自定义模块目录。

- 依赖环境
  - 参考 `requirements.txt`；根据 Python 版本/平台使用不同的精确依赖。
  - 数据库使用 PostgreSQL；建议开启 `unaccent`、`pg_trgm` 等扩展以获得更好的搜索与匹配体验。

- 部署
  - 生产环境常见架构：Nginx/Apache + uWSGI/Gunicorn + Odoo；或基于 systemd/service 脚本（见 `debian/`）。
  - 静态资源与长连接（bus）需结合反向代理与缓存策略优化。

## 开发模型与模块结构（简要）

- 模块清单文件：`__manifest__.py`
  - 关键字段：`name`、`depends`、`data`、`assets`、`demo`、`installable` 等。

- 典型目录结构
  - `models/`：Python 模型与业务逻辑（继承 `models.Model`、`fields.*` 定义字段、`@api.*` 装饰器定义接口）
  - `views/`：XML 视图（表单、列表、看板、搜索、动作与菜单）
  - `security/`：访问控制（`ir.model.access.csv`）与记录规则（`ir.rule`）
  - `data/`：初始化与配置数据（序列、邮件模板、定时任务等）
  - `report/`：QWeb 报表模板与报表动作
  - `static/`：前端资源（JS/CSS/图片），assets 在 manifest 中声明
  - `controllers/`：HTTP 控制器（可提供前台或 API）
  - `i18n/`：翻译文件

- 继承与扩展
  - 业务扩展通过 `_inherit`、`_name`、`_inherits` 进行模型与视图继承；视图通过 XML `xpath`/`inherit_id` 嵌入。
  - 模块依赖通过 `depends` 管理；升级/迁移脚本可置于 `migrations/`。

## 测试与升级

- 单元与集成测试
  - 内核测试：`odoo/tests/`
  - 模块测试：`addons/test_*`、`odoo/addons/test_*`
  - 表单测试工具与基类：`odoo/tests/form.py`、`odoo/tests/common.py`

- 升级与迁移
  - 升级框架：`odoo/upgrade/` 与示例代码 `odoo/upgrade_code/`
  - 模块升级涉及数据迁移、视图调整与业务逻辑兼容；需结合 `module.py`、`migration.py` 的机制与钩子。

## 本仓库中值得关注的文件/目录

- `odoo/release.py`：版本信息（18.0）
- `odoo/tools/config.py`：配置项定义与解析
- `odoo/modules/module.py`：模块生命周期与加载
- `odoo/service/server.py`：服务器启动与主循环
- `odoo/http.py`：Web/HTTP/RPC 入口
- `addons/`：完整的社区模块生态（销售、采购、库存、会计、HR、MRP、POS、网站、电商、营销、支付、本地化等）
- `requirements.txt`：跨版本/平台的精准依赖矩阵

## 结语

本分析旨在从“代码-运行-业务”三条主线快速建立对 Odoo 18 代码库的整体认知：

- 代码：核心在 `odoo/`，模块在 `addons/`，两者通过模块加载器与注册表打通。
- 运行：`odoo-bin` + 配置文件 + PostgreSQL，HTTP/RPC 为外部接口，assets 驱动前端体验。
- 业务：围绕 ERP 核心域（销售/采购/库存/MRP/会计/HR/项目/POS/网站/营销/支付/本地化）模块化演进，低耦合可扩展。

如需进一步细化特定模块（例如只关注某行业域、或自定义模块的扩展点），可在本文件基础上追加“模块级深度解析”章节，选取目标模块逐层（manifest→models→views→security→controllers→report→assets→tests）展开。
