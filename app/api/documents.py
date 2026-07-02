from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import document_service
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    content = await file.read()

    # 解析
    try:
        if file.filename.endswith('.pdf'):
            text = document_service.parse_pdf(content)
        elif file.filename.endswith('.docx'):
            text = document_service.parse_docx(content)
        elif file.filename.endswith('.txt'):
            text = document_service.parse_txt(content)
        else:
            raise HTTPException(status_code=400, detail="仅支持 PDF, DOCX, TXT")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")

    # 入库
    chunk_count = rag_service.add_document(text)

    return {
        "filename": file.filename,
        "status": "success",
        "chunks_added": chunk_count
    }


@router.get("/list")
async def list_documents():
    return {"total_chunks": len(rag_service.chunks)}