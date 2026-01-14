from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from parsers.main_parser import parse_report

app = FastAPI(title="Credit Report Parsing API", version="1.0")


@app.post("/v1/parse")
async def parse_html(html: str = Form(...)):
    try:
        data = parse_report(html)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/v1/parse-file")
async def parse_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".html", ".htm")):
        raise HTTPException(status_code=400, detail="Only HTML files are allowed")

    try:
        content = await file.read()
        html = content.decode("utf-8")
        data = parse_report(html)
        return {"success": True, "data": data}
    except UnicodeDecodeError:
        return {"success": False, "error": "Fayl UTF-8 formatida emas"}
    except Exception as e:
        return {"success": False, "error": str(e)}
