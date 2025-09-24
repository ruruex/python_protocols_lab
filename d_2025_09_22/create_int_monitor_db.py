
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import Column, String, Integer, DateTime,BigInteger,Boolean
import datetime
import os

# Define DB location
script_dir = os.path.dirname(os.path.abspath(__file__))
db_file_name = f'{script_dir}/sqlalchemy_router_int_sqlite3.db'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False', echo=False)
Base = declarative_base()

# 记录路由器各类metric的表
class InterfaceMonitor(Base):
    __tablename__ = 'interface_monitor'

    id = Column(Integer, primary_key=True, autoincrement=True) # 唯一ID，主键
    device_ip = Column(String(64), nullable=False,comment="设备管理IP") 
    interface_name = Column(String(64), nullable=False,comment="接口名称")
    in_bytes = Column(BigInteger, nullable=False, comment="接口入站字节数")
    out_bytes = Column(BigInteger, nullable=False, comment="接口出站字节数")


    # 记录时间
    record_datetime = Column(DateTime(timezone=True), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(路由器IP: {self.device_ip} " \
               f"| 时间: {self.record_datetime} " \
               f"| 接口名称: {self.interface_name} " \
               f"| 入向字节数: {self.in_bytes} " \
               f"| 出向字节数: {self.out_bytes})"
    

if __name__ == '__main__':
    Base.metadata.create_all(engine,checkfirst=True)