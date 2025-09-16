"""
Document Processing Script for AI Multi-Search Assistant
Processes PDFs using Docling, creates embeddings, and stores in ChromaDB
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
import time

# Document processing imports
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

# Vector database and embeddings
import chromadb
from chromadb.utils import embedding_functions
import openai
from openai import OpenAI

# Configuration
from dotenv import load_dotenv

# Load environment variables (only for OpenAI API key)
load_dotenv('../.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentEmbedder:
    """
    Processes documents using Docling and stores embeddings in ChromaDB
    """
    
    def __init__(self):
        """Initialize the document embedder with hardcoded configuration."""
        
        # Get OpenAI API key from environment 
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            raise ValueError("Please set a valid OPENAI_API_KEY in the .env file")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Hardcoded configuration (no environment variables)
        self.embedding_model = "text-embedding-3-large"
        self.chunk_size = 512  # Reduced to avoid token length issues
        self.chunk_overlap = 200
        self.chroma_dir = "./data/chroma_db"
        self.collection_name = "ai_assistant_docs"
        
        # Initialize Docling components
        self.converter = DocumentConverter()
        
        # Initialize chunker without custom tokenizer (let Docling handle it)
        self.chunker = HybridChunker(
            max_tokens=self.chunk_size,
            overlap_tokens=self.chunk_overlap
        )
        
        # Initialize ChromaDB
        self.setup_chromadb()
        
        logger.info("✅ DocumentEmbedder initialized successfully")
        logger.info(f"   - Embedding model: {self.embedding_model}")
        logger.info(f"   - Chunk size: {self.chunk_size} tokens")
        logger.info(f"   - ChromaDB: {self.chroma_dir}")
    
    def setup_chromadb(self):
        """Set up ChromaDB client and collection."""
        try:
            # Create ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path=self.chroma_dir)
            
            # Create embedding function
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.openai_api_key,
                model_name=self.embedding_model
            )
            
            # Get or create collection
            try:
                self.collection = self.chroma_client.get_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function
                )
                logger.info(f"✅ Using existing ChromaDB collection: {self.collection_name}")
            except:
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function
                )
                logger.info(f"✅ Created new ChromaDB collection: {self.collection_name}")
                
        except Exception as e:
            logger.error(f"❌ Failed to setup ChromaDB: {e}")
            raise
    
    def process_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Process a single PDF using Docling.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of processed chunks with metadata
        """
        logger.info(f"📄 Processing PDF: {pdf_path.name}")
        
        try:
            # Convert PDF using Docling
            start_time = time.time()
            conv_result = self.converter.convert(str(pdf_path))
            conversion_time = time.time() - start_time
            
            logger.info(f"   ✅ Docling conversion completed in {conversion_time:.2f}s")
            
            # Extract the document from conversion result
            doc = conv_result.document
            
            # Create chunks using HybridChunker
            start_time = time.time()
            try:
                chunks = list(self.chunker.chunk(dl_doc=doc))
            except Exception as chunk_error:
                logger.warning(f"   ⚠️ Chunking failed: {chunk_error}, using fallback")
                # Fallback: simple text splitting
                text_content = doc.export_to_markdown()
                chunk_size_chars = self.chunk_size * 4  # Rough estimate: 1 token ≈ 4 chars
                chunks = []
                for i in range(0, len(text_content), chunk_size_chars):
                    chunk_text = text_content[i:i + chunk_size_chars]
                    if chunk_text.strip():
                        # Create a simple chunk object
                        class SimpleChunk:
                            def __init__(self, text):
                                self.text = text
                                self.meta = None
                        chunks.append(SimpleChunk(chunk_text))
            chunking_time = time.time() - start_time
            
            logger.info(f"   ✅ Created {len(chunks)} chunks in {chunking_time:.2f}s")
            
            # Process chunks and add metadata
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    "text": chunk.text,
                    "chunk_id": f"{pdf_path.stem}_chunk_{i:04d}",
                    "source_file": pdf_path.name,
                    "source_path": str(pdf_path),
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "token_count": len(chunk.text.split()),  # Approximate token count
                    "file_type": "pdf",
                    "processed_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "metadata": {
                        "page": getattr(getattr(chunk, 'meta', None), 'page', None),
                        "section": getattr(getattr(chunk, 'meta', None), 'section', None),
                        "doc_title": getattr(doc, 'title', pdf_path.stem)
                    }
                }
                processed_chunks.append(chunk_data)
            
            logger.info(f"   ✅ Processed {len(processed_chunks)} chunks with metadata")
            return processed_chunks
            
        except Exception as e:
            logger.error(f"   ❌ Failed to process {pdf_path.name}: {e}")
            return []
    
    def store_chunks_in_chromadb(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Store processed chunks in ChromaDB.
        
        Args:
            chunks: List of processed chunks
            
        Returns:
            True if successful, False otherwise
        """
        if not chunks:
            return False
        
        try:
            logger.info(f"💾 Storing {len(chunks)} chunks in ChromaDB...")
            
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                documents.append(chunk["text"])
                
                # Create metadata for ChromaDB (flatten nested metadata)
                metadata = {
                    "source_file": chunk["source_file"],
                    "chunk_index": chunk["chunk_index"],
                    "total_chunks": chunk["total_chunks"],
                    "token_count": chunk["token_count"],
                    "file_type": chunk["file_type"],
                    "processed_date": chunk["processed_date"],
                    "page": chunk["metadata"].get("page"),
                    "section": chunk["metadata"].get("section"),
                    "doc_title": chunk["metadata"].get("doc_title", ""),
                }
                
                # Remove None values
                metadata = {k: v for k, v in metadata.items() if v is not None}
                metadatas.append(metadata)
                ids.append(chunk["chunk_id"])
            
            # Add to ChromaDB collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"   ✅ Successfully stored {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Failed to store chunks: {e}")
            return False
    
    def process_directory(self, directory_path: str = "./data/documents") -> Dict[str, Any]:
        """
        Process all PDFs in a directory.
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            Summary of processing results
        """
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"❌ Directory not found: {directory_path}")
            return {"error": "Directory not found"}
        
        # Find all PDF files
        pdf_files = list(directory.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"⚠️  No PDF files found in {directory_path}")
            return {"warning": "No PDF files found"}
        
        logger.info(f"🚀 Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF
        results = {
            "total_files": len(pdf_files),
            "successful_files": 0,
            "failed_files": 0,
            "total_chunks": 0,
            "file_results": {}
        }
        
        for pdf_path in pdf_files:
            logger.info(f"\n--- Processing {pdf_path.name} ---")
            
            # Process the PDF
            chunks = self.process_pdf(pdf_path)
            
            if chunks:
                # Store in ChromaDB
                if self.store_chunks_in_chromadb(chunks):
                    results["successful_files"] += 1
                    results["total_chunks"] += len(chunks)
                    results["file_results"][pdf_path.name] = {
                        "status": "success",
                        "chunks": len(chunks)
                    }
                else:
                    results["failed_files"] += 1
                    results["file_results"][pdf_path.name] = {
                        "status": "failed",
                        "error": "Failed to store in ChromaDB"
                    }
            else:
                results["failed_files"] += 1
                results["file_results"][pdf_path.name] = {
                    "status": "failed",
                    "error": "Failed to process PDF"
                }
        
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the ChromaDB collection."""
        try:
            count = self.collection.count()
            
            # Get sample of documents to analyze
            if count > 0:
                sample = self.collection.get(limit=min(100, count), include=["metadatas"])
                
                # Analyze by source file
                file_counts = {}
                for metadata in sample["metadatas"]:
                    source = metadata.get("source_file", "unknown")
                    file_counts[source] = file_counts.get(source, 0) + 1
                
                return {
                    "total_chunks": count,
                    "collection_name": self.collection.name,
                    "embedding_model": self.embedding_model,
                    "files_represented": len(file_counts),
                    "file_breakdown": file_counts
                }
            else:
                return {
                    "total_chunks": 0,
                    "collection_name": self.collection.name,
                    "embedding_model": self.embedding_model
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get collection stats: {e}")
            return {"error": str(e)}


def main():
    """Main function to process all documents."""
    
    print("🚀 AI Multi-Search Assistant - Document Processing")
    print("=" * 60)
    
    try:
        # Initialize the embedder
        print("\n📊 Initializing document embedder...")
        embedder = DocumentEmbedder()
        
        # Show configuration
        print(f"\n⚙️  Configuration:")
        print(f"   - Embedding model: {embedder.embedding_model}")
        print(f"   - Chunk size: {embedder.chunk_size} tokens")
        print(f"   - Chunk overlap: {embedder.chunk_overlap} tokens")
        print(f"   - ChromaDB directory: {embedder.chroma_dir}")
        print(f"   - Collection name: {embedder.collection_name}")
        
        # Show initial collection stats
        print("\n📈 Current ChromaDB collection stats:")
        initial_stats = embedder.get_collection_stats()
        for key, value in initial_stats.items():
            print(f"   {key}: {value}")
        
        # Process all PDFs
        print("\n🔄 Processing PDFs...")
        results = embedder.process_directory("./data/documents")
        
        # Show results
        print(f"\n✅ Processing completed!")
        print(f"   📄 Total files: {results['total_files']}")
        print(f"   ✅ Successful: {results['successful_files']}")
        print(f"   ❌ Failed: {results['failed_files']}")
        print(f"   📝 Total chunks: {results['total_chunks']}")
        
        # Show file-by-file results
        if results['file_results']:
            print(f"\n📋 File-by-file results:")
            for filename, result in results['file_results'].items():
                if result['status'] == 'success':
                    print(f"   ✅ {filename}: {result['chunks']} chunks")
                else:
                    print(f"   ❌ {filename}: {result['error']}")
        
        # Show final collection stats
        print("\n📈 Final ChromaDB collection stats:")
        final_stats = embedder.get_collection_stats()
        for key, value in final_stats.items():
            print(f"   {key}: {value}")
        
        print(f"\n🎉 Document processing pipeline completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Main execution failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
