import logging
import uuid
from pathlib import Path

from app.config import UPLOAD_DIR

logger = logging.getLogger(__name__)


class ImageStorageService:
    def __init__(self, storage_dir: Path = UPLOAD_DIR):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(exist_ok=True)
    
    def generate_image_id(self) -> str:
        return str(uuid.uuid4())[:12]  
    
    def save_image(self, image_id: str, contents: bytes, extension: str) -> Path:
        filename = f"{image_id}{extension}"
        filepath = self.storage_dir / filename
        
        filepath.write_bytes(contents)
        logger.info(f"Image saved: {filename} ({len(contents)} bytes)")
        
        return filepath
    
    def get_image_path(self, image_id: str) -> Path | None:
        for extension in [".jpg", ".jpeg", ".png"]:
            filepath = self.storage_dir / f"{image_id}{extension}"
            if filepath.exists():
                return filepath
        
        return None
    
    def image_exists(self, image_id: str) -> bool:
        return self.get_image_path(image_id) is not None
    
    def get_image_info(self, image_id: str) -> dict | None:
        filepath = self.get_image_path(image_id)
        
        if filepath is None:
            return None
        
        stat = filepath.stat()
        return {
            "image_id": image_id,
            "filename": filepath.name,
            "size_bytes": stat.st_size,
            "extension": filepath.suffix,
            "created_at": stat.st_ctime
        }


storage_service = ImageStorageService()