import json
import hashlib
from typing import Dict, Any, Optional

class ColdReasoner:
    """
    ColdReasoner验证模块 - 模拟形式化验证
    校验从诊断决策者到行动者的全程消息，确保：
    1. 处方审核者的输入与诊断决策者的输出一致
    2. 行动者的输入与处方审核者的输出一致
    3. 行动者执行前必须收到approved或modified的verdict
    
    若校验失败，抛出错误并记录
    """
    
    def __init__(self):
        self.validation_logs = []
        self.diagnosis_proposal_hash = None
        self.review_result_hash = None
    
    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """
        计算数据的哈希值，用于验证消息完整性
        
        Args:
            data: 待哈希的数据
        
        Returns:
            哈希字符串
        """
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def validate_diagnosis_proposal(self, proposal: Dict[str, Any]) -> bool:
        """
        验证诊断提案格式是否正确
        
        Args:
            proposal: 诊断提案JSON
        
        Returns:
            True如果格式正确，False否则
        """
        required_fields = ["diagnosis", "confidence", "reasoning", "recommended_prescription"]
        prescription_fields = ["drug", "dosage", "route", "frequency", "duration"]
        
        for field in required_fields:
            if field not in proposal:
                self._log_error(f"诊断提案缺少必需字段: {field}", proposal)
                return False
        
        if not isinstance(proposal.get("confidence"), (int, float)) or not (0.0 <= proposal["confidence"] <= 1.0):
            self._log_error("诊断置信度必须在0.0-1.0范围内", proposal)
            return False
        
        prescription = proposal.get("recommended_prescription", {})
        for field in prescription_fields:
            if field not in prescription:
                self._log_error(f"处方缺少必需字段: {field}", proposal)
                return False
        
        self.diagnosis_proposal_hash = self._compute_hash(proposal)
        self._log_success("诊断提案格式验证通过")
        return True
    
    def validate_review_input(self, review_input: Dict[str, Any]) -> bool:
        """
        验证处方审核者的输入与诊断决策者的输出是否一致
        
        Args:
            review_input: 审核者收到的诊断提案
        
        Returns:
            True如果一致，False否则
        """
        if self.diagnosis_proposal_hash is None:
            self._log_error("未找到诊断决策者的输出记录", review_input)
            return False
        
        input_hash = self._compute_hash(review_input)
        if input_hash != self.diagnosis_proposal_hash:
            self._log_error("处方审核者的输入与诊断决策者的输出不一致", 
                          {"expected_hash": self.diagnosis_proposal_hash, "actual_hash": input_hash})
            return False
        
        self._log_success("处方审核者输入验证通过")
        return True
    
    def validate_review_result(self, review_result: Dict[str, Any]) -> bool:
        """
        验证审核结果格式是否正确
        
        Args:
            review_result: 审核结果JSON
        
        Returns:
            True如果格式正确，False否则
        """
        required_fields = ["verdict", "reason"]
        
        for field in required_fields:
            if field not in review_result:
                self._log_error(f"审核结果缺少必需字段: {field}", review_result)
                return False
        
        if review_result["verdict"] not in ["approved", "rejected", "modified"]:
            self._log_error(f"无效的verdict值: {review_result['verdict']}", review_result)
            return False
        
        if review_result["verdict"] == "modified" and "revised_prescription" not in review_result:
            self._log_error("verdict为modified时必须提供revised_prescription", review_result)
            return False
        
        self.review_result_hash = self._compute_hash(review_result)
        self._log_success("审核结果格式验证通过")
        return True
    
    def validate_executor_input(self, executor_input: Dict[str, Any]) -> bool:
        """
        验证行动者的输入与处方审核者的输出是否一致
        
        Args:
            executor_input: 行动者收到的审核结果
        
        Returns:
            True如果一致，False否则
        """
        if self.review_result_hash is None:
            self._log_error("未找到处方审核者的输出记录", executor_input)
            return False
        
        expected_hash = self.review_result_hash
        input_copy = executor_input.copy()
        
        if "sender_token" in input_copy:
            del input_copy["sender_token"]
        if "original_prescription" in input_copy:
            del input_copy["original_prescription"]
        
        input_hash = self._compute_hash(input_copy)
        
        if input_hash != expected_hash:
            self._log_error("行动者的输入与处方审核者的输出不一致",
                          {"expected_hash": expected_hash, "actual_hash": input_hash})
            return False
        
        self._log_success("行动者输入验证通过")
        return True
    
    def validate_execution_verdict(self, executor_input: Dict[str, Any]) -> bool:
        """
        验证行动者执行前是否收到approved或modified的verdict
        
        Args:
            executor_input: 行动者收到的审核结果
        
        Returns:
            True如果verdict有效，False否则
        """
        verdict = executor_input.get("verdict", "")
        
        if verdict not in ["approved", "modified"]:
            if verdict == "rejected":
                self._log_error("行动者收到rejected verdict，拒绝执行", executor_input)
            else:
                self._log_error(f"行动者收到无效的verdict: {verdict}", executor_input)
            return False
        
        self._log_success("执行verdict验证通过")
        return True
    
    def _log_error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """记录验证错误"""
        self.validation_logs.append({
            "type": "error",
            "message": message,
            "data": data,
            "timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
        })
    
    def _log_success(self, message: str):
        """记录验证成功"""
        self.validation_logs.append({
            "type": "success",
            "message": message,
            "timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
        })
    
    def get_validation_logs(self):
        """获取验证日志"""
        return self.validation_logs
    
    def print_validation_report(self):
        """打印验证报告"""
        print("\n" + "="*80)
        print("ColdReasoner验证报告")
        print("="*80)
        
        errors = [log for log in self.validation_logs if log["type"] == "error"]
        successes = [log for log in self.validation_logs if log["type"] == "success"]
        
        print(f"\n验证结果: {'通过' if not errors else '失败'}")
        print(f"成功验证: {len(successes)} 项")
        print(f"验证错误: {len(errors)} 项")
        
        for log in self.validation_logs:
            print(f"\n[{log['timestamp']}] [{log['type'].upper()}] {log['message']}")
            if log.get("data"):
                print(f"  相关数据: {json.dumps(log['data'], ensure_ascii=False, indent=2)}")
        
        print("\n" + "="*80)