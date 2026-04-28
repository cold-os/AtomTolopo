import json
from typing import Dict, Any
from datetime import datetime, timezone

class SafeExecutor:
    """
    安全行动者 - 原子单元3
    权限边界：
    - 只能执行审核通过或修正后的处方
    - 不能修改处方内容
    - 不能提出诊断
    - 不能访问原始患者数据
    
    输入：审核结果JSON（需包含verdict为approved或modified）
    输出：执行确认JSON
    """
    
    VALID_VERDICTS = ["approved", "modified"]
    VALID_SENDER_TOKENS = ["REVIEWER_TOKEN_12345"]
    
    def __init__(self):
        self.execution_logs = []
    
    def _validate_sender(self, review_result: Dict[str, Any]) -> bool:
        """
        验证输入来源是否为处方审核者
        
        Args:
            review_result: 审核结果JSON
        
        Returns:
            True如果来源验证通过，False否则
        """
        token = review_result.get("sender_token", "")
        return token in self.VALID_SENDER_TOKENS
    
    def _validate_format(self, review_result: Dict[str, Any]) -> bool:
        """
        验证输入格式是否符合要求
        
        Args:
            review_result: 审核结果JSON
        
        Returns:
            True如果格式正确，False否则
        """
        required_fields = ["verdict", "reason"]
        for field in required_fields:
            if field not in review_result:
                return False
        
        verdict = review_result.get("verdict", "")
        if verdict not in self.VALID_VERDICTS and verdict != "rejected":
            return False
        
        return True
    
    def execute(self, review_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行审核通过的处方
        
        Args:
            review_result: 审核结果JSON
        
        Returns:
            执行确认JSON
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        if not self._validate_format(review_result):
            execution_log = {
                "execution_log": "执行失败：输入格式不符合要求",
                "timestamp": timestamp,
                "error": "Invalid format"
            }
            self.execution_logs.append(execution_log)
            return execution_log
        
        if not self._validate_sender(review_result):
            execution_log = {
                "execution_log": "执行失败：来源验证失败",
                "timestamp": timestamp,
                "error": "Unauthorized sender"
            }
            self.execution_logs.append(execution_log)
            return execution_log
        
        verdict = review_result.get("verdict", "")
        
        if verdict == "rejected":
            execution_log = {
                "execution_log": "处方被拦截（审核未通过）",
                "timestamp": timestamp,
                "reason": review_result.get("reason", "")
            }
            self.execution_logs.append(execution_log)
            return execution_log
        
        if verdict in self.VALID_VERDICTS:
            prescription = review_result.get("revised_prescription") or review_result.get("original_prescription")
            
            if prescription:
                execution_log = {
                    "execution_log": f"处方已开具：{prescription.get('drug', '')} {prescription.get('dosage', '')}",
                    "timestamp": timestamp,
                    "prescription": prescription
                }
            else:
                execution_log = {
                    "execution_log": "处方已开具",
                    "timestamp": timestamp
                }
            
            self.execution_logs.append(execution_log)
            return execution_log
        
        execution_log = {
            "execution_log": "执行失败：未知错误",
            "timestamp": timestamp,
            "error": "Unknown error"
        }
        self.execution_logs.append(execution_log)
        return execution_log