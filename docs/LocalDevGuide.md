# Local Dev Guide — Pour Decisions

## 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt
```

依赖清单：`streamlit>=1.28.0`、`openai`、`python-dotenv`

---

## 2. 配置 API Key

复制模板文件，填入真实 key：

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

打开 `.streamlit/secrets.toml`，填写：

```toml
MINIMAX_API_KEY = "你的 Minimax API Key"
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"
```

> `secrets.toml` 已在 `.gitignore` 中，不会被提交。

---

## 3. 启动应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。侧边栏列出所有页面。

---

## 4. 功能检查清单

### 页面 01 — Home（食材匹配 + AI 推荐）

**食材匹配流程：**
1. 从下拉框选择 1-2 个食材（如 `vodka`、`lime juice`）
2. 点击 **Find matching cocktails**
3. 应跳转到 Results 页，显示精确匹配和部分匹配，partial match 标注缺少的食材

**边界情况：**
- 不选任何食材直接提交 → 应显示 warning，不跳转
- 在「Add custom ingredients」输入框输入 `ginger beer, mint` → 应与多选框的食材合并后搜索

**AI 推荐流程：**
1. 在「Describe your mood」输入 `something citrusy and refreshing`
2. 点击 **Get AI suggestions**
3. 等待 spinner，应跳转 Results 页显示 3-5 条推荐，每条带 why 字段
4. 回到 Home 再次提交**相同** prompt → 应直接跳转（命中缓存，无 spinner）

**边界情况：**
- 空 prompt 提交 → warning，不跳转
- 无效 API Key 或断网 → Results 页显示 fallback 提示，不崩溃

---

### 页面 02 — Browse（浏览 + 搜索筛选）

1. 打开页面，应显示全部 16 条食谱，3 列网格布局
2. 搜索框输入 `mar` → 结果实时缩减（含 Margarita）
3. Base spirit 筛选选 `gin` → 只显示 gin 类食谱
4. 同时选 Base spirit = `rum` + Difficulty = `hard` → 交叉过滤，只剩 Mai Tai
5. 点击 **Clear filters** → 恢复全部 16 条
6. 无匹配时 → 显示友好提示，不显示空白

**导航：**
- 点击任意食谱卡片的 **View details** → 跳转 Recipe Detail 页，且食谱已预填

---

### 页面 03 — Results（匹配结果）

- 从 Home 跳转过来后，精确匹配排在前面，部分匹配在后
- 精确匹配应显示绿色「You have everything needed」
- 部分匹配显示缺少的食材列表
- AI 推荐区块只在有 AI 结果时出现
- 直接访问 Results（未经 Home）→ 显示引导提示

---

### 页面 04 — Recipe Detail（配方详情 + 缩放）

1. 顶部下拉框可切换食谱
2. Serving size 选 `x2` → 所有食材用量应翻倍，`0.75 oz` 变为 `1 1/2 oz`
3. `null` 用量（如 salt to taste）→ 不变，显示「to taste」
4. 点击 **Start Mixing** → 跳转 Mix 页，serving size 保持同步

---

### 页面 05 — Mix（逐步调酒）

1. 从 Recipe Detail 点 Start Mixing 进入
2. 每次点 **Next Step** 前进一步，progress bar 同步更新
3. **Start Over** → 回到第 1 步
4. 走完全部步骤 → 显示完成提示，Start Over 可用
5. 直接访问 Mix 页（未选食谱）→ 显示引导提示 + 跳转按钮，不崩溃

---

## 5. 常见问题

| 症状 | 原因 | 解决 |
|---|---|---|
| `ModuleNotFoundError: openai` | 依赖未安装 | `pip install -r requirements.txt` |
| AI 推荐返回空结果 | API Key 未填或填错 | 检查 `.streamlit/secrets.toml` |
| 页面间跳转失败 | Streamlit 版本过低 | 确认 `streamlit>=1.28.0`（`st.switch_page` 需要此版本） |
| 食谱数据不显示 | 工作目录不对 | 必须在项目根目录执行 `streamlit run app.py` |
