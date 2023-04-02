CHAT_COMPLETIONS = [
    'gpt-4', 'gpt-4-0314', 'gpt-4-32k', 'gpt-4-32k-0314', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0301'
]

COMPLETIONS = [
    'text-davinci-003', 'text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001', 'davinci', 'curie', 'babbage', 'ada'
]

EDITS = [
    'text-davinci-edit-001', 'code-davinci-edit-001'
]

EMBEDDINGS = [
    'text-embedding-ada-002', 'text-search-ada-doc-001'
]

PREFIX_LIBRARY = {
    'joke': 'Tell me a random funny joke today: ',
    'explain': 'Explain this to me: ',
    'polish': 'Polish this for me: ',
    'grammar_check': 'Find any spelling or grammar error of this: ',
    'translate': 'Translate this to English: ',
    'writing': 'Compose a whole paragraph based on this: '
}

SYSTEM_MESSAGE_LIBRARY = {
    'brief': 'You are a helpful assistant with brief answer.',
    'detail': 'You are a helpful assistant with detailed answer.',
    'reason': 'You are a helpful assistant with reasoned answer.',
    'creative': 'You are a helpful assistant with creative answer (may not be correct).',
    'neutral': 'You are a helpful assistant with neutral answer (any biased answer is strictly forbidden).',
    'funny': 'You are a helpful assistant with funny answer (may not be neutral).',
    'correct': 'You are a helpful assistant who answers me only when you are very confident. Answer "idk" if you do not know the answer.',
    'academic': 'You are a academic researcher who precisely answers my question with logic. Answer "idk" if you do not know the answer.',
}