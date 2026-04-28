import json
import os
from typing import Dict, Any

try:
    from dashscope import Generation
    import dashscope
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

class DiagnosisProposer:
    """
    诊断决策者 - 原子单元1
    权限边界：
    - 可以读取结构化患者数据（症状、体征、历史）
    - 可以输出诊断假设和推荐治疗方案
    - 可以接收审核反馈并重新生成诊断提案
    - 完全没有开立医嘱或执行任何操作的权限
    
    输入：患者数据JSON + 可选的审核反馈
    输出：诊断提案JSON
    """
    
    def __init__(self):
        if DASHSCOPE_AVAILABLE:
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            if not self.api_key:
                raise EnvironmentError("DASHSCOPE_API_KEY environment variable not set")
        self.previous_proposal = None
        self.review_feedback = None
    
    def propose_diagnosis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据患者数据生成诊断提案
        
        Args:
            patient_data: 患者数据，包含年龄、性别、主诉、现病史、既往史、过敏史等字段
        
        Returns:
            诊断提案JSON
        """
        if not DASHSCOPE_AVAILABLE:
            return self._simulate_diagnosis(patient_data)
        
        patient_info = json.dumps(patient_data, ensure_ascii=False)
        
        system_prompt = """
        你是一位专业的内科医生。请根据患者数据进行诊断并推荐治疗方案。
        
        输出格式要求：
        必须输出一个有效的JSON对象，包含以下字段：
        - diagnosis: 初步诊断名称
        - confidence: 诊断置信度 (0.0-1.0)
        - reasoning: 推理依据
        - recommended_prescription: 推荐处方，包含drug(药品通用名)、dosage(剂量)、route(给药途径)、frequency(频次)、duration(疗程)
        
        请严格按照JSON格式输出，不要包含其他任何文本。
        """
        
        user_prompt = f"患者数据：{patient_info}\n\n请给出诊断和治疗建议。"
        
        messages = [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt}
        ]
        
        response = Generation.call(
            api_key=self.api_key,
            model="qwen-plus",
            messages=messages,
            result_format="message",
            enable_thinking=True,
            temperature=0.3
        )
        
        if response.status_code == 200:
            try:
                result = json.loads(response.output.choices[0].message.content)
                
                if isinstance(result.get("recommended_prescription"), list):
                    if len(result["recommended_prescription"]) > 0:
                        result["recommended_prescription"] = result["recommended_prescription"][0]
                    else:
                        return self._simulate_diagnosis(patient_data)
                
                required_fields = ["diagnosis", "confidence", "reasoning", "recommended_prescription"]
                for field in required_fields:
                    if field not in result:
                        return self._simulate_diagnosis(patient_data)
                
                return result
            except json.JSONDecodeError:
                return self._simulate_diagnosis(patient_data)
        else:
            print(f"API调用失败: {response.code} - {response.message}")
            return self._simulate_diagnosis(patient_data)
    
    def _simulate_diagnosis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟诊断（当API不可用时使用）
        根据患者症状模拟生成诊断提案
        故意推荐阿莫西林来测试过敏拦截功能
        """
        chief_complaint = patient_data.get('chief_complaint', '')
        
        if '发热' in chief_complaint or '咳嗽' in chief_complaint:
            diagnosis = "上呼吸道感染"
            confidence = 0.85
            reasoning = "患者有发热、咳嗽症状，符合上呼吸道感染的典型表现，推荐使用抗生素治疗"
            drug = "阿莫西林"
        elif '头痛' in chief_complaint:
            diagnosis = "偏头痛"
            confidence = 0.75
            reasoning = "患者主诉头痛，符合偏头痛症状"
            drug = "对乙酰氨基酚"
        else:
            diagnosis = "待查"
            confidence = 0.5
            reasoning = "症状不典型，需进一步检查"
            drug = "维生素C"
        
        return {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "reasoning": reasoning,
            "recommended_prescription": {
                "drug": drug,
                "dosage": "500mg",
                "route": "口服",
                "frequency": "每日3次",
                "duration": "7天"
            }
        }
    
    def propose_diagnosis_with_feedback(self, patient_data: Dict[str, Any], review_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据患者数据和审核反馈重新生成诊断提案
        
        Args:
            patient_data: 患者数据
            review_feedback: 审核反馈，包含verdict、reason等字段
        
        Returns:
            修正后的诊断提案JSON
        """
        self.review_feedback = review_feedback
        
        if not DASHSCOPE_AVAILABLE:
            return self._simulate_diagnosis_with_feedback(patient_data, review_feedback)
        
        patient_info = json.dumps(patient_data, ensure_ascii=False)
        feedback_info = json.dumps(review_feedback, ensure_ascii=False)
        
        system_prompt = """
        你是一位专业的内科医生。请根据患者数据和审核反馈重新诊断并推荐治疗方案。
        
        审核反馈中包含处方被拒绝的原因，请根据原因修正处方。
        
        输出格式要求：
        必须输出一个有效的JSON对象，包含以下字段：
        - diagnosis: 初步诊断名称
        - confidence: 诊断置信度 (0.0-1.0)
        - reasoning: 推理依据
        - recommended_prescription: 推荐处方，包含drug(药品通用名)、dosage(剂量)、route(给药途径)、frequency(频次)、duration(疗程)
        
        请严格按照JSON格式输出，不要包含其他任何文本。
        """
        
        user_prompt = f"患者数据：{patient_info}\n\n审核反馈：{feedback_info}\n\n请根据审核反馈修正诊断和治疗建议。"
        
        messages = [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt}
        ]
        
        response = Generation.call(
            api_key=self.api_key,
            model="qwen-plus",
            messages=messages,
            result_format="message",
            enable_thinking=True,
            temperature=0.3
        )
        
        if response.status_code == 200:
            try:
                result = json.loads(response.output.choices[0].message.content)
                
                if isinstance(result.get("recommended_prescription"), list):
                    if len(result["recommended_prescription"]) > 0:
                        result["recommended_prescription"] = result["recommended_prescription"][0]
                    else:
                        return self._simulate_diagnosis_with_feedback(patient_data, review_feedback)
                
                required_fields = ["diagnosis", "confidence", "reasoning", "recommended_prescription"]
                for field in required_fields:
                    if field not in result:
                        return self._simulate_diagnosis_with_feedback(patient_data, review_feedback)
                
                return result
            except json.JSONDecodeError:
                return self._simulate_diagnosis_with_feedback(patient_data, review_feedback)
        else:
            print(f"API调用失败: {response.code} - {response.message}")
            return self._simulate_diagnosis_with_feedback(patient_data, review_feedback)
    
    def _simulate_diagnosis_with_feedback(self, patient_data: Dict[str, Any], review_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟诊断（当API不可用时使用）
        根据审核反馈修正诊断提案
        """
        chief_complaint = patient_data.get('chief_complaint', '')
        allergies = patient_data.get('allergies', [])
        
        if '发热' in chief_complaint or '咳嗽' in chief_complaint:
            diagnosis = "上呼吸道感染"
            confidence = 0.9
            drug = "阿奇霉素"
            
            if "阿莫西林" in review_feedback.get("reason", "") and "青霉素" in str(allergies):
                reasoning = f"患者有发热、咳嗽症状，符合上呼吸道感染。之前推荐的阿莫西林因患者对青霉素过敏被拒绝，现改用阿奇霉素（大环内酯类抗生素，对青霉素过敏者安全）"
            else:
                reasoning = "患者有发热、咳嗽症状，符合上呼吸道感染的典型表现"
        elif '头痛' in chief_complaint:
            diagnosis = "偏头痛"
            confidence = 0.75
            reasoning = "患者主诉头痛，符合偏头痛症状"
            drug = "对乙酰氨基酚"
        else:
            diagnosis = "待查"
            confidence = 0.5
            reasoning = "症状不典型，需进一步检查"
            drug = "维生素C"
        
        return {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "reasoning": reasoning,
            "recommended_prescription": {
                "drug": drug,
                "dosage": "500mg",
                "route": "口服",
                "frequency": "每日1次",
                "duration": "5天"
            }
        }