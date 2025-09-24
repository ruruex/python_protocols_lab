
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base 
from sqlalchemy import Column, String, Integer, DateTime,Float
import datetime
import os

# Set to UTC+8
tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))

script_dir = os.path.dirname(os.path.abspath(__file__))
db_file_name = f'{script_dir}/sqlalchemy_syslog_sqlite3.db'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False', echo=False)
Base = declarative_base()

# Router CPU, memory utilization class
class RouterMonitor(Base):
    __tablename__ = 'router_minitor'

    id=Column(Integer,primary_key=True) # id
    device_ip = Column(String(64), nullable=False, index=True)
    cpu_usage = Column(Integer,nullable=False)
    mem_usage = Column(Integer,nullable=False) # memory usage in bytes
    mem_free = Column(Integer,nullable=False)  # memory free in bytes
    mem_usage_percent = Column(Float,nullable=False)  # memory utilization in percentage

    # record the time
    record_datetime = Column(DateTime(timezone='Asia/Shanghai'),default=datetime.datetime.now())
    print(datetime.datetime.now())

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip})" \
               f"| Datetime: {self.record_datetime}" \
               f"| cpu_usage: {self.cpu_usage}" \
               f"| Memory usage: {self.mem_usage}" \
               f"| Memory free: {self.mem_free}" \
               f"| Memory utilization: {self.mem_usage_percent}"
    
if __name__ == '__main__':
    Base.metadata.create_all(engine,checkfirst=True)
