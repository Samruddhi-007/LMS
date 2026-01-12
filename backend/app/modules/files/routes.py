"""
File Upload API Routes
Endpoints for file upload and management
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List

from app.modules.files.storage import FileStorageService

router = APIRouter()


@router.post("/upload/logo")
async def upload_logo(file: UploadFile = File(...)):
    """
    Upload laboratory logo
    
    - **file**: Image file (JPG/PNG, max 1MB)
    """
    try:
        file_url = await FileStorageService.save_logo(file)
        return {
            "success": True,
            "file_url": file_url,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/upload/document")
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = "general"
):
    """
    Upload document file
    
    - **file**: PDF file (max 2MB)
    - **doc_type**: Type of document (general, compliance, policy, etc.)
    """
    try:
        file_url = await FileStorageService.save_document(file, doc_type)
        return {
            "success": True,
            "file_url": file_url,
            "filename": file.filename,
            "doc_type": doc_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/upload/multiple")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    doc_type: str = "general"
):
    """
    Upload multiple document files
    
    - **files**: List of PDF files (max 2MB each)
    - **doc_type**: Type of documents
    """
    try:
        uploaded_files = []
        
        for file in files:
            file_url = await FileStorageService.save_document(file, doc_type)
            uploaded_files.append({
                "file_url": file_url,
                "filename": file.filename
            })
        
        return {
            "success": True,
            "files": uploaded_files,
            "count": len(uploaded_files)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/delete")
async def delete_file(file_url: str):
    """
    Delete a file
    
    - **file_url**: URL of the file to delete
    """
    success = FileStorageService.delete_file(file_url)
    
    if success:
        return {
            "success": True,
            "message": "File deleted successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
