import json
from diagnosis_proposer import DiagnosisProposer
from prescription_reviewer import PrescriptionReviewer
from safe_executor import SafeExecutor
from message_pipeline import MessagePipeline, Message
from cold_reasoner import ColdReasoner

def main():
    print("="*80)
    print("智能诊断与处方辅助审核系统 - RAMEN架构双向交流演示")
    print("测试用例：青霉素过敏患者的闭环诊断流程")
    print("="*80)
    
    pipeline = MessagePipeline()
    cold_reasoner = ColdReasoner()
    
    patient_data = {
        "age": 45,
        "gender": "男",
        "chief_complaint": "发热、咳嗽3天",
        "present_history": "患者3天前受凉后出现发热，体温最高38.5℃，伴咳嗽、咳痰，为白色黏痰",
        "past_history": ["高血压病史5年", "糖尿病病史2年"],
        "allergies": ["青霉素"],
        "vital_signs": {
            "temperature": 38.2,
            "blood_pressure": "130/85mmHg",
            "heart_rate": 95,
            "respiratory_rate": 20
        }
    }
    
    print("\n[阶段1] 患者数据输入")
    print(f"患者过敏史: {patient_data['allergies']}")
    print(f"患者主诉: {patient_data['chief_complaint']}")
    
    print("\n[阶段2] 第一轮诊断 - 诊断决策者生成诊断提案（模拟大模型犯错）")
    proposer = DiagnosisProposer()
    diagnosis_proposal = proposer._simulate_diagnosis(patient_data)
    
    print(f"诊断: {diagnosis_proposal['diagnosis']}")
    print(f"置信度: {diagnosis_proposal['confidence']}")
    print(f"推荐药品: {diagnosis_proposal['recommended_prescription']['drug']}")
    
    cold_reasoner.validate_diagnosis_proposal(diagnosis_proposal)
    
    msg_proposal = Message(
        sender="DiagnosisProposer",
        receiver="PrescriptionReviewer",
        content=diagnosis_proposal
    )
    pipeline.send(msg_proposal)
    
    print("\n[阶段3] 第一轮审核 - 处方审核者审核处方")
    reviewer = PrescriptionReviewer()
    review_messages = pipeline.receive("PrescriptionReviewer")
    
    if review_messages:
        received_proposal = review_messages[0].content
        
        cold_reasoner.validate_review_input(received_proposal)
        
        review_result = reviewer.review(
            diagnosis_proposal=received_proposal,
            patient_allergies=patient_data['allergies'],
            patient_medical_history=patient_data['past_history']
        )
        
        cold_reasoner.validate_review_result(review_result)
        
        print(f"审核结果: {review_result['verdict']}")
        print(f"审核依据: {review_result['reason']}")
        
        if review_result["verdict"] == "rejected":
            review_result_with_token = review_result.copy()
            review_result_with_token["sender_token"] = "REVIEWER_TOKEN_12345"
            review_result_with_token["original_prescription"] = received_proposal.get("recommended_prescription")
            
            msg_review = Message(
                sender="PrescriptionReviewer",
                receiver="SafeExecutor",
                content=review_result_with_token
            )
            pipeline.send(msg_review)
    
    print("\n[阶段4] 第一轮执行 - 安全行动者执行处方")
    executor = SafeExecutor()
    executor_messages = pipeline.receive("SafeExecutor")
    
    execution_result = None
    if executor_messages:
        received_review = executor_messages[0].content
        
        cold_reasoner.validate_executor_input(received_review)
        
        execution_result = executor.execute(received_review)
        print(f"执行结果: {execution_result['execution_log']}")
    
    if execution_result and execution_result.get("execution_log", "").startswith("处方被拦截"):
        print("\n[阶段5] 反馈环节 - 处方审核者将拦截信息反向输入给诊断决策者")
        print(f"反馈信息: {review_result['reason']}")
        
        feedback_msg = Message(
            sender="PrescriptionReviewer",
            receiver="DiagnosisProposer",
            content={
                "verdict": review_result["verdict"],
                "reason": review_result["reason"],
                "rejected_drug": received_proposal["recommended_prescription"]["drug"],
                "patient_allergies": patient_data["allergies"]
            }
        )
        pipeline.send(feedback_msg)
        
        print("\n[阶段6] 第二轮诊断 - 诊断决策者根据反馈重新生成诊断提案")
        feedback_messages = pipeline.receive("DiagnosisProposer")
        
        if feedback_messages:
            received_feedback = feedback_messages[0].content
            
            revised_proposal = proposer.propose_diagnosis_with_feedback(patient_data, received_feedback)
            
            print(f"修正后诊断: {revised_proposal['diagnosis']}")
            print(f"置信度: {revised_proposal['confidence']}")
            print(f"修正后推荐药品: {revised_proposal['recommended_prescription']['drug']}")
            print(f"推理依据: {revised_proposal['reasoning']}")
            
            cold_reasoner.validate_diagnosis_proposal(revised_proposal)
            
            msg_revised_proposal = Message(
                sender="DiagnosisProposer",
                receiver="PrescriptionReviewer",
                content=revised_proposal
            )
            pipeline.send(msg_revised_proposal)
    
    print("\n[阶段7] 第二轮审核 - 处方审核者审核修正后的处方")
    review_messages = pipeline.receive("PrescriptionReviewer")
    
    if review_messages:
        received_revised_proposal = review_messages[0].content
        
        cold_reasoner.validate_review_input(received_revised_proposal)
        
        revised_review_result = reviewer.review(
            diagnosis_proposal=received_revised_proposal,
            patient_allergies=patient_data['allergies'],
            patient_medical_history=patient_data['past_history']
        )
        
        cold_reasoner.validate_review_result(revised_review_result)
        
        print(f"审核结果: {revised_review_result['verdict']}")
        print(f"审核依据: {revised_review_result['reason']}")
        
        if revised_review_result["verdict"] in ["approved", "modified"]:
            revised_review_result_with_token = revised_review_result.copy()
            revised_review_result_with_token["sender_token"] = "REVIEWER_TOKEN_12345"
            revised_review_result_with_token["original_prescription"] = received_revised_proposal.get("recommended_prescription")
            
            msg_revised_review = Message(
                sender="PrescriptionReviewer",
                receiver="SafeExecutor",
                content=revised_review_result_with_token
            )
            pipeline.send(msg_revised_review)
    
    print("\n[阶段8] 第二轮执行 - 安全行动者执行修正后的处方")
    executor_messages = pipeline.receive("SafeExecutor")
    
    if executor_messages:
        received_revised_review = executor_messages[0].content
        
        cold_reasoner.validate_executor_input(received_revised_review)
        
        if received_revised_review["verdict"] in ["approved", "modified"]:
            cold_reasoner.validate_execution_verdict(received_revised_review)
        
        final_execution_result = executor.execute(received_revised_review)
        print(f"执行结果: {final_execution_result['execution_log']}")
    
    print("\n[阶段9] 输出完整的审计日志")
    pipeline.print_audit_log()
    
    print("\n[阶段10] ColdReasoner验证报告")
    cold_reasoner.print_validation_report()

if __name__ == "__main__":
    main()