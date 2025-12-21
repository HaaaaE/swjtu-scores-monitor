[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FHaaaaE%2Fswjtu-score-monitor&env=SWJTU_USERNAME,EMAIL_PASSWORD,SMTP_HOST,NOTIFY_EMAIL,EMAIL_PASSWORD,UPSTASH_REDIS_REST_URL,UPSTASH_REDIS_REST_TOKEN,API_SECRET_TOKEN&project-name=swjtu-score-monitor&repository-name=swjtu-score-monitor)

```
SWJTU_USERNAME=
SWJTU_PASSWORD=
SMTP_HOST=
NOTIFY_EMAIL=
EMAIL_PASSWORD=
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
API_SECRET_TOKEN=
```

# 西南交大成绩监控系统部署教程

## 一、项目简介

本项目可以自动监控西南交通大学教务系统的成绩变化，当检测到新成绩或成绩更新时，会通过邮件发送通知。

**GitHub Actions 部署方案的优势：**
- 🆓 完全免费，利用 GitHub 免费额度
- ☁️ 无需自己的服务器
- ⏰ 自动定时运行（北京时间 6:00-23:59，每20分钟检查一次）
- 🔒 隐私安全，敏感信息加密存储
- 📧 成绩变化时自动邮件通知

---

## 二、隐私与安全说明 ✅

### 为什么本项目是安全的？

1. **所有敏感信息都存储在 GitHub Secrets 中**
   - 学号、密码、邮箱授权码等信息不会出现在代码中
   - GitHub Secrets 使用加密存储，外部无法访问
   - 运行日志中 Secrets 会被自动隐藏（显示为 `***`）

2. **即使仓库公开也安全**
   - Fork 后的仓库可以是公开的，不影响安全性
   - 代码中不包含任何密码或敏感信息
   - 只有你能在自己的仓库中配置 Secrets

3. **数据存储方式**
   - 成绩数据存储在你自己的 GitHub Gist 中（私有）
   - 只有你的 Personal Access Token 能访问

### ⚠️ 安全使用原则

- ✅ **永远不要**把密码直接写在代码文件中
- ✅ **永远使用** GitHub Secrets 来存储敏感信息
- ✅ 不要将 Secrets 的值分享给他人

---

## 三、前置准备

### 3.1 你需要准备

1. **你的 GitHub 账号**
2. **西南交大教务系统账号密码**
3. **一个邮箱**（推荐使用QQ邮箱，可以绑定微信收取实时通知。通过自己给自己发邮件，实现发送和接收成绩通知）

### 3.2 获取每个 Secret（密钥）

#### ① SWJTU_USERNAME 和 SWJTU_PASSWORD

- `SWJTU_USERNAME`：你的教务系统**学号**
- `SWJTU_PASSWORD`：你的教务系统**密码**

#### ② SMTP_HOST、NOTIFY_EMAIL 和 EMAIL_PASSWORD

这三个配置用于发送邮件通知，以下是QQ邮箱的配置方法：

1. **SMTP_HOST**：`smtp.qq.com`
2. **NOTIFY_EMAIL**：你的 QQ 邮箱地址（如 `12345678@qq.com`）
3. **EMAIL_PASSWORD**：需要获取**授权码**（不是QQ密码）

**如何获取 QQ 邮箱授权码：**

1. 登录 QQ 邮箱网页版：https://mail.qq.com
2. 进入「账号与安全」
3. 进入「安全设置」
4. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」并开启
5. 点击「生成授权码」
6. 获得一个 16 位授权码（如：`abcdabcdabcdabcd`）
7. 这个授权码就是 EMAIL_PASSWORD 的值，**该字符串仅在授权码页面展示一次，请合理保存**
8. 途中可能经过三次手机号验证，这是正常的

---

#### ③ GIST_PAT（GitHub Personal Access Token）

**这是什么？**

GitHub Personal Access Token（个人访问令牌）是用来授权程序访问你的 GitHub Gist 的凭证。本项目使用 Gist 来存储你的成绩数据。

**如何创建 GIST_PAT：**

1. **登录 GitHub**，点击右上角头像

2. **进入 Settings**
   - 点击下拉菜单中的「Settings」

3. **找到 Developer settings**
   - 在左侧菜单最底部点击「Developer settings」

4. **创建 Personal access tokens**
   - 点击左侧「Personal access tokens」→「Tokens (classic)」
   - 点击右上角「Generate new token」→「Generate new token (classic)」

5. **配置 Token**
   - **Note**（备注）：填写一个描述，如 `swjtu-scores-monitor`
   - **Expiration**（有效期）：建议选择「No expiration」（永不过期）或「1 year」
   - **Select scopes**（权限选择）：**只勾选 `gist`**
     ```
     ☑️ gist
         Create gists
     ```
   - 其他权限都不要勾选！

