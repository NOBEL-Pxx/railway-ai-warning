// 适配 Vercel 部署的完整 app.js 代码
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const https = require('https');
const url = require('url');

const app = express();
// 关键：Vercel 自动分配端口，不再固定 3001
const PORT = process.env.PORT || 3001;

// ================= 配置区 =================
// 🔐 API Keys — 通过环境变量配置，切勿硬编码提交到GitHub
// 本地开发: 创建 .env 文件设置 DASHSCOPE_API_KEY 和 GAODE_API_KEY
// Vercel部署: 在项目 Settings → Environment Variables 中配置
const AI_API_KEY = process.env.DASHSCOPE_API_KEY || "";
const AI_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";

// 2. 天气配置 (高德地图)
const GAODE_KEY = process.env.GAODE_API_KEY || "";

// ================= 中间件 =================
app.use(cors()); // 允许跨域
app.use(express.json()); // 解析 JSON 请求体

// ================= 路由逻辑 =================
/**
 * 接口 1: AI 对话 (/api/chat)
 * 方法: POST
 * 逻辑: 转发请求给阿里云 DashScope (Qwen-Turbo)
 */
app.post('/api/chat', async (req, res) => {
    console.log(`🤖 [${new Date().toLocaleTimeString()}] 收到 AI 请求`);
    
    try {
        const { message } = req.body;

        if (!message) {
            return res.status(400).json({ success: false, reply: "请输入内容" });
        }

        const response = await axios.post(
            AI_API_URL,
            {
                model: "qwen-turbo",
                input: {
                    messages: [
                        { role: "system", content: "你是一个 helpful 的助手，专注于介绍兰州大学金鹰数字乡村项目。" },
                        { role: "user", content: message }
                    ]
                },
                parameters: {
                    temperature: 0.7
                }
            },
            {
                headers: {
                    "Authorization": `Bearer ${AI_API_KEY}`,
                    "Content-Type": "application/json"
                }
            }
        );

        // 兼容不同版本的返回结构
        const reply = response.data?.output?.text || response.data?.choices?.[0]?.message?.content || "AI 未返回有效内容";
        
        console.log(`✅ AI 回复成功`);
        res.json({ success: true, reply });

    } catch (err) {
        console.error("❌ 调用千问失败：", err.response?.data || err.message);
        
        let errorMsg = "AI暂时无法回答，请稍后再试";
        if (err.response?.status === 401) {
            errorMsg = "API Key 无效，请联系管理员检查后端配置。";
        } else if (err.code === 'ENOTFOUND') {
            errorMsg = "网络连接错误，无法访问 AI 服务。";
        }

        res.json({
            success: false,
            reply: errorMsg
        });
    }
});

/**
 * 接口 2: 天气查询 (/api/weather)
 * 方法: GET
 * 逻辑: 代理请求给高德地图 API
 */
app.get('/api/weather', (req, res) => {
    console.log(`🌤️ [${new Date().toLocaleTimeString()}] 收到天气请求`);

    const cityCode = req.query.city || '620123'; // 默认榆中县
    
    if (!GAODE_KEY) {
        return res.status(500).json({
            status: '0',
            info: '后端配置错误：请设置环境变量 GAODE_API_KEY'
        });
    }

    const gaodeUrl = `https://restapi.amap.com/v3/weather/weatherInfo?key=${GAODE_KEY}&city=${cityCode}&extensions=base`;

    https.get(gaodeUrl, (response) => {
        let data = '';
        
        response.on('data', chunk => {
            data += chunk;
        });

        response.on('end', () => {
            try {
                const jsonData = JSON.parse(data);
                // 直接透传高德的返回结果给前端
                res.status(response.statusCode).json(jsonData);
            } catch (e) {
                console.error('解析高德数据失败:', e);
                res.status(500).json({ error: '数据解析失败', detail: e.message });
            }
        });
    }).on('error', (err) => {
        console.error('请求高德服务器失败:', err.message);
        res.status(500).json({ error: '无法连接高德服务器', message: err.message });
    });
});

// ================= 启动服务 =================
app.listen(PORT, () => {
    console.log('------------------------------------------------');
    console.log(`🚀 综合后端服务已启动 (AI + 天气)`);
    console.log(`   监听端口: ${PORT}`);
    console.log(`   文件路径: ${__filename}`);
    console.log(`   AI 接口：http://localhost:${PORT}/api/chat (POST)`);
    console.log(`   天气接口: http://localhost:${PORT}/api/weather (GET)`);
    console.log('------------------------------------------------');
    console.log('💡 提示：请保持此窗口开启，不要关闭！');
});

// 关键：Vercel 必需的导出，否则部署后无法访问接口
module.exports = app;