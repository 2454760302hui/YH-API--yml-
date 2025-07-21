#!/usr/bin/env python3
"""
测试Swagger UI显示问题
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI(
    title="YH API测试框架",
    description="测试Swagger UI显示",
    version="2.0.0",
)

# 强制设置OpenAPI版本为3.0.2
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.2"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "测试Swagger UI"}

@app.get("/test")
async def test_endpoint():
    """测试端点"""
    return {"message": "这是一个测试端点"}

@app.get("/docs", response_class=HTMLResponse)
async def custom_swagger_ui_html():
    """简化的Swagger UI文档页面"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>YH API测试框架 - API文档</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <style>
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
        .header { background: #667eea; color: white; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
        #swagger-ui { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 YH API测试框架 - API文档</h1>
        <p>测试Swagger UI显示</p>
    </div>
    <div id="swagger-ui"></div>

    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            console.log('开始初始化Swagger UI...');
            
            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                onComplete: function() {
                    console.log('Swagger UI 初始化完成');
                },
                onFailure: function(error) {
                    console.error('Swagger UI 初始化失败:', error);
                }
            });
            
            console.log('Swagger UI 配置完成');
        };
        
        // 检查资源加载
        window.addEventListener('error', function(e) {
            console.error('资源加载错误:', e.target.src || e.target.href, e.message);
        });
    </script>
</body>
</html>
    """

if __name__ == "__main__":
    print("启动简化的Swagger UI测试服务器...")
    uvicorn.run(app, host="127.0.0.1", port=8094, log_level="info")
