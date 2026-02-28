"""
Simple AI system without PyTorch - fast and lightweight
Uses pattern matching and templates for responses
"""
import random
from typing import List, Dict
import re

class SimpleAI:
    def __init__(self):
        self.memory: List[str] = []
        self.context: Dict[str, any] = {}
        
        self.patterns = {
            # Greetings
            r"\b(hello|hi|hey|greetings)\b": [
                "Hello! How can I help you today?",
                "Hi there! What would you like to know?",
                "Hey! I'm here to assist you."
            ],
            
            # Capabilities
            r"\b(what can you do|your capabilities|what do you know|help me)\b": [
                "I can help you with:\n• Answering questions\n• Having conversations\n• Remembering our chat history\n• Providing information\n\nWhat would you like to explore?",
                "I'm designed to assist with various tasks, answer questions, and have meaningful conversations. What interests you?",
                "I can chat, answer questions, and help with information. What would you like to discuss?"
            ],
            
            # About AI
            r"\b(who are you|what are you|tell me about yourself)\b": [
                "I'm an AI assistant built to help you with information and conversations. I learn from our interactions and aim to be helpful!",
                "I'm your AI companion - here to chat, answer questions, and assist you with various tasks.",
                "I'm an intelligent assistant designed to understand and respond to your needs."
            ],
            
            # Gratitude
            r"\b(thank you|thanks|thx|appreciate)\b": [
                "You're very welcome!",
                "Happy to help!",
                "Anytime! Let me know if you need anything else.",
                "Glad I could assist!"
            ],
            
            # Farewell
            r"\b(bye|goodbye|see you|later)\b": [
                "Goodbye! Come back anytime!",
                "See you later! Have a great day!",
                "Take care! Feel free to return whenever you need help."
            ],
            
            # How are you
            r"\b(how are you|how's it going|what's up)\b": [
                "I'm functioning perfectly, thanks for asking! How can I help you?",
                "I'm doing great! Ready to assist you with anything you need.",
                "All systems operational! What brings you here today?"
            ],
            
            # Name questions
            r"\b(what is your name|your name|who should I call you)\b": [
                "You can call me AI Assistant. What's your name?",
                "I'm your AI helper! What would you like to know?",
                "I don't have a specific name, but I'm here to help you!"
            ],
            
            # Time/Date
            r"\b(what time|what day|current time|today)\b": [
                "I don't have access to real-time information, but I can help you with other questions!",
                "I can't check the current time, but I'm here to assist with other things!"
            ],
            
            # Jokes
            r"\b(tell me a joke|make me laugh|something funny)\b": [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "What do you call a bear with no teeth? A gummy bear! 🐻",
                "Why did the scarecrow win an award? He was outstanding in his field! 🌾"
            ],
            
            # Learning
            r"\b(can you learn|do you learn|remember)\b": [
                "Yes! I remember our conversation and learn from our interactions.",
                "I keep track of our chat history and use it to provide better responses!",
                "Absolutely! I'm designed to learn and improve from our conversations."
            ],
        }
        
    def respond(self, message: str) -> str:
        """Generate a response to the message"""
        # Store in memory
        self.memory.append(f"User: {message}")
        
        # Normalize message
        msg_lower = message.lower().strip()
        
        # Check patterns using regex
        for pattern, responses in self.patterns.items():
            if re.search(pattern, msg_lower):
                response = random.choice(responses)
                self.memory.append(f"AI: {response}")
                return response
        
        # Check for questions
        if "?" in message:
            question_responses = [
                f"That's an interesting question! Based on what you're asking about '{message[:40]}...', I'd say it depends on the context. Can you provide more details?",
                f"Great question! While I don't have specific data on that, I can help you think through it. What aspect interests you most?",
                f"I appreciate your curiosity about that! Let me help you explore this topic further.",
            ]
            response = random.choice(question_responses)
            self.memory.append(f"AI: {response}")
            return response
        
        # Check for keywords and provide contextual responses
        keywords = {
            "python": "Python is a great programming language! Are you working on a Python project?",
            "code": "Coding is fascinating! What kind of programming are you interested in?",
            "ai": "AI is an exciting field! I'm an example of AI technology. What would you like to know?",
            "learn": "Learning is important! What are you trying to learn about?",
            "help": "I'm here to help! What do you need assistance with?",
            "problem": "I'd be happy to help you solve that problem. Can you describe it in more detail?",
            "work": "Tell me more about what you're working on!",
            "project": "Projects are exciting! What kind of project are you thinking about?",
        }
        
        for keyword, response in keywords.items():
            if keyword in msg_lower:
                self.memory.append(f"AI: {response}")
                return response
        
        # Default intelligent responses
        default_responses = [
            f"I understand you're mentioning '{message[:40]}...'. That's interesting! Can you tell me more?",
            f"Thanks for sharing that! What would you like to know or discuss about it?",
            f"I see what you mean. How can I help you with that?",
            f"That's a good point! What aspect would you like to explore further?",
            f"Interesting perspective! What made you think of that?",
        ]
        response = random.choice(default_responses)
        self.memory.append(f"AI: {response}")
        return response
    
    def get_memory(self) -> List[str]:
        """Get conversation memory"""
        return self.memory[-10:]  # Last 10 messages
