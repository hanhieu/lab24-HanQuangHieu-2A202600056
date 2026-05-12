"""
Phase A.1 - Synthetic Test Set Generation
Generate 50 questions from document corpus with RAGAS
"""

import os
import pandas as pd
from ragas.testset import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load documents
print("Loading documents from ./docs...")
loader = DirectoryLoader("./docs", glob="**/*.md")
documents = loader.load()
print(f"Loaded {len(documents)} documents")

# Setup generator
print("Setting up RAGAS TestsetGenerator...")
generator = TestsetGenerator.from_langchain(
    generator_llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
    critic_llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
    embeddings=OpenAIEmbeddings(),
)

# Generate test set
print("Generating test set with 50 questions...")
testset = generator.generate_with_langchain_docs(
    documents=documents,
    test_size=50,
    distributions={
        simple: 0.5,
        reasoning: 0.25,
        multi_context: 0.25
    }
)

# Save to CSV
print("Saving test set to phase-a/testset_v1.csv...")
df = testset.to_pandas()
df.to_csv("phase-a/testset_v1.csv", index=False)

# Print distribution
print("\n=== Test Set Distribution ===")
print(df['evolution_type'].value_counts())
print(f"\nTotal questions: {len(df)}")
print(f"\nColumns: {list(df.columns)}")

# Print first few questions for review
print("\n=== Sample Questions ===")
for idx, row in df.head(5).iterrows():
    print(f"\n[{idx}] Type: {row['evolution_type']}")
    print(f"Question: {row['question'][:100]}...")
    print(f"Ground Truth: {row['ground_truth'][:100]}...")

print("\n✓ Test set generation complete!")
print("Next step: Review questions manually and edit phase-a/testset_review_notes.md")
