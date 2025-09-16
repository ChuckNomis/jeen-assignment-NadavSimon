"""
Test script to verify the document processing setup
Checks all dependencies and configurations before running the main processing
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (only for OpenAI API key)
load_dotenv('../.env')

def test_environment():
    """Test environment configuration."""
    print("🔧 Testing Environment Configuration...")
    
    # Check OpenAI API key (only thing we get from env)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("   ❌ OPENAI_API_KEY not set or using default value")
        print("   Please set a valid OpenAI API key in the .env file")
        return False
    else:
        print(f"   ✅ OpenAI API key configured (ends with: ...{api_key[-4:]})")
    
    # Show hardcoded configuration
    print("\n   📋 Hardcoded Configuration:")
    config = {
        "Embedding Model": "text-embedding-3-large",
        "Chunk Size": "1000 tokens",
        "Chunk Overlap": "200 tokens", 
        "ChromaDB Directory": "./data/chroma_db",
        "Collection Name": "ai_assistant_docs"
    }
    
    for key, value in config.items():
        print(f"   ✅ {key}: {value}")
    
    return True

def test_dependencies():
    """Test that all required packages are installed."""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        ("docling", "Document processing"),
        ("tiktoken", "Tokenization"),
        ("chromadb", "Vector database"),
        ("openai", "OpenAI embeddings"),
        ("python-dotenv", "Environment variables")
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ❌ {package}: Missing - {description}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   ❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install " + " ".join(missing_packages))
        return False
    
    return True

def test_directories():
    """Test that required directories exist."""
    print("\n📁 Testing Directory Structure...")
    
    directories = [
        ("./data/documents", "PDF documents directory"),
        ("./data/chroma_db", "ChromaDB storage (will be created)"),
    ]
    
    for dir_path, description in directories:
        path = Path(dir_path)
        if path.exists():
            if dir_path == "./data/documents":
                # Count PDF files
                pdf_count = len(list(path.glob("*.pdf")))
                print(f"   ✅ {dir_path}: {description} ({pdf_count} PDFs)")
            else:
                print(f"   ✅ {dir_path}: {description}")
        else:
            if "chroma_db" in dir_path:
                print(f"   ⚠️  {dir_path}: {description} (will be created)")
            else:
                print(f"   ❌ {dir_path}: {description} (missing)")
    
    return True

def test_pdf_files():
    """List PDF files to be processed."""
    print("\n📄 PDF Files to Process...")
    
    docs_dir = Path("./data/documents")
    if not docs_dir.exists():
        print("   ❌ Documents directory not found")
        return False
    
    pdf_files = list(docs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("   ⚠️  No PDF files found")
        return False
    
    print(f"   Found {len(pdf_files)} PDF files:")
    for i, pdf_path in enumerate(pdf_files, 1):
        file_size = pdf_path.stat().st_size / (1024 * 1024)  # Size in MB
        print(f"   {i}. {pdf_path.name} ({file_size:.1f} MB)")
    
    return True

def test_openai_connection():
    """Test OpenAI API connection."""
    print("\n🔌 Testing OpenAI Connection...")
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        
        # Test with a simple embedding request
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input="This is a test."
        )
        
        if response.data and len(response.data) > 0:
            embedding_dim = len(response.data[0].embedding)
            print(f"   ✅ OpenAI API connection successful")
            print(f"   ✅ Embedding dimension: {embedding_dim}")
            return True
        else:
            print("   ❌ Invalid response from OpenAI API")
            return False
            
    except Exception as e:
        print(f"   ❌ OpenAI connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 AI Multi-Search Assistant - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies), 
        ("Directories", test_directories),
        ("PDF Files", test_pdf_files),
        ("OpenAI Connection", test_openai_connection)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n📊 Test Summary:")
    print("-" * 30)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("-" * 30)
    
    if all_passed:
        print("🎉 All tests passed! Ready to process documents.")
        print("\nNext step: Run 'python process_documents.py'")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)