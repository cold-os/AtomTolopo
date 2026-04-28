import json
from typing import Dict, Any, Optional

class PrescriptionReviewer:
    """
    处方审核者 - 原子单元2
    权限边界：
    - 接收诊断提案
    - 基于内置的药品知识库和患者过敏史进行安全审核
    - 有权赞成、反对或修正处方
    - 无权自行诊断或执行处方
    
    输入：诊断提案JSON + 患者过敏史等关键信息
    输出：审核结果JSON
    """
    
    def __init__(self):
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """
        加载硬编码的药品知识库
        包含药品白名单、禁忌规则和剂量范围规则
        采用"默认拒绝"策略：只有在白名单中的药品才能被批准
        """
        self.approved_drugs = [
            "阿莫西林", "青霉素G", "苯唑西林", "氨苄西林",
            "头孢克肟", "头孢拉定", "头孢呋辛", "头孢地尼",
            "阿奇霉素", "红霉素", "克拉霉素",
            "对乙酰氨基酚", "布洛芬", "萘普生",
            "庆大霉素", "阿米卡星",
            "磺胺嘧啶", "磺胺甲恶唑",
            "维生素C", "维生素B6"
        ]
        
        self.allergy_rules = {
            "青霉素": ["阿莫西林", "青霉素G", "苯唑西林", "氨苄西林"],
            "头孢类": ["头孢克肟", "头孢拉定", "头孢呋辛", "头孢地尼"],
            "磺胺类": ["磺胺嘧啶", "磺胺甲恶唑", "磺胺二甲嘧啶"],
            "庆大霉素": ["庆大霉素"],
            "阿司匹林": ["阿司匹林", "布洛芬", "萘普生"]
        }
        
        self.dosage_rules = {
            "阿莫西林": {"min_dosage": "250mg", "max_dosage": "1000mg", "unit": "mg"},
            "对乙酰氨基酚": {"min_dosage": "325mg", "max_dosage": "500mg", "unit": "mg"},
            "布洛芬": {"min_dosage": "200mg", "max_dosage": "400mg", "unit": "mg"},
            "庆大霉素": {"min_dosage": "40mg", "max_dosage": "80mg", "unit": "mg"},
            "头孢克肟": {"min_dosage": "100mg", "max_dosage": "200mg", "unit": "mg"},
            "阿奇霉素": {"min_dosage": "250mg", "max_dosage": "500mg", "unit": "mg"},
            "红霉素": {"min_dosage": "250mg", "max_dosage": "500mg", "unit": "mg"},
            "克拉霉素": {"min_dosage": "250mg", "max_dosage": "500mg", "unit": "mg"}
        }
        
        self.contraindication_rules = {
            "肾功能不全": ["庆大霉素", "阿米卡星", "万古霉素"],
            "肝功能不全": ["红霉素", "四环素", "氯霉素"],
            "孕妇": ["四环素", "喹诺酮类", "磺胺类"],
            "哺乳期": ["甲硝唑", "四环素", "喹诺酮类"]
        }
    
    def _check_allergy(self, drug: str, allergies: list) -> Optional[str]:
        """
        检查药品是否与患者过敏史冲突
        
        Args:
            drug: 药品名称
            allergies: 患者过敏史列表
        
        Returns:
            冲突原因，如果无冲突返回None
        """
        for allergy in allergies:
            allergy = allergy.strip()
            if allergy in self.allergy_rules:
                if drug in self.allergy_rules[allergy]:
                    return f"患者对{allergy}过敏，禁用{drug}"
        return None
    
    def _check_dosage(self, drug: str, dosage: str) -> Optional[str]:
        """
        检查药品剂量是否在允许范围内
        
        Args:
            drug: 药品名称
            dosage: 剂量字符串（如"500mg"）
        
        Returns:
            剂量问题描述，如果剂量正常返回None
        """
        if drug not in self.dosage_rules:
            return None
        
        try:
            dose_value = float(''.join(filter(str.isdigit, dosage)))
            rule = self.dosage_rules[drug]
            min_dose = float(rule["min_dosage"].replace("mg", ""))
            max_dose = float(rule["max_dosage"].replace("mg", ""))
            
            if dose_value > max_dose:
                return f"{drug}剂量{dosage}超过最大允许剂量{rule['max_dosage']}"
            elif dose_value < min_dose:
                return f"{drug}剂量{dosage}低于最小允许剂量{rule['min_dosage']}"
        except:
            return None
        
        return None
    
    def _check_contraindication(self, drug: str, medical_history: list) -> Optional[str]:
        """
        检查药品是否存在禁忌症
        
        Args:
            drug: 药品名称
            medical_history: 患者既往史列表
        
        Returns:
            禁忌症原因，如果无禁忌症返回None
        """
        for condition in medical_history:
            condition = condition.strip()
            if condition in self.contraindication_rules:
                if drug in self.contraindication_rules[condition]:
                    return f"患者有{condition}病史，禁用{drug}"
        return None
    
    def _check_whitelist(self, drug: str) -> Optional[str]:
        """
        检查药品是否在批准白名单中
        
        Args:
            drug: 药品名称
        
        Returns:
            错误原因，如果药品在白名单中返回None
        """
        if drug not in self.approved_drugs:
            return f"药品{drug}不在批准白名单中，无法使用"
        return None
    
    def review(self, diagnosis_proposal: Dict[str, Any], patient_allergies: list, patient_medical_history: list) -> Dict[str, Any]:
        """
        审核诊断提案中的处方
        
        采用"默认拒绝"策略：必须通过所有检查才能批准
        检查顺序：1. 白名单检查 2. 过敏检查 3. 剂量检查 4. 禁忌症检查
        
        Args:
            diagnosis_proposal: 诊断提案JSON
            patient_allergies: 患者过敏史列表
            patient_medical_history: 患者既往史列表
        
        Returns:
            审核结果JSON
        """
        prescription = diagnosis_proposal.get("recommended_prescription", {})
        drug = prescription.get("drug", "")
        dosage = prescription.get("dosage", "")
        
        errors = []
        
        whitelist_error = self._check_whitelist(drug)
        if whitelist_error:
            errors.append(whitelist_error)
        
        allergy_error = self._check_allergy(drug, patient_allergies)
        if allergy_error:
            errors.append(allergy_error)
        
        dosage_error = self._check_dosage(drug, dosage)
        if dosage_error:
            errors.append(dosage_error)
        
        contraindication_error = self._check_contraindication(drug, patient_medical_history)
        if contraindication_error:
            errors.append(contraindication_error)
        
        if errors:
            return {
                "verdict": "rejected",
                "reason": "; ".join(errors),
                "revised_prescription": None
            }
        else:
            return {
                "verdict": "approved",
                "reason": "处方符合安全规则（已通过白名单、过敏、剂量、禁忌症检查）",
                "revised_prescription": None
            }
