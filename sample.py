from dspy.adapters import litellm

# List available models
models = litellm.list_models()
print(models)
