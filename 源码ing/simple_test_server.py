#!/usr/bin/env python3
"""
简单的测试服务器
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

# 创建FastAPI应用
app = FastAPI(
    title="YH API测试框架",
    description="测试OpenAPI版本修复",
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
    # 强制设置为OpenAPI 3.0.2
    openapi_schema["openapi"] = "3.0.2"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "framework": "YH API测试框架"}

@app.get("/")
async def home():
    """主页"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>YH API测试框架</title>
    </head>
    <body>
        <h1>YH API测试框架</h1>
        <p><a href="/docs">查看API文档</a></p>
        <p><a href="/health">健康检查</a></p>
    </body>
    </html>
    """)

@app.post("/api/execute")
async def execute_api(
    method: str,
    url: str,
    headers: dict = None,
    params: dict = None,
    json_data: dict = None
):
    """执行API测试"""
    return {
        "success": True,
        "message": "API测试执行成功",
        "request": {
            "method": method,
            "url": url,
            "headers": headers or {},
            "params": params or {},
            "json_data": json_data or {}
        }
    }

if __name__ == "__main__":
    print("启动简单测试服务器...")
    print("OpenAPI版本将被设置为3.0.2")
    uvicorn.run(app, host="127.0.0.1", port=8085, log_level="info")
