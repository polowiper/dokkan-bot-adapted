from pathlib import Path

from orator import DatabaseManager

class GamePlatform:
  def __init__(
    self,
    name: str,
    user_agent: str,
    device_name: str,
    device_model: str,
    os_version: str
  ):
    self.name = name
    self.user_agent = user_agent
    self.device_name = device_name
    self.device_model = device_model
    self.os_version = os_version

class GameEnvironment:
  def __init__(
    self,
    name: str,
    url: str,
    port: int,
    version_code: str,
    db_path: Path,
    db_password: bytearray
  ):
    self.name = name
    self.url = url
    self.port = port
    self.version_code = version_code
    self.db_path = db_path
    self.db_password = db_password
    self.db_manager = DatabaseManager({
      'mysql': {
        'driver': 'sqlite',
        'database': db_path
      }
    })