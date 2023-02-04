from ted.model.singleton_base import SingletonBase
from ted.model.packet_base import MethodPacket
import os

class DataManager(SingletonBase):
  _current_file_name = None
  _current_data = None
  _current_data_type = None
  
  def load_data(self, file_name) -> bool:
    packet = MethodPacket(
      is_success=False,
      message="실패"
    )
    if not os.path.exists(file_name):
      packet.message = "파일이 존재하지 않습니다."
      return packet