6. **生成并保存**
   - 点击底部「Generate token」
   - 复制生成的 Token（格式如：`ghp_xxxxxxxxxxxxxxxxxxxx`）
   - **重要：这个 Token 也只会显示一次，请立即复制保存**
   - 这个 Token 就是 `GIST_PAT` 的值

---

## 四、部署步骤

### 步骤 1：Fork 本项目

1. 在项目主页点击右上角「Fork」按钮
2. Fork 到你自己的账号下
3. 仓库可以保持公开（Public）或设为私有（Private），都不影响安全性

### 步骤 2：配置 GitHub Secrets

1. **进入你 Fork 的仓库**

2. **打开 Settings**
   - 点击仓库顶部的「Settings」标签

3. **进入 Secrets 配置页面**
   - 在左侧菜单中找到「Secrets and variables」
   - 点击「Actions」

4. **添加 Secrets**
   - 点击绿色「New repository secret」按钮
   - 添加以下 6 个 Secrets：

| Name | Secret | 说明 |
|------|-------|------|
| `SWJTU_USERNAME` | 你的学号 | 教务系统登录学号 |
| `SWJTU_PASSWORD` | 你的密码 | 教务系统登录密码 |
| `SMTP_HOST` | smtp.qq.com | 邮箱 SMTP 服务器地址 |
| `NOTIFY_EMAIL` | your@qq.com | 接收通知的邮箱 |
| `EMAIL_PASSWORD` | 授权码 | 邮箱授权码（不是邮箱密码） |
| `GIST_PAT` | ghp_xxx... | GitHub Personal Access Token |

**添加方式：**
- 在「Name」输入框填入 Secret 名称（如 `SWJTU_USERNAME`）
- 在「Secret」输入框填入对应的值
- 点击「Add secret」
- 重复以上步骤添加所有 6 个 Secrets

### 步骤 3：启用 GitHub Actions

1. **进入 Actions 页面**
   - 点击仓库顶部的「Actions」标签

2. **启用 Workflows**
   - 如果看到提示「Workflows aren't being run on this forked repository」
   - 点击「I understand my workflows, go ahead and enable them」

3. **确认 Monitor Scores 工作流已启用**
   - 在左侧列表中找到「Monitor Scores」
   - 确保它处于启用状态
   - （别的workflow我用作测试，不用管）

### 步骤 4：手动测试运行

1. **在 Actions 页面**，点击左侧的「Monitor Scores」

2. **手动触发运行**
   - 点击右上角「Run workflow」下拉按钮
   - 点击「Run workflow」确认

3. **查看运行结果**
   - 等待几分钟，workflow 会开始运行
   - 点击正在运行的任务查看实时日志
   - 如果配置正确，应该能看到：
     ```
     --- 任务开始: 监控成绩变化 ---
     正在从数据库获取历史成绩...
     正在登录教务系统获取最新成绩...
     --- 登录尝试 #1/5 ---
     正在获取验证码...
     OCR 识别结果: xxxx
     正在尝试登录API...
     API验证成功！
     ...
     ```
   - **该运行结果也只有你可见**

4. **检查邮箱**
   - 如果是首次运行或有成绩变化，你会收到邮件通知

---

## 五、monitor.yml 工作原理

### 运行时间

```yaml
schedule:
  - cron: '*/20 0-15,22-23 * * *'
```

- **北京时间**：6:00 - 23:59，每 20 分钟运行一次，由于github actions的调度等原因，时间并非决定精准（可能会偏移多达15分钟，不影响使用）
- **UTC时间**：22:00 - 15:59（GitHub Actions 使用 UTC 时间）
- 北京时间 00:00 - 5:59 教务处暂停外部访问，故不运行

### 工作流程

1. **检出代码**：获取最新的项目代码
2. **安装依赖**：使用 uv 安装 Python 依赖
3. **运行监控脚本**：
   - 从 GitHub Gist 读取上次保存的成绩
   - 登录教务系统获取最新成绩
   - 对比新旧成绩，检测变化
   - 如果有变化，发送邮件通知
   - 将最新成绩保存到 Gist

### 检测的变化类型

- ✅ 新增课程成绩
- ✅ 成绩分数变化
- ✅ 新增平时成绩
- ✅ 平时成绩变化

---

## 六、使用与维护

### 如何查看运行日志

1. 进入仓库的「Actions」页面
2. 点击任意一次运行记录
3. 点击「run-job」查看详细日志
4. 可以看到登录过程、成绩获取、变化检测等详细信息

### 如何手动触发监控

1. 进入「Actions」→「Monitor Scores」
2. 点击「Run workflow」
3. 点击「Run workflow」确认
4. 适合测试或立即检查成绩

