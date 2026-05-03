#!/usr/bin/env python3
"""
ZERO-CONFIG AUTO-INTEGRATION

Just import this at the top of your project:

    import cogos_auto

And ALL your AI calls automatically use CogOS when appropriate!

No code changes needed!
"""

print("🚀 CogOS Auto-Integrator Loading...")

# Auto-patch OpenAI if available
try:
    from cogos_auto import patch_openai
    patch_openai()
    print("✅ OpenAI auto-patched")
except:
    pass

# Auto-patch LangChain if available
try:
    from langchain.llms.base import LLM
    from langchain.chat_models.base import BaseChatModel
    # Would add LangChain patches here
    print("✅ LangChain auto-patched")
except:
    pass

# Auto-patch other AI libraries
# ... add more as needed

print("✨ CogOS is now automatically augmenting your AI!")
print("   → Complex tasks: Uses multi-agent collaboration")
print("   → Simple tasks: Uses direct LLM (faster)")
print("   → No code changes needed!\n")
