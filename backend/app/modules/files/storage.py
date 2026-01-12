"""
File Storage Service
Handles file upload, storage, and retrieval
"""
import os
import shutil
from typing import Optional
from fastapi import UploadFile
from pathlib import Path

from app.core.config import settings
from app.utils.helpers import sanitize_filename, get_file_extension
from app.utils.exceptions import FileUploadException


class FileStorageService:
    """Service for file storage operations"""
    
    @staticmethod
    def validate_file(file: UploadFile, file_type: str = "document") -> bool:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file
            file_type: Type of file (image or document)
        
        Returns:
            True if valid
        
        Raises:
            FileUploadException: If validation fails
        """
        # Check file size
        max_size = settings.MAX_IMAGE_SIZE if file_type == "image" else settings.MAX_FILE_SIZE
        
        # Get file size (this is an approximation)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            raise FileUploadException(f"File size exceeds {max_mb}MB limit")
        
        # Check file type
        if file_type == "image":
            allowed_types = settings.allowed_image_types_list
        else:
            allowed_types = settings.allowed_document_types_list
        
        if file.content_type not in allowed_types:
            raise FileUploadException(f"File type {file.content_type} not allowed")
        
        return True
    
    @staticmethod
    async def save_file(
        file: UploadFile,
        subfolder: str = "documents",
        file_type: str = "document"
    ) -> str:
        """
        Save uploaded file to storage
        
        Args:
            file: Uploaded file
            subfolder: Subfolder to save file in
            file_type: Type of file (image or document)
        
        Returns:
            File URL/path
        
        Raises:
            FileUploadException: If save fails
        """
        try:
            # Validate file
            FileStorageService.validate_file(file, file_type)
            
            # Sanitize filename
            safe_filename = sanitize_filename(file.filename)
            
            # Create full path
            upload_dir = Path(settings.UPLOAD_DIR) / subfolder
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = upload_dir / safe_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Return relative URL
            return f"/uploads/{subfolder}/{safe_filename}"
            
        except Exception as e:
            raise FileUploadException(f"Failed to save file: {str(e)}")
    
    @staticmethod
    def delete_file(file_url: str) -> bool:
        """
        Delete file from storage
        
        Args:
            file_url: File URL to delete
        
        Returns:
            True if deleted successfully
        """
        try:
            # Extract path from URL
            if file_url.startswith("/uploads/"):
                file_path = Path(settings.UPLOAD_DIR) / file_url.replace("/uploads/", "")
                
                if file_path.exists():
                    file_path.unlink()
                    return True
            
            return False
            
        except Exception:
            return False
    
    @staticmethod
    async def save_logo(file: UploadFile) -> str:
        """Save laboratory logo"""
        return await FileStorageService.save_file(file, "logos", "image")
    
    @staticmethod
    async def save_document(file: UploadFile, doc_type: str = "general") -> str:
        """Save document file"""
        return await FileStorageService.save_file(file, f"documents/{doc_type}", "document")
