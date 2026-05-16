"""
Repository reader module for cloning and extracting content from GitHub repositories.
"""
import os
import shutil
import subprocess
import tempfile
import mimetypes
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse


class RepoReaderError(Exception):
    """Custom exception for repository reading errors."""
    pass


def is_binary_file(file_path: Path) -> bool:
    """
    Check if a file is binary by checking its mimetype.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if file is binary, False otherwise
    """
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        # If mimetype is unknown, try reading first few bytes
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                # Check for null bytes which indicate binary
                return b'\x00' in chunk
        except Exception:
            return True
    
    # Consider text types as non-binary
    return not mime_type.startswith('text/')


def should_ignore_path(path: Path, base_path: Path) -> bool:
    """
    Check if a path should be ignored based on common patterns.
    
    Args:
        path: Path to check
        base_path: Base repository path
        
    Returns:
        True if path should be ignored, False otherwise
    """
    relative_path = path.relative_to(base_path)
    path_parts = relative_path.parts
    
    # Directories to ignore
    ignore_dirs = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv',
        'dist', 'build', '.next', '.nuxt', 'coverage', '.pytest_cache',
        '.mypy_cache', '.tox', 'vendor', 'target'
    }
    
    # Files to ignore
    ignore_files = {
        '.env', '.env.local', '.env.production', '.DS_Store',
        'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock'
    }
    
    # Check if any part of the path is in ignore list
    if any(part in ignore_dirs for part in path_parts):
        return True
    
    # Check if filename should be ignored
    if path.name in ignore_files:
        return True
    
    # Ignore hidden files (except specific ones we might want)
    if path.name.startswith('.') and path.name not in {'.gitignore', '.env.example'}:
        return True
    
    return False


def extract_repo_name(repo_url: str) -> str:
    """
    Extract repository name from GitHub URL.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Repository name
        
    Raises:
        RepoReaderError: If URL is invalid
    """
    try:
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) < 2:
            raise RepoReaderError(f"Invalid GitHub URL format: {repo_url}")
        
        # Remove .git suffix if present
        repo_name = path_parts[-1].replace('.git', '')
        return f"{path_parts[-2]}_{repo_name}"
    except Exception as e:
        raise RepoReaderError(f"Failed to parse repository URL: {str(e)}")


def clone_and_read(repo_url: str, max_chars_per_file: int = 3000) -> Dict[str, str]:
    """
    Clone a GitHub repository and read its contents.
    
    This function:
    1. Clones the repository with depth=1 (shallow clone)
    2. Reads all text files, ignoring binaries and common ignore patterns
    3. Limits each file to max_chars_per_file characters
    4. Returns a dictionary mapping relative paths to file contents
    5. Cleans up the temporary directory
    
    Args:
        repo_url: GitHub repository URL (must start with https://github.com/)
        max_chars_per_file: Maximum characters to read per file (default: 3000)
        
    Returns:
        Dictionary mapping relative file paths to their contents
        
    Raises:
        RepoReaderError: If cloning fails or URL is invalid
    """
    # Validate URL
    if not repo_url.startswith('https://github.com/'):
        raise RepoReaderError("URL must start with 'https://github.com/'")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix='bob_repo_')
    repo_name = extract_repo_name(repo_url)
    clone_path = Path(temp_dir) / repo_name
    
    try:
        # Clone repository with shallow depth
        print(f"Cloning repository: {repo_url}")
        result = subprocess.run(
            ['git', 'clone', '--depth=1', repo_url, str(clone_path)],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout for cloning
        )
        
        if result.returncode != 0:
            raise RepoReaderError(f"Git clone failed: {result.stderr}")
        
        print(f"Repository cloned to: {clone_path}")
        
        # Read files
        file_contents = {}
        files_read = 0
        files_skipped = 0
        
        for file_path in clone_path.rglob('*'):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip ignored paths
            if should_ignore_path(file_path, clone_path):
                files_skipped += 1
                continue
            
            # Skip binary files
            if is_binary_file(file_path):
                files_skipped += 1
                continue
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(max_chars_per_file)
                    
                    # Get relative path for the key
                    relative_path = file_path.relative_to(clone_path)
                    file_contents[str(relative_path)] = content
                    files_read += 1
                    
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {str(e)}")
                files_skipped += 1
                continue
        
        print(f"Files read: {files_read}, Files skipped: {files_skipped}")
        
        if not file_contents:
            raise RepoReaderError("No readable files found in repository")
        
        return file_contents
        
    except subprocess.TimeoutExpired:
        raise RepoReaderError("Repository cloning timed out (exceeded 2 minutes)")
    except Exception as e:
        if isinstance(e, RepoReaderError):
            raise
        raise RepoReaderError(f"Unexpected error while reading repository: {str(e)}")
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up temporary directory {temp_dir}: {str(e)}")


if __name__ == "__main__":
    # Test with FastAPI repository
    test_url = "https://github.com/tiangolo/fastapi"
    print(f"\nTesting repo_reader with: {test_url}\n")
    
    try:
        contents = clone_and_read(test_url)
        print(f"\nSuccessfully read {len(contents)} files")
        print("\nFirst 5 files:")
        for i, (path, content) in enumerate(list(contents.items())[:5]):
            print(f"\n{i+1}. {path} ({len(content)} chars)")
            print(f"   Preview: {content[:100]}...")
    except RepoReaderError as e:
        print(f"Error: {e}")

# Made with Bob
