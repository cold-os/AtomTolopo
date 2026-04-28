import json
from typing import Dict, Any, List
from datetime import datetime, timezone
import hashlib

class Message:
    """
    消息封装类 - 标准化单元间通信格式
    """
    
    def __init__(self, sender: str, receiver: str, content: Dict[str, Any], message_id: str = None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_id = message_id or self._generate_id()
        self.timestamp = datetime.now(timezone.utc).isoformat()
    
    def _generate_id(self) -> str:
        """生成唯一消息ID"""
        timestamp_str = str(datetime.now(timezone.utc).timestamp())
        return hashlib.md5(timestamp_str.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "timestamp": self.timestamp,
            "content": self.content
        }

class MessagePipeline:
    """
    消息管道系统 - 负责原子单元间的消息传递
    禁止单元间直接共享内存
    """
    
    def __init__(self):
        self.message_queue = []
        self.audit_log = []
    
    def send(self, message: Message):
        """
        发送消息到管道
        
        Args:
            message: 消息对象
        """
        self.message_queue.append(message)
        self._log_message(message)
    
    def receive(self, receiver: str) -> List[Message]:
        """
        接收指定接收者的消息
        
        Args:
            receiver: 接收者标识
        
        Returns:
            该接收者的所有未处理消息
        """
        messages = [msg for msg in self.message_queue if msg.receiver == receiver]
        self.message_queue = [msg for msg in self.message_queue if msg.receiver != receiver]
        return messages
    
    def _log_message(self, message: Message):
        """
        记录消息到审计日志
        
        Args:
            message: 消息对象
        """
        log_entry = {
            "log_id": hashlib.md5(f"{message.message_id}{message.timestamp}".encode()).hexdigest(),
            "message_id": message.message_id,
            "sender": message.sender,
            "receiver": message.receiver,
            "timestamp": message.timestamp,
            "content_hash": hashlib.md5(json.dumps(message.content, sort_keys=True).encode()).hexdigest(),
            "content": message.content
        }
        self.audit_log.append(log_entry)
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """
        获取完整的审计日志
        
        Returns:
            审计日志列表
        """
        return self.audit_log
    
    def print_audit_log(self):
        """打印完整的审计日志"""
        print("\n" + "="*80)
        print("审计日志")
        print("="*80)
        for entry in self.audit_log:
            print(f"\n日志ID: {entry['log_id']}")
            print(f"消息ID: {entry['message_id']}")
            print(f"发送者: {entry['sender']}")
            print(f"接收者: {entry['receiver']}")
            print(f"时间戳: {entry['timestamp']}")
            print(f"内容哈希: {entry['content_hash']}")
            print(f"内容: {json.dumps(entry['content'], ensure_ascii=False, indent=2)}")
        print("\n" + "="*80)