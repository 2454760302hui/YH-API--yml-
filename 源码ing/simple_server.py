#!/usr/bin/env python3
"""
简化的服务器测试编码修复
"""

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse, JSONResponse
    import uvicorn
    
    app = FastAPI(title="YH API测试框架", version="2.0.0")
    
    # 强制设置OpenAPI版本为3.0.2
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        from fastapi.openapi.utils import get_openapi
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description="测试编码修复",
            routes=app.routes,
        )
        openapi_schema["openapi"] = "3.0.2"
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "message": "编码修复成功"}
    
    @app.get("/")
    async def home():
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>YH API测试框架</title></head>
        <body>
            <h1>🎉 编码修复成功！</h1>
            <p>服务器正常运行</p>
            <p><a href="/docs">查看API文档</a></p>
        </body>
        </html>
        """)
    
    if __name__ == "__main__":
        print("启动简化服务器测试编码修复...")
        uvicorn.run(app, host="127.0.0.1", port=8091)
        
except ImportError as e:
    print(f"模块导入失败: {e}")
    print("请安装: pip install fastapi uvicorn")
except Exception as e:
    print(f"启动失败: {e}")
