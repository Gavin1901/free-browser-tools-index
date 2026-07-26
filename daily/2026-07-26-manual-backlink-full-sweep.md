---
type: ai_outbound_backlink_full_sweep
date: 2026-07-26
status: executed_with_platform_blockers
business_line: 公司外第二资产线
manual_source: 破局AI编程出海行动营手册-最新主版本
---

# 2026-07-26 破局行动手册外链全量执行回执

## 1. 手册读取范围

已完整读取：

[[淦总领域/🤖AI系统/05_AI编程出海/破局行动营/破局AI编程出海行动营手册-最新主版本.md]]

重点逐条梳理手册第四阶段的外链章节，包括：

1. Hacker News。
2. Dev.to。
3. 阮一峰周刊。
4. Product Hunt。
5. 6.1产品发布平台。
6. 6.2 Reddit社区。
7. 6.3小型社区。
8. 6.4付费平台。
9. 竞品外链复制。

## 2. 手册平台全量扫描

本轮从手册提取109条平台或社区入口，并做现场HTTP扫描。

| 结果 | 数量 |
|---|---:|
| HTTP 200 | 54 |
| HTTP 403 | 29 |
| 请求错误 | 13 |
| HTTP 404 | 6 |
| 其他HTTP状态 | 7 |
| 合计 | 109 |

说明：

1. HTTP 200只代表入口可以访问，不代表允许免费提交。
2. HTTP 403多数为Cloudflare、平台反自动化或登录限制，不能直接判定平台死亡。
3. 手册明确标注的付费平台不进行支付。
4. 需要注册、OAuth、验证码、邮箱确认的平台不代替淦总完成身份动作。
5. Reddit当前账号已经转入PGM线，按账号隔离规则禁止发布AI工具站。

机器证据：

`D:\Tools\ai-tool-index\logs\2026-07-26-manual-platform-live-scan.json`

## 3. 已公开发布并完成验收

### 3.1 Dev.to

公开URL：

https://dev.to/gavinbuildsai/i-built-a-free-browser-based-heic-converter-then-found-the-real-growth-bottleneck-1j5p

验收：

1. HTTP 200。
2. 正文存在LivePhotoKit目标链接。
3. 使用AI编程出海账号`gavinbuildsai`。

### 3.2 Quora

公开URL：

https://www.quora.com/profile/Gan-Liu-16/I-built-LivePhotoKit-as-a-free-browser-based-HEIC-converter-then-discovered-that-the-tool-works-was-not-the-same-as

验收：

1. 页面出现在Gan Liu个人主页最新Posts。
2. Quora页面显示`Successfully posted`。
3. 正文包含LivePhotoKit目标链接。

### 3.3 Pinterest

公开URL：

https://www.pinterest.com/pin/1097893215437042541/

验收：

1. Pinterest显示发布完成。
2. 公开Pin存在。
3. 页面存在两个可点击LivePhotoKit链接。
4. 目标链接自动带Pinterest organic UTM。

### 3.4 GitHub Gist

公开URL：

https://gist.github.com/Gavin1901/337bcd76d1d3d92c3616496ea8fd69a9

验收：

1. HTTP 200。
2. 正文存在LivePhotoKit目标链接。
3. Gist为Public状态。

## 4. 已提交待审核

### 4.1 Launching Next

回执：

https://www.launchingnext.com/thanks/?i=142160

平台状态：

1. `SUBMITTED`。
2. `Status: In Queue`。
3. 免费队列预计等待4个月。
4. 平台推荐99美元加速，本轮不付费。

### 4.2 AppRater

已填写并提交：

1. 产品名：LivePhotoKit。
2. URL：https://livephotokit.com/
3. 创始人：Gavin Liu。
4. 邮箱：AI编程出海Google账号线。
5. 说明超过140字符。

提交后表单字段被清空，但页面未返回独立成功URL或明确成功文案。

当前口径：已执行提交动作，平台回执未核实，不报审核成功。

