from dataclasses import dataclass

@dataclass
class MethodPacket:
  is_success: bool = None
  message: str = None
  data = None
  
  def open_file(self, file_path) -> bool:
    pass
  
NOT_EXIST_FILE = "파일이 존재하지 않습니다."