### 如何修改监控频率

编辑 monitor.yml 文件，修改 cron 表达式：

```yaml
schedule:
  # 改为每10分钟运行一次（白天时段）
  - cron: '*/10 0-15,22-23 * * *'
  
  # 或改为每小时运行一次
  - cron: '0 0-15,22-23 * * *'
```

**注意**：
- GitHub Actions 免费账户私有仓库每月有 2000 分钟的运行时间，公开仓库不限制。
- 单次运行约 30s
- 过于频繁可能被教务系统限制访问

### 如何暂停监控

1. 进入「Actions」→「Monitor Scores」
2. 点击右上角「...」菜单
3. 选择「Disable workflow」

### 如何恢复监控

重新启用 workflow 即可


---

## 七、常见问题

### Q1：登录失败怎么办？

**可能原因：**
1. 学号或密码错误
   - 检查 `SWJTU_USERNAME` 和 `SWJTU_PASSWORD` 是否正确
   
2. 教务系统维护或关闭外网访问
   - 查看运行日志，如果多次重试都失败
   - 尝试在浏览器手动登录教务系统确认
   
3. 验证码识别失败
   - 项目使用 OCR 自动识别验证码
   - 最多重试 5 次，偶尔失败是正常的
   - 如果持续失败，等待下次自动运行

### Q2：收不到邮件通知？

**检查清单：**

1. **Secrets 配置是否正确**
   - 确认 `SMTP_HOST`、`NOTIFY_EMAIL`、`EMAIL_PASSWORD` 都已配置
   - 确认 `EMAIL_PASSWORD` 使用的是授权码，不是登录密码

2. **检查垃圾邮件箱**
   - 第一次接收时可能被识别为垃圾邮件

3. **查看运行日志**
   - 进入 Actions 查看详细日志
   - 搜索「邮件」或「SMTP」相关错误信息

4. **SMTP 服务是否开启**
   - 确认邮箱已开启 SMTP 服务
   - QQ 邮箱：设置 → 账户 → POP3/SMTP 服务

5. **端口问题**
   - 项目默认使用 465 端口
   - 如需修改，可在 Secrets 中添加 `SMTP_PORT`

### Q3：如何查看当前存储的成绩数据？

1. 访问你的 GitHub Gists：https://gist.github.com/你的用户名
2. 找到描述为 `just_for_swjtu_scores_monitor` 的 Gist
3. 文件名为 `scores.json`
4. 点击查看即可看到存储的成绩 JSON 数据

### Q4：GitHub Actions 免费额度够用吗？

**免费账户限制：**
- 每月 2000 分钟运行时间
- 公开仓库不消耗额度
- 私有仓库消耗额度

**本项目消耗：**
- 单次运行约 30s
- 每天运行约 54 次（20分钟间隔，18小时）
- 每月约 54 × 30 × 0.5 = 810 分钟

**建议：**
- 保持仓库为公开（Public）→ 不消耗额度

### Q5：为什么有时候运行失败？

**正常情况：**
- 验证码识别失败：会自动重试 5 次
- 教务系统临时无法访问：下次运行会自动恢复
- GitHub Actions 服务波动：偶尔发生

**不影响使用：**
- 只要不是连续多次失败，都属于正常现象
- 20 分钟后会自动重新运行

### Q6：如何更新项目代码？

如果原项目有更新，同步到你的 Fork：

1. 在你的仓库页面，点击「Sync fork」
2. 点击「Update branch」
3. Secrets 配置会保留，无需重新配置

### Q7：可以监控多个账号吗？

当前版本只支持单账号。如需监控多个账号：

1. 再次 Fork 项目（使用不同的仓库名）
2. 为每个仓库配置不同的 Secrets
3. 每个仓库独立运行

---

## 八、技术说明

### 使用的技术栈

- **Python 3.12**：主要编程语言
- **uv**：快速的 Python 包管理器
- **requests + BeautifulSoup**：网页抓取
- **OCR 验证码识别**：自动识别登录验证码
- **GitHub Gist**：数据存储
- **SMTP**：邮件发送

### 项目结构

```
.github/workflows/
  └── monitor.yml          # GitHub Actions 工作流配置
actions/
  └── index.py             # 主要业务逻辑
utils/
  ├── fetcher.py          # 教务系统爬虫
  ├── database.py         # Gist 数据存储
  ├── notify.py           # 邮件通知
  └── ocr.py              # 验证码识别
```

---

## 九、致谢与支持

如果这个项目对你有帮助，欢迎：

- ⭐ Star 本项目
- 🐛 提交 Issue 反馈问题
- 🔀 提交 Pull Request 改进项目
