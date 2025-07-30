# 이미지 전처리
from fastapi import UploadFile, HTTPException
from typing import BinaryIO
import imghdr

ALLOWED_IMAGE_TYPES = {"jpeg", "png", "jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_image(file: UploadFile) -> bool:
    """이미지 파일 유효성 검사"""
    
    # 파일 크기 확인
    contents = await file.read()
    await file.seek(0)  # 파일 포인터를 처음으로 되돌림
    
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"파일 크기가 너무 큽니다. 최대 {MAX_FILE_SIZE // (1024*1024)}MB까지 가능합니다."
        )
    
    # 파일 형식 확인
    image_type = imghdr.what(None, contents)
    if image_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 이미지 형식입니다. 지원 형식: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    print("image_processing")
    return True