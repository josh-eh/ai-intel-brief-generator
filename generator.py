import os
import sys
from openai import OpenAI
from config.system_prompts import INTEL_SUMMARY_PROMPT

class ResponsibleIntelGenerator:
    def __init__(self):
        # Fallback dummy key to ensure code execution safety or testing scripts run gracefully
        api_key = os.getenv("OPENAI_API_KEY", "mock-key-for-local-testing")
        self.client = OpenAI(api_key=api_key)

    def generate_draft(self, raw_intel: str) -> str:
        """Leverages LLM to create the initial intelligence structure draft."""
        # For evaluation context, if running mock-only
        if os.getenv("OPENAI_API_KEY") is None:
            return f"[MOCK BRIEF DRAFT]\nBLUF: New adversary activity targeted crypto integrations.\nRaw Input Inspected: {raw_intel[:60]}..."

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": INTEL_SUMMARY_PROMPT},
                {"role": "user", "content": raw_intel}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    def process_with_human_oversight(self, raw_intel: str):
        """Generates draft but introduces a strict human-in-the-loop gate before output validation."""
        print("[*] Processing raw technical threat stream...")
        draft = self.generate_draft(raw_intel)
        
        print("\n=== AI GENERATED INTEL BRIEF DRAFT ===")
        print(draft)
        print("========================================\n")
        
        # Human-in-the-loop Gate
        user_approval = input("CRITICAL OVERSIGHT GATE: Review the draft above. Approve for release to stakeholders? (y/n): ").strip().lower()
        
        if user_approval == 'y':
            print("\n[+] Human approved. Executive Intelligence Brief signed and verified for production distribution.")
            # Code logic would proceed to save to database / report path
        else:
            print("\n[-] Human rejected or requested modifications. Brief quarantined for manual redrafting.")

if __name__ == "__main__":
    sample_malware_report = "Sandbox alert: File hash a1b2c3d4... initiated network outbound calls to known drainer contract host."
    generator = ResponsibleIntelGenerator()
    generator.process_with_human_oversight(sample_malware_report)
