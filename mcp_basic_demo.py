from autogen import UserProxyAgent, AssistantAgent, config_list_from_dotenv
import os
import re

# LLM 설정
llm_config = {
    "config_list": config_list_from_dotenv(),
    "temperature": 0,
}

class CodeSavingDevAgent(AssistantAgent):
    def generate_reply(self, messages=None, sender=None):
        reply = super().generate_reply(messages, sender)

        if isinstance(reply, str) and "public class" in reply:
            import re
            match = re.search(r"public\s+class\s+(\w+)", reply)
            filename = f"{match.group(1)}.java" if match else "Generated.java"
            with open(filename, "w") as f:
                f.write(reply)
            print(f"✅ 자바 코드가 '{filename}' 파일로 저장되었습니다.\n")

        return reply

dev = CodeSavingDevAgent(
    name="Dev",
    llm_config=llm_config,
    system_message="You are a skilled Java developer. Respond only with the full Java code required.",
)

pm = UserProxyAgent(
    name="PM",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

pm.initiate_chat(dev)
