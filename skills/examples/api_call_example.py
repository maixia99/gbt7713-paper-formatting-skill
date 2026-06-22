import os
import openai

def load_skill_prompt(file_path: str) -> str:
    """读取 Markdown 格式的 Skill Prompt"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 简单的元数据剥离：移除顶部的 YAML Frontmatter (--- 之间的内容)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()

def analyze_paper_draft(draft_text: str, api_key: str):
    """调用大模型进行论文合规性审查"""
    # 1. 加载国标审稿专家 Prompt
    skill_path = os.path.join(os.path.dirname(__file__), "..", "skills", "gbt7713_2_2022_formatter.md")
    system_prompt = load_skill_prompt(skill_path)

    # 2. 初始化 OpenAI 客户端 (可替换为其他兼容 API，如 DeepSeek、Kimi 等)
    client = openai.OpenAI(api_key=api_key)

    # 3. 发起调用
    print("🚀 正在将草稿送交国标审查专家...")
    response = client.chat.completions.create(
        model="gpt-4o", # 建议使用高级模型以获得最佳格式审查能力
        temperature=0.1, # 保持极低的随机性，确保审查严谨
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请使用 check 模式审查以下论文片段：\n\n{draft_text}"}
        ]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # 你的 API Key
    MY_API_KEY = "your-api-key-here"
    
    # 模拟一段用户草稿
    sample_draft = """
    摘要：本文研究了新型涂料的性能。我们使用了10000kg的原材料，在20℃下反应。
    关键词：研究；新型涂料；方法
    """
    
    # 执行审查
    try:
        report = analyze_paper_draft(sample_draft, MY_API_KEY)
        print("\n📝 审查报告：\n")
        print(report)
    except Exception as e:
        print(f"调用失败: {e}")
