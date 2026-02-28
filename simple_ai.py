"""
Simple AI system without PyTorch - fast and lightweight
Uses pattern matching and templates for responses
"""
import random
from typing import List, Dict

class SimpleAI:
    def __init__(self):
        self.memory: List[str] = []
        self.patterns = {
            "hello": ["Hello! How can I help you?", "Hi there!", "Hey! What's up?"],
            "how are you": ["I'm doing great, thanks!", "I'm good! How about you?", "Excellent!"],
            "what can you do": [
                "I can chat with you, remember our conversations, and help with various tasks!",
                "I'm here to assist you with questions and have conversations.",
                "I can help you with information, answer questions, and chat!"
            ],
            "bye": ["Goodbye!", "See you later!", "Take care!"],
            "thanks": ["You're welcome!", "Happy to help!", "Anytime!"],
            "help": ["I'm here to chat and assist you. Just ask me anything!", "How can I help you today?"],
        }
        
    def respond(self, message: str) -> str:
        """Generate a response to the message"""
        # Store in memory
        self.memory.append(f"User: {message}")
        
        # Normalize message
        msg_lower = message.lower().strip()
        
        # Check patterns
        for pattern, responses in self.patterns.items():
            if pattern in msg_lower:
                response = random.choice(responses)
                self.memory.append(f"AI: {response}")
                return response
        
        # Check for questions
        if "?" in message:
            response = f"That's an interesting question about '{message[:50]}'. Let me think about that..."
            self.memory.append(f"AI: {response}")
            return response
        
        # Default response
        responses = [
            f"I understand you're talking about: {message[:50]}...",
            f"Interesting! Tell me more about that.",
            f"I see. Can you elaborate on that?",
            f"That's a good point about {message[:30]}...",
        ]
        response = random.choice(responses)
        self.memory.append(f"AI: {response}")
        return response
    
    def get_memory(self) -> List[str]:
        """Get conversation memory"""
        return self.memory[-10:]  # Last 10 messages