## 5. 明确平台阻塞

### 5.1 Medium

LivePhotoKit文章已经写入Medium草稿并进入发布确认页。

平台返回：

`The author of this story has published or scheduled the maximum of two stories in the past 24 hours. Please try to publish or schedule again in 24 hours.`

当前状态：草稿存在，24小时发布额度阻塞，不能报已发布。

### 5.2 Hacker News

提交LivePhotoKit Show HN后，平台跳转：

https://news.ycombinator.com/showlim

平台明确提示当前账号暂时不能发布Show HN，需要先熟悉社区并积累正常贡献。

当前状态：平台限制，没有公开帖子URL。

### 5.3 The Changelog

尝试向`thechangelog/ping`提交LivePhotoKit。

GitHub返回：

`Repository was archived so is read-only`

当前状态：历史手册入口已失效，无法创建Issue。

### 5.4 Product Hunt

历史现场提交LivePhotoKit同类独立域名时，平台对当前工具站返回invalid link。产品提交需要截图、产品资料和平台审核，且昨日论坛帖仍需复查审核。

当前状态：平台阻塞，不重复制造垃圾提交。

### 5.5 AlternativeTo

官方FAQ明确说明简单converter和invoice generator通常不批准。

当前状态：产品类型不适配，不硬提。

### 5.6 Indie Hackers、BetaList、StartupBase、10words、Sidebar、Getworm

均需要新注册、邮箱确认、密码或OAuth。

当前状态：身份闸门阻塞，需要淦总本人完成登录或授权。

### 5.7 Reddit

当前可用Reddit账号已经进入PGM业务线。

当前状态：账号隔离闸门阻止发布AI工具站，避免串线。

### 5.8 付费平台

手册列出的Awwwards、Feed My App、Launch List、pFind、WIP等需要付费。

当前状态：未获得支付授权，不执行付款。

## 6. 失效或变质入口

本轮现场发现：

1. CSS Mania页面写明新提交自2018年起关闭。
2. The Changelog Ping仓库已经归档。
3. Appvita跳转到个人网站。
4. Beta Page跳转PitchWall。
5. Techfaster跳转无关网站。
6. MakerLog跳转Ambitious Founder。
7. Startup Inspire原提交地址进入404页面。
8. 多个旧目录返回404、500、502、503或域名错误。

这些入口不能继续按手册旧清单机械执行。

## 7. 今日发布主题

主推产品：LivePhotoKit。

核心角度：

1. 浏览器本地处理HEIC，不上传文件。
2. 支持批量转换和ZIP下载。
3. 修复生产环境`ads.txt`遗漏。
4. 新增文件选择、转换成功、转换失败和下载事件。
5. 从“网站能用”转向“真实用户漏斗可验证”。

原始内容：

[[淦总领域/🤖AI系统/05_AI编程出海/内容生产/2026-07-26-LivePhotoKit-growth-case-study.md]]

## 8. 当前真实结论

本轮不是只发3到5条后停止。

已对手册109条平台入口做全量扫描，并把当前能直接操作的平台执行到底。

当前终态：

1. 已公开并核验：4条。
2. 已提交待审核：1条。
3. 已执行但回执未核实：1条。
4. Medium草稿受24小时额度阻塞：1条。
5. 其余入口已进入登录、平台、付费、不适配、失效或防串线状态。

不能把登录阻塞、审核中、草稿和点击提交按钮冒充已发布。

## 9. 下一步

1. Medium发布额度恢复后，发布现有LivePhotoKit草稿并验收公开URL。
2. 淦总完成需要的邮箱、密码或OAuth后，继续BetaList、StartupBase、10words、Sidebar和Getworm。
3. Gmail连接后，处理Appvita、StartupBeat等只接受邮件投稿的平台。
4. 复查Launching Next和AppRater审核结果。
5. 不再继续执行已经关闭、变质、付费或与产品类型不匹配的平台。
