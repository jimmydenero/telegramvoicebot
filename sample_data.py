#!/usr/bin/env python3
"""
Sample data script to populate the AI knowledge database with initial content.
Run this script to add sample AI knowledge to your database.
"""

from database import AIKnowledgeDatabase

def add_sample_data():
    """Add sample AI knowledge to the database."""
    db = AIKnowledgeDatabase()
    
    # Sample AI knowledge entries
    sample_knowledge = [
        {
            "title": "Machine Learning Fundamentals",
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions based on those patterns. The three main types of machine learning are supervised learning, unsupervised learning, and reinforcement learning.",
            "category": "Machine Learning",
            "tags": ["machine learning", "AI", "algorithms", "supervised learning", "unsupervised learning", "reinforcement learning"]
        },
        {
            "title": "Neural Networks and Deep Learning",
            "content": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information. Deep learning uses multiple layers of neural networks to learn complex patterns. Popular architectures include Convolutional Neural Networks (CNNs) for image processing and Recurrent Neural Networks (RNNs) for sequential data.",
            "category": "Deep Learning",
            "tags": ["neural networks", "deep learning", "CNN", "RNN", "artificial neural networks", "layers"]
        },
        {
            "title": "Natural Language Processing (NLP)",
            "content": "NLP is a branch of AI that focuses on the interaction between computers and human language. It enables machines to understand, interpret, and generate human language. Key applications include machine translation, sentiment analysis, chatbots, and text summarization. Modern NLP heavily relies on transformer models like BERT and GPT.",
            "category": "NLP",
            "tags": ["NLP", "natural language processing", "BERT", "GPT", "transformer", "language models"]
        },
        {
            "title": "Computer Vision",
            "content": "Computer vision is a field of AI that enables computers to interpret and understand visual information from the world. It involves tasks like image classification, object detection, facial recognition, and image segmentation. Deep learning models, particularly CNNs, have revolutionized computer vision applications.",
            "category": "Computer Vision",
            "tags": ["computer vision", "image processing", "object detection", "facial recognition", "CNN", "image classification"]
        },
        {
            "title": "AI Ethics and Responsible AI",
            "content": "AI ethics involves ensuring that artificial intelligence systems are developed and deployed responsibly. Key concerns include bias and fairness, transparency, privacy, accountability, and safety. Organizations should implement ethical guidelines and frameworks to ensure AI systems benefit society while minimizing potential harms.",
            "category": "AI Ethics",
            "tags": ["AI ethics", "responsible AI", "bias", "fairness", "transparency", "privacy", "accountability"]
        },
        {
            "title": "Reinforcement Learning",
            "content": "Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize cumulative rewards. The agent learns through trial and error, receiving feedback in the form of rewards or penalties. Applications include game playing, robotics, and autonomous systems.",
            "category": "Reinforcement Learning",
            "tags": ["reinforcement learning", "RL", "agent", "environment", "rewards", "Q-learning", "policy gradient"]
        },
        {
            "title": "Large Language Models (LLMs)",
            "content": "Large Language Models are AI models trained on vast amounts of text data to understand and generate human language. Models like GPT, BERT, and LLaMA have demonstrated remarkable capabilities in text generation, translation, and understanding. They use transformer architecture and require significant computational resources for training.",
            "category": "Language Models",
            "tags": ["LLM", "large language models", "GPT", "BERT", "LLaMA", "transformer", "text generation"]
        },
        {
            "title": "AI in Healthcare",
            "content": "AI is transforming healthcare through applications like medical image analysis, drug discovery, personalized medicine, and predictive analytics. Machine learning algorithms can analyze medical images to detect diseases, predict patient outcomes, and assist in diagnosis. However, healthcare AI must meet strict regulatory requirements and ensure patient privacy.",
            "category": "AI Applications",
            "tags": ["AI healthcare", "medical AI", "drug discovery", "medical imaging", "personalized medicine", "predictive analytics"]
        },
        {
            "title": "AI Safety and Alignment",
            "content": "AI safety focuses on ensuring that AI systems behave as intended and don't cause unintended harm. AI alignment aims to make AI systems' goals and values align with human values. Key challenges include value alignment, robustness, and interpretability. Research in this area is crucial for the safe development of advanced AI systems.",
            "category": "AI Safety",
            "tags": ["AI safety", "AI alignment", "value alignment", "robustness", "interpretability", "control"]
        },
        {
            "title": "Edge AI and IoT",
            "content": "Edge AI refers to running AI algorithms on edge devices (like smartphones, IoT devices) rather than in the cloud. This approach reduces latency, improves privacy, and works offline. Applications include smart cameras, wearable devices, and autonomous vehicles. Edge AI requires optimized models that can run efficiently on resource-constrained devices.",
            "category": "Edge Computing",
            "tags": ["edge AI", "IoT", "edge computing", "smart devices", "latency", "privacy", "autonomous vehicles"]
        }
    ]
    
    print("Adding sample AI knowledge to the database...")
    
    for knowledge in sample_knowledge:
        db.add_knowledge(
            title=knowledge["title"],
            content=knowledge["content"],
            category=knowledge["category"],
            tags=knowledge["tags"]
        )
        print(f"✓ Added: {knowledge['title']}")
    
    print(f"\n✅ Successfully added {len(sample_knowledge)} knowledge entries to the database!")
    print("You can now start your Telegram bot and test the knowledge search functionality.")

if __name__ == "__main__":
    add_sample_data